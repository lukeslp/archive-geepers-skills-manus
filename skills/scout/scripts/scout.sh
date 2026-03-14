#!/bin/bash
# Project Scout - Quick Reconnaissance
# Analyzes a codebase and produces a structured overview.
# Usage: bash scout.sh [project_dir] [--json]
#
# Outputs: tech stack, architecture, file stats, health indicators.

set -euo pipefail

PROJECT_DIR="${1:-.}"
JSON_MODE="${2:-}"
cd "$PROJECT_DIR"
PROJECT_DIR="$(pwd)"

# --- Tech Stack Detection ---
detect_stack() {
    local stack=""
    local frameworks=""
    local languages=""

    # Languages
    [ -n "$(find . -name '*.py' -not -path '*/node_modules/*' -not -path '*/.git/*' 2>/dev/null | head -1)" ] && languages="$languages Python"
    [ -n "$(find . -name '*.ts' -not -path '*/node_modules/*' -not -path '*/.git/*' 2>/dev/null | head -1)" ] && languages="$languages TypeScript"
    [ -n "$(find . -name '*.js' -not -path '*/node_modules/*' -not -path '*/.git/*' 2>/dev/null | head -1)" ] && languages="$languages JavaScript"
    [ -n "$(find . -name '*.rs' -not -path '*/target/*' -not -path '*/.git/*' 2>/dev/null | head -1)" ] && languages="$languages Rust"
    [ -n "$(find . -name '*.go' -not -path '*/vendor/*' -not -path '*/.git/*' 2>/dev/null | head -1)" ] && languages="$languages Go"
    [ -n "$(find . -name '*.cs' -not -path '*/.git/*' 2>/dev/null | head -1)" ] && languages="$languages C#"
    [ -n "$(find . -name '*.java' -not -path '*/.git/*' 2>/dev/null | head -1)" ] && languages="$languages Java"
    [ -n "$(find . -name '*.rb' -not -path '*/.git/*' 2>/dev/null | head -1)" ] && languages="$languages Ruby"
    [ -n "$(find . -name '*.swift' -not -path '*/.git/*' 2>/dev/null | head -1)" ] && languages="$languages Swift"

    # Frameworks (from package.json)
    if [ -f "package.json" ]; then
        grep -q '"react"' package.json 2>/dev/null && frameworks="$frameworks React"
        grep -q '"next"' package.json 2>/dev/null && frameworks="$frameworks Next.js"
        grep -q '"vue"' package.json 2>/dev/null && frameworks="$frameworks Vue"
        grep -q '"svelte"' package.json 2>/dev/null && frameworks="$frameworks Svelte"
        grep -q '"express"' package.json 2>/dev/null && frameworks="$frameworks Express"
        grep -q '"fastify"' package.json 2>/dev/null && frameworks="$frameworks Fastify"
        grep -q '"tailwindcss"' package.json 2>/dev/null && frameworks="$frameworks Tailwind"
        grep -q '"vite"' package.json 2>/dev/null && frameworks="$frameworks Vite"
        grep -q '"webpack"' package.json 2>/dev/null && frameworks="$frameworks Webpack"
        grep -q '"prisma"' package.json 2>/dev/null && frameworks="$frameworks Prisma"
        grep -q '"drizzle"' package.json 2>/dev/null && frameworks="$frameworks Drizzle"
        grep -q '"typescript"' package.json 2>/dev/null && frameworks="$frameworks TypeScript"
    fi

    # Python frameworks
    if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
        local pyfiles="requirements.txt pyproject.toml setup.cfg"
        for pf in $pyfiles; do
            if [ -f "$pf" ]; then
                grep -qi "django" "$pf" 2>/dev/null && frameworks="$frameworks Django"
                grep -qi "flask" "$pf" 2>/dev/null && frameworks="$frameworks Flask"
                grep -qi "fastapi" "$pf" 2>/dev/null && frameworks="$frameworks FastAPI"
                grep -qi "pytorch\|torch" "$pf" 2>/dev/null && frameworks="$frameworks PyTorch"
                grep -qi "tensorflow" "$pf" 2>/dev/null && frameworks="$frameworks TensorFlow"
                grep -qi "pandas" "$pf" 2>/dev/null && frameworks="$frameworks Pandas"
            fi
        done
    fi

    # Infrastructure
    [ -f "Dockerfile" ] || [ -f "docker-compose.yml" ] && stack="$stack Docker"
    [ -f ".github/workflows/"*.yml ] 2>/dev/null && stack="$stack GitHub-Actions"
    [ -f ".gitlab-ci.yml" ] && stack="$stack GitLab-CI"
    [ -f "vercel.json" ] || [ -f ".vercel" ] && stack="$stack Vercel"
    [ -f "netlify.toml" ] && stack="$stack Netlify"
    [ -d ".terraform" ] && stack="$stack Terraform"

    echo "LANGUAGES:$(echo $languages | xargs)"
    echo "FRAMEWORKS:$(echo $frameworks | xargs)"
    echo "INFRA:$(echo $stack | xargs)"
}

# --- File Statistics ---
file_stats() {
    local total_files=$(find . -type f -not -path '*/.git/*' -not -path '*/node_modules/*' -not -path '*/.venv/*' -not -path '*/target/*' 2>/dev/null | wc -l)
    local total_dirs=$(find . -type d -not -path '*/.git/*' -not -path '*/node_modules/*' -not -path '*/.venv/*' -not -path '*/target/*' 2>/dev/null | wc -l)

    echo "TOTAL_FILES:$total_files"
    echo "TOTAL_DIRS:$total_dirs"

    echo "FILE_TYPES:"
    find . -type f -not -path '*/.git/*' -not -path '*/node_modules/*' -not -path '*/.venv/*' -not -path '*/target/*' 2>/dev/null \
        | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -15
}

# --- Code Line Counts ---
line_counts() {
    echo "LINE_COUNTS:"
    for ext in py ts tsx js jsx rs go java rb cs html css md json; do
        count=$(find . -name "*.$ext" -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/.venv/*' -not -path '*/target/*' -exec cat {} + 2>/dev/null | wc -l)
        if [ "$count" -gt 0 ]; then
            printf "  %-10s %s lines\n" ".$ext" "$count"
        fi
    done
}

# --- Health Indicators ---
health_check() {
    echo "HEALTH:"

    # README
    if [ -f "README.md" ] || [ -f "readme.md" ] || [ -f "README" ]; then
        local readme_lines=$(wc -l < README.md 2>/dev/null || wc -l < readme.md 2>/dev/null || echo 0)
        if [ "$readme_lines" -gt 20 ]; then
            echo "  README: GOOD ($readme_lines lines)"
        else
            echo "  README: THIN ($readme_lines lines)"
        fi
    else
        echo "  README: MISSING"
    fi

    # License
    if [ -f "LICENSE" ] || [ -f "LICENSE.md" ] || [ -f "LICENCE" ]; then
        echo "  LICENSE: PRESENT"
    else
        echo "  LICENSE: MISSING"
    fi

    # Tests
    local test_files=$(find . -name "*test*" -o -name "*spec*" -not -path '*/node_modules/*' -not -path '*/.git/*' 2>/dev/null | wc -l)
    if [ "$test_files" -gt 0 ]; then
        echo "  TESTS: FOUND ($test_files test files)"
    else
        echo "  TESTS: NONE"
    fi

    # CI/CD
    if [ -d ".github/workflows" ] || [ -f ".gitlab-ci.yml" ] || [ -f ".circleci/config.yml" ]; then
        echo "  CI/CD: CONFIGURED"
    else
        echo "  CI/CD: NONE"
    fi

    # .gitignore
    if [ -f ".gitignore" ]; then
        echo "  GITIGNORE: PRESENT"
    else
        echo "  GITIGNORE: MISSING"
    fi

    # .env files committed
    local env_files=$(find . -name ".env" -not -path '*/.git/*' -not -path '*/node_modules/*' 2>/dev/null | wc -l)
    if [ "$env_files" -gt 0 ]; then
        echo "  ENV_FILES: WARNING ($env_files .env files found in repo)"
    else
        echo "  ENV_FILES: CLEAN"
    fi

    # Last commit
    if [ -d ".git" ]; then
        local last_commit=$(git log -1 --format="%ar" 2>/dev/null || echo "unknown")
        local total_commits=$(git rev-list --count HEAD 2>/dev/null || echo "unknown")
        local contributors=$(git shortlog -sn --no-merges 2>/dev/null | wc -l || echo "unknown")
        echo "  LAST_COMMIT: $last_commit"
        echo "  TOTAL_COMMITS: $total_commits"
        echo "  CONTRIBUTORS: $contributors"
    fi
}

# --- Directory Structure ---
dir_structure() {
    echo "STRUCTURE:"
    find . -maxdepth 2 -type d -not -path '*/.git/*' -not -path '*/node_modules/*' -not -path '*/.venv/*' -not -path '*/target/*' 2>/dev/null | sort | head -40
}

# --- Entry Points ---
entry_points() {
    echo "ENTRY_POINTS:"
    for f in index.ts index.js main.py app.py manage.py server.ts server.js main.rs main.go cmd/main.go src/index.ts src/index.js src/main.ts src/main.js src/App.tsx src/app.ts; do
        if [ -f "$f" ]; then
            echo "  $f ($(wc -l < "$f") lines)"
        fi
    done
}

# --- Output ---
echo "========================================"
echo "  PROJECT SCOUT REPORT"
echo "  $(basename $PROJECT_DIR)"
echo "  $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "========================================"
echo ""

detect_stack
echo ""
file_stats
echo ""
line_counts
echo ""
entry_points
echo ""
dir_structure
echo ""
health_check
echo ""
echo "========================================"
