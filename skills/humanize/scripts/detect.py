#!/usr/bin/env python3
"""
AI Writing Indicator Detector

Scans text files for patterns that signal AI-generated prose.
Outputs a JSON report with matches, confidence scores, and suggested fixes.

Usage:
    python3 detect.py README.md
    python3 detect.py docs/ --recursive
    python3 detect.py README.md --fix --output README.humanized.md
    python3 detect.py README.md --json
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional


@dataclass
class Match:
    pattern: str
    line_number: int
    original: str
    suggested: str
    confidence: float
    category: str


@dataclass
class FileReport:
    path: str
    matches: list = field(default_factory=list)
    auto_fixable: int = 0
    suggestions: int = 0
    flagged: int = 0


# --- Pattern Definitions ---

JARGON_MAP = {
    r'\bleverage\b': 'use',
    r'\butilize\b': 'use',
    r'\brobust\b': 'reliable',
    r'\bseamless\b': 'smooth',
    r'\becosystem\b': 'system',
    r'\bparadigm\b': 'approach',
    r'\bsynergy\b': 'cooperation',
    r'\binnovative\b': 'new',
    r'\bcutting-edge\b': 'modern',
    r'\bempower\b': 'enable',
    r'\bholistic\b': 'complete',
    r'\boptimize\b': 'improve',
    r'\bscalable\b': 'flexible',
    r'\bstreamline\b': 'simplify',
    r'\bfacilitate\b': 'help',
    r'\benhance\b': 'improve',
    r'\bpivot\b': 'change',
    r'\bactionable\b': 'practical',
    r'\bimpactful\b': 'effective',
    r'\bdelve\b': 'explore',
}

REDUNDANCY_MAP = {
    r'\badvance planning\b': 'planning',
    r'\bpast history\b': 'history',
    r'\bfinal outcome\b': 'outcome',
    r'\bfuture plans\b': 'plans',
    r'\bcurrent status\b': 'status',
    r'\bend result\b': 'result',
    r'\bbasic fundamentals\b': 'fundamentals',
    r'\bcollaborate together\b': 'collaborate',
    r'\bcompletely eliminate\b': 'eliminate',
    r'\bcombine together\b': 'combine',
}

STIFF_PHRASES = {
    r'[Ii]t is important to note that\s*': '',
    r'[Ii]t should be noted that\s*': '',
    r'[Ii]t is worth mentioning that\s*': '',
    r'[Ii]t can be seen that\s*': '',
    r'[Oo]ne should consider\s*': '',
    r'[Ii]t is essential to\s*': '',
    r'[Ii]n order to\b': 'to',
    r'[Dd]ue to the fact that\b': 'because',
    r'[Aa]t this point in time\b': 'now',
    r'[Ii]n the event that\b': 'if',
}

HEDGE_PHRASES = [
    r'\bmight potentially\b',
    r'\bcould potentially\b',
    r'\bmay perhaps\b',
    r'\bit seems that\b',
    r'\bit appears that\b',
    r'\bgenerally speaking\b',
    r'\bfor the most part\b',
    r'\bin some cases\b',
    r'\btends to be\b',
]

TRANSITION_PHRASES = [
    r'^Furthermore,\s',
    r'^Moreover,\s',
    r'^Additionally,\s',
    r'^In addition to this,\s',
    r'^Consequently,\s',
    r'^Nevertheless,\s',
    r'^Notwithstanding,\s',
    r'^In conclusion,\s',
]

AI_ATTRIBUTION = [
    r'\bClaude\b(?! [A-Z][a-z]+)',  # Claude not followed by a surname
    r'\bthe assistant\b',
    r'\bthe AI\b',
    r'\bthis AI\b',
    r'\bI am an AI\b',
    r'\bas an AI\b',
    r'\bChatGPT\b',
    r'\bGPT-\d\b',
    r'\blanguage model\b',
]


def detect_em_dashes(line: str, line_num: int) -> list[Match]:
    matches = []
    if '\u2014' in line:
        fixed = re.sub(r'\s*\u2014\s*', ', ', line).strip()
        matches.append(Match(
            pattern='em-dash',
            line_number=line_num,
            original=line.strip(),
            suggested=fixed,
            confidence=0.95,
            category='punctuation'
        ))
    return matches


def detect_jargon(line: str, line_num: int) -> list[Match]:
    matches = []
    for pattern, replacement in JARGON_MAP.items():
        if re.search(pattern, line, re.IGNORECASE):
            fixed = re.sub(pattern, replacement, line, flags=re.IGNORECASE)
            matches.append(Match(
                pattern='corporate-jargon',
                line_number=line_num,
                original=line.strip(),
                suggested=fixed.strip(),
                confidence=0.90,
                category='jargon'
            ))
            break  # one match per line per category
    return matches


def detect_redundancy(line: str, line_num: int) -> list[Match]:
    matches = []
    for pattern, replacement in REDUNDANCY_MAP.items():
        if re.search(pattern, line, re.IGNORECASE):
            fixed = re.sub(pattern, replacement, line, flags=re.IGNORECASE)
            matches.append(Match(
                pattern='redundancy',
                line_number=line_num,
                original=line.strip(),
                suggested=fixed.strip(),
                confidence=0.95,
                category='redundancy'
            ))
            break
    return matches


def detect_passive_voice(line: str, line_num: int) -> list[Match]:
    matches = []
    passive_pattern = r'\b(is|are|was|were|been|being)\s+(\w+ed|built|done|made|seen|known|given|taken|found|shown)\b'
    if re.search(passive_pattern, line, re.IGNORECASE):
        matches.append(Match(
            pattern='passive-voice',
            line_number=line_num,
            original=line.strip(),
            suggested='[rewrite in active voice]',
            confidence=0.85,
            category='voice'
        ))
    return matches


def detect_stiff_construction(line: str, line_num: int) -> list[Match]:
    matches = []
    for pattern, replacement in STIFF_PHRASES.items():
        if re.search(pattern, line):
            fixed = re.sub(pattern, replacement, line)
            # Capitalize first letter if replacement is at start of sentence
            if fixed and fixed[0].islower():
                fixed = fixed[0].upper() + fixed[1:]
            matches.append(Match(
                pattern='stiff-construction',
                line_number=line_num,
                original=line.strip(),
                suggested=fixed.strip(),
                confidence=0.90,
                category='style'
            ))
            break
    return matches


def detect_hedge_phrases(line: str, line_num: int) -> list[Match]:
    matches = []
    for pattern in HEDGE_PHRASES:
        if re.search(pattern, line, re.IGNORECASE):
            matches.append(Match(
                pattern='hedge-phrase',
                line_number=line_num,
                original=line.strip(),
                suggested='[remove hedging, be direct]',
                confidence=0.80,
                category='hedging'
            ))
            break
    return matches


def detect_transitions(line: str, line_num: int) -> list[Match]:
    matches = []
    for pattern in TRANSITION_PHRASES:
        if re.search(pattern, line):
            fixed = re.sub(pattern, '', line).strip()
            if fixed and fixed[0].islower():
                fixed = fixed[0].upper() + fixed[1:]
            matches.append(Match(
                pattern='transition-phrase',
                line_number=line_num,
                original=line.strip(),
                suggested=fixed,
                confidence=0.75,
                category='transitions'
            ))
            break
    return matches


def detect_ai_attribution(line: str, line_num: int) -> list[Match]:
    matches = []
    for pattern in AI_ATTRIBUTION:
        if re.search(pattern, line, re.IGNORECASE):
            matches.append(Match(
                pattern='ai-attribution',
                line_number=line_num,
                original=line.strip(),
                suggested='[remove AI attribution, use "I" if needed]',
                confidence=1.0,
                category='attribution'
            ))
            break
    return matches


def detect_buzzword_clusters(line: str, line_num: int) -> list[Match]:
    """Detect 3+ buzzwords in a single line."""
    buzzwords = list(JARGON_MAP.keys())
    count = sum(1 for b in buzzwords if re.search(b, line, re.IGNORECASE))
    if count >= 3:
        return [Match(
            pattern='buzzword-cluster',
            line_number=line_num,
            original=line.strip(),
            suggested='[simplify: too many buzzwords in one sentence]',
            confidence=0.90,
            category='jargon'
        )]
    return []


ALL_DETECTORS = [
    detect_em_dashes,
    detect_jargon,
    detect_redundancy,
    detect_passive_voice,
    detect_stiff_construction,
    detect_hedge_phrases,
    detect_transitions,
    detect_ai_attribution,
    detect_buzzword_clusters,
]


def is_code_block(lines: list[str], idx: int) -> bool:
    """Check if line is inside a fenced code block."""
    fence_count = 0
    for i in range(idx):
        if lines[i].strip().startswith('```'):
            fence_count += 1
    return fence_count % 2 == 1


def scan_file(filepath: str) -> FileReport:
    report = FileReport(path=filepath)
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
        return report

    for idx, line in enumerate(lines):
        line_num = idx + 1

        # Skip code blocks, frontmatter, and very short lines
        if is_code_block(lines, idx):
            continue
        stripped = line.strip()
        if not stripped or stripped.startswith('#') or stripped.startswith('|') or stripped.startswith('---'):
            continue
        if len(stripped) < 10:
            continue

        for detector in ALL_DETECTORS:
            matches = detector(line, line_num)
            for m in matches:
                report.matches.append(m)
                if m.confidence >= 0.90:
                    report.auto_fixable += 1
                elif m.confidence >= 0.70:
                    report.suggestions += 1
                else:
                    report.flagged += 1

    return report


def apply_fixes(filepath: str, report: FileReport, output_path: Optional[str] = None) -> str:
    """Apply high-confidence fixes and write to output file."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()

    # Build a map of line_number -> best fix (highest confidence)
    fixes = {}
    for m in report.matches:
        if m.confidence >= 0.90 and m.suggested and not m.suggested.startswith('['):
            if m.line_number not in fixes or m.confidence > fixes[m.line_number].confidence:
                fixes[m.line_number] = m

    # Apply fixes
    for line_num, match in fixes.items():
        idx = line_num - 1
        if idx < len(lines):
            # Preserve leading whitespace
            leading = len(lines[idx]) - len(lines[idx].lstrip())
            lines[idx] = ' ' * leading + match.suggested + '\n'

    result = ''.join(lines)
    dest = output_path or filepath
    with open(dest, 'w', encoding='utf-8') as f:
        f.write(result)
    return dest


def collect_files(path: str, recursive: bool = False) -> list[str]:
    """Collect markdown and text files from path."""
    p = Path(path)
    if p.is_file():
        return [str(p)]
    if p.is_dir():
        pattern = '**/*.md' if recursive else '*.md'
        files = list(p.glob(pattern))
        # Also include .txt files
        txt_pattern = '**/*.txt' if recursive else '*.txt'
        files.extend(p.glob(txt_pattern))
        return [str(f) for f in sorted(files)]
    return []


def print_report(reports: list[FileReport], json_output: bool = False):
    if json_output:
        data = []
        for r in reports:
            d = {
                'path': r.path,
                'auto_fixable': r.auto_fixable,
                'suggestions': r.suggestions,
                'flagged': r.flagged,
                'total': len(r.matches),
                'matches': [asdict(m) for m in r.matches]
            }
            data.append(d)
        print(json.dumps(data, indent=2))
        return

    total_matches = sum(len(r.matches) for r in reports)
    total_auto = sum(r.auto_fixable for r in reports)
    total_suggest = sum(r.suggestions for r in reports)
    total_flag = sum(r.flagged for r in reports)

    print(f"\n{'=' * 60}")
    print(f"  AI WRITING INDICATOR SCAN")
    print(f"{'=' * 60}")
    print(f"  Files scanned:  {len(reports)}")
    print(f"  Total matches:  {total_matches}")
    print(f"  Auto-fixable:   {total_auto} (confidence >= 0.90)")
    print(f"  Suggestions:    {total_suggest} (confidence 0.70-0.89)")
    print(f"  Flagged:        {total_flag} (confidence < 0.70)")

    for r in reports:
        if not r.matches:
            continue
        print(f"\n  {'─' * 56}")
        print(f"  {r.path}")
        print(f"  {'─' * 56}")

        # Group by category
        by_cat = {}
        for m in r.matches:
            by_cat.setdefault(m.category, []).append(m)

        for cat, matches in sorted(by_cat.items()):
            print(f"\n  [{cat.upper()}] ({len(matches)} matches)")
            for m in matches[:5]:  # Show up to 5 per category
                conf_label = 'AUTO' if m.confidence >= 0.90 else 'SUGGEST' if m.confidence >= 0.70 else 'FLAG'
                print(f"    L{m.line_number} [{conf_label}] {m.pattern}")
                print(f"      - {m.original[:80]}")
                if not m.suggested.startswith('['):
                    print(f"      + {m.suggested[:80]}")
            if len(matches) > 5:
                print(f"    ... and {len(matches) - 5} more")

    print(f"\n{'=' * 60}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Detect AI writing indicators in text files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s README.md                    Scan a single file
  %(prog)s docs/ --recursive            Scan all .md files in docs/
  %(prog)s README.md --fix              Auto-fix high-confidence issues in-place
  %(prog)s README.md --fix --output out.md   Fix to a new file
  %(prog)s docs/ --recursive --json     Output JSON report
        """
    )
    parser.add_argument('path', help='File or directory to scan')
    parser.add_argument('--recursive', '-r', action='store_true',
                        help='Recursively scan directories')
    parser.add_argument('--fix', action='store_true',
                        help='Auto-fix high-confidence issues (>= 0.90)')
    parser.add_argument('--output', '-o',
                        help='Output file for --fix (default: overwrite in place)')
    parser.add_argument('--json', action='store_true',
                        help='Output JSON report')

    args = parser.parse_args()

    files = collect_files(args.path, args.recursive)
    if not files:
        print(f"No files found at: {args.path}", file=sys.stderr)
        sys.exit(1)

    reports = [scan_file(f) for f in files]

    if args.fix:
        for r in reports:
            if r.auto_fixable > 0:
                dest = apply_fixes(r.path, r, args.output if len(files) == 1 else None)
                print(f"Fixed {r.auto_fixable} issues in {dest}")

    print_report(reports, json_output=args.json)


if __name__ == '__main__':
    main()
