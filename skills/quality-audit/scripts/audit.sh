#!/bin/bash
# Quality Audit Runner
# Detects project type and runs appropriate quality tools.
# Usage: bash audit.sh [project_dir] [--domain a11y|perf|security|deps|all]
#
# Installs tools as needed and outputs structured results.

set -euo pipefail

PROJECT_DIR="${1:-.}"
DOMAIN="${2:---domain all}"
DOMAIN="${DOMAIN#--domain }"
REPORT_DIR="${PROJECT_DIR}/.audit-reports"
mkdir -p "$REPORT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[AUDIT]${NC} $1"; }
pass() { echo -e "${GREEN}[PASS]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
fail() { echo -e "${RED}[FAIL]${NC} $1"; }

# --- Detect project type ---
detect_project() {
    cd "$PROJECT_DIR"
    if [ -f "package.json" ]; then
        echo "node"
    elif [ -f "pyproject.toml" ] || [ -f "setup.py" ] || [ -f "requirements.txt" ]; then
        echo "python"
    elif [ -f "Cargo.toml" ]; then
        echo "rust"
    elif [ -f "go.mod" ]; then
        echo "go"
    else
        echo "unknown"
    fi
}

PROJECT_TYPE=$(detect_project)
log "Project type: $PROJECT_TYPE"
log "Project dir: $(realpath $PROJECT_DIR)"
log "Report dir: $REPORT_DIR"
echo ""

# --- Dependency Audit ---
audit_deps() {
    log "=== DEPENDENCY AUDIT ==="

    if [ "$PROJECT_TYPE" = "node" ]; then
        cd "$PROJECT_DIR"
        log "Running npm audit..."
        npm audit --json > "$REPORT_DIR/npm-audit.json" 2>/dev/null || true
        npm audit 2>/dev/null | tail -20 || warn "npm audit found issues (see $REPORT_DIR/npm-audit.json)"

        log "Checking outdated packages..."
        npm outdated --json > "$REPORT_DIR/npm-outdated.json" 2>/dev/null || true
        npm outdated 2>/dev/null || pass "All packages up to date"

    elif [ "$PROJECT_TYPE" = "python" ]; then
        cd "$PROJECT_DIR"
        log "Running pip audit..."
        if ! command -v pip-audit &>/dev/null; then
            sudo pip3 install pip-audit -q 2>/dev/null
        fi
        pip-audit -r requirements.txt --format json -o "$REPORT_DIR/pip-audit.json" 2>/dev/null || true
        pip-audit -r requirements.txt 2>/dev/null || warn "pip-audit found issues"

    else
        warn "No dependency audit available for $PROJECT_TYPE"
    fi
    echo ""
}

# --- Security Audit ---
audit_security() {
    log "=== SECURITY AUDIT ==="
    cd "$PROJECT_DIR"

    # Check for secrets in code
    log "Scanning for exposed secrets..."
    SECRETS_FOUND=0
    for pattern in "API_KEY\s*=" "SECRET\s*=" "PASSWORD\s*=" "TOKEN\s*=" "aws_access_key" "private_key"; do
        MATCHES=$(grep -rn "$pattern" --include="*.py" --include="*.js" --include="*.ts" --include="*.env" --include="*.yaml" --include="*.yml" . 2>/dev/null | grep -v node_modules | grep -v ".git/" | grep -v "__pycache__" || true)
        if [ -n "$MATCHES" ]; then
            warn "Potential secret exposure: $pattern"
            echo "$MATCHES" | head -5
            SECRETS_FOUND=$((SECRETS_FOUND + 1))
        fi
    done
    if [ "$SECRETS_FOUND" -eq 0 ]; then
        pass "No obvious secret exposure found"
    fi

    # Check .gitignore
    if [ -f ".gitignore" ]; then
        for sensitive in ".env" "*.pem" "*.key" "node_modules"; do
            if grep -q "$sensitive" .gitignore 2>/dev/null; then
                pass ".gitignore covers $sensitive"
            else
                warn ".gitignore missing: $sensitive"
            fi
        done
    else
        fail "No .gitignore file found"
    fi

    # Python-specific: bandit
    if [ "$PROJECT_TYPE" = "python" ]; then
        log "Running bandit security scanner..."
        if ! command -v bandit &>/dev/null; then
            sudo pip3 install bandit -q 2>/dev/null
        fi
        bandit -r . -f json -o "$REPORT_DIR/bandit.json" --exclude "./.venv,./node_modules,./.git" 2>/dev/null || true
        bandit -r . --exclude "./.venv,./node_modules,./.git" -ll 2>/dev/null | tail -30 || pass "No high-severity issues"
    fi

    # Node-specific: check for eval, innerHTML
    if [ "$PROJECT_TYPE" = "node" ]; then
        log "Checking for dangerous patterns..."
        DANGEROUS=$(grep -rn "eval(" --include="*.js" --include="*.ts" . 2>/dev/null | grep -v node_modules | grep -v ".git/" || true)
        if [ -n "$DANGEROUS" ]; then
            warn "Found eval() usage:"
            echo "$DANGEROUS" | head -5
        else
            pass "No eval() usage found"
        fi

        INNERHTML=$(grep -rn "innerHTML\s*=" --include="*.js" --include="*.ts" --include="*.tsx" . 2>/dev/null | grep -v node_modules | grep -v ".git/" || true)
        if [ -n "$INNERHTML" ]; then
            warn "Found innerHTML assignment (XSS risk):"
            echo "$INNERHTML" | head -5
        else
            pass "No innerHTML assignment found"
        fi
    fi
    echo ""
}

# --- Performance Audit ---
audit_perf() {
    log "=== PERFORMANCE AUDIT ==="
    cd "$PROJECT_DIR"

    if [ "$PROJECT_TYPE" = "node" ]; then
        # Bundle size check
        if [ -d "dist" ] || [ -d "build" ]; then
            BUILD_DIR="dist"
            [ -d "build" ] && BUILD_DIR="build"
            log "Bundle size analysis ($BUILD_DIR/):"
            du -sh "$BUILD_DIR"/ 2>/dev/null
            find "$BUILD_DIR" -name "*.js" -exec du -sh {} \; 2>/dev/null | sort -rh | head -10
        else
            warn "No build directory found. Run build first for bundle analysis."
        fi

        # Check for large dependencies
        if [ -d "node_modules" ]; then
            log "Largest dependencies:"
            du -sh node_modules/*/ 2>/dev/null | sort -rh | head -10
        fi
    fi

    # General: large files in repo
    log "Large files in repository:"
    find . -not -path "./.git/*" -not -path "./node_modules/*" -not -path "./.venv/*" -type f -size +1M -exec du -sh {} \; 2>/dev/null | sort -rh | head -10 || pass "No files over 1MB"

    echo ""
}

# --- Accessibility Audit ---
audit_a11y() {
    log "=== ACCESSIBILITY AUDIT ==="
    cd "$PROJECT_DIR"

    # Check HTML files for basic a11y
    HTML_FILES=$(find . -name "*.html" -not -path "./node_modules/*" -not -path "./.git/*" 2>/dev/null)
    if [ -z "$HTML_FILES" ]; then
        warn "No HTML files found for accessibility audit"
        return
    fi

    for f in $HTML_FILES; do
        log "Checking: $f"

        # Check for alt attributes on images
        IMGS_NO_ALT=$(grep -c '<img[^>]*[^/]>' "$f" 2>/dev/null || echo 0)
        IMGS_WITH_ALT=$(grep -c '<img[^>]*alt=' "$f" 2>/dev/null || echo 0)
        if [ "$IMGS_NO_ALT" -gt "$IMGS_WITH_ALT" ]; then
            warn "$f: Some <img> tags may be missing alt attributes"
        else
            pass "$f: Images have alt attributes"
        fi

        # Check for lang attribute
        if grep -q '<html[^>]*lang=' "$f" 2>/dev/null; then
            pass "$f: <html> has lang attribute"
        else
            warn "$f: <html> missing lang attribute"
        fi

        # Check for viewport meta
        if grep -q 'viewport' "$f" 2>/dev/null; then
            pass "$f: Has viewport meta tag"
        else
            warn "$f: Missing viewport meta tag"
        fi

        # Check for heading hierarchy
        H1_COUNT=$(grep -c '<h1' "$f" 2>/dev/null || echo 0)
        if [ "$H1_COUNT" -eq 0 ]; then
            warn "$f: No <h1> found"
        elif [ "$H1_COUNT" -gt 1 ]; then
            warn "$f: Multiple <h1> tags ($H1_COUNT)"
        else
            pass "$f: Single <h1> present"
        fi
    done
    echo ""
}

# --- Run selected domains ---
case "$DOMAIN" in
    all)
        audit_deps
        audit_security
        audit_perf
        audit_a11y
        ;;
    deps)
        audit_deps
        ;;
    security)
        audit_security
        ;;
    perf)
        audit_perf
        ;;
    a11y)
        audit_a11y
        ;;
    *)
        echo "Unknown domain: $DOMAIN"
        echo "Usage: bash audit.sh [project_dir] [--domain a11y|perf|security|deps|all]"
        exit 1
        ;;
esac

log "=== AUDIT COMPLETE ==="
log "Reports saved to: $REPORT_DIR/"
ls -la "$REPORT_DIR/" 2>/dev/null
