# Quality Audit Tool Reference

## Node.js / TypeScript Projects

### Linting
```bash
# Install and run ESLint
npx eslint . --ext .js,.ts,.tsx --format json -o .audit-reports/eslint.json
```

### Type Checking
```bash
npx tsc --noEmit 2>&1 | tee .audit-reports/typescript.txt
```

### Test Coverage
```bash
npx jest --coverage --coverageReporters=json-summary 2>&1
# or
npx vitest run --coverage 2>&1
```

### Bundle Analysis
```bash
npx webpack-bundle-analyzer stats.json  # if using webpack
npx vite-bundle-visualizer              # if using vite
```

## Python Projects

### Linting
```bash
# Ruff (fast, modern)
sudo pip3 install ruff
ruff check . --output-format json > .audit-reports/ruff.json

# Flake8 (traditional)
sudo pip3 install flake8
flake8 . --format json --output-file .audit-reports/flake8.json
```

### Type Checking
```bash
sudo pip3 install mypy
mypy . --ignore-missing-imports 2>&1 | tee .audit-reports/mypy.txt
```

### Security
```bash
sudo pip3 install bandit
bandit -r . -f json -o .audit-reports/bandit.json
```

### Test Coverage
```bash
sudo pip3 install pytest-cov
pytest --cov=. --cov-report=json:.audit-reports/coverage.json
```

## Web Accessibility

### Lighthouse (headless)
```bash
# Requires Chrome/Chromium
npx lighthouse http://localhost:3000 --output json --output-path .audit-reports/lighthouse.json --chrome-flags="--headless --no-sandbox"
```

### axe-core (programmatic)
```bash
npx @axe-core/cli http://localhost:3000 --save .audit-reports/axe.json
```

## General

### Secret Scanning
```bash
# TruffleHog
sudo pip3 install trufflehog
trufflehog filesystem . --json > .audit-reports/secrets.json
```

### License Compliance
```bash
# Node
npx license-checker --json > .audit-reports/licenses.json

# Python
sudo pip3 install pip-licenses
pip-licenses --format json --output-file .audit-reports/licenses.json
```
