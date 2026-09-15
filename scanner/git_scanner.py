import subprocess

from scanner.scanner import scan_file
from scanner.risk_engine import is_blocking_finding


def get_staged_files() -> list[str]:
    """
    Get files that are currently staged for commit.
    """

    result = subprocess.run(
        [
            "git",
            "diff",
            "--cached",
            "--name-only",
            "--diff-filter=ACMR",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )

    if result.returncode != 0:
        print("❌ Unable to read staged Git files.")
        print(result.stderr)
        return []

    return [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]


def is_git_repository() -> bool:
    """
    Check whether the current directory is inside a Git repository.
    """

    result = subprocess.run(
        [
            "git",
            "rev-parse",
            "--is-inside-work-tree",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )

    return (
        result.returncode == 0
        and result.stdout.strip() == "true"
    )


def get_staged_file_content(file_path: str) -> str | None:
    """
    Read the staged version of a file directly from Git.
    """

    result = subprocess.run(
        [
            "git",
            "show",
            f":{file_path}",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )

    if result.returncode != 0:
        return None

    return result.stdout


def scan_staged_file(file_path: str) -> list[dict]:
    """
    Scan the staged version of one file.
    """

    content = get_staged_file_content(file_path)

    if content is None:
        return []

    findings = []

    for line_number, line in enumerate(
        content.splitlines(),
        start=1,
    ):
        from scanner.regex_detector import detect_secrets
        from scanner.entropy_detector import detect_high_entropy
        from scanner.risk_engine import calculate_risk

        for match in detect_secrets(line):

            finding = {
                "file": file_path,
                "line": line_number,
                "type": match["type"],
                "match": match["match"],
                "detection": "Regex",
            }

            findings.append(
                calculate_risk(finding)
            )

        for match in detect_high_entropy(line):

            finding = {
                "file": file_path,
                "line": line_number,
                "type": match["type"],
                "match": match["match"],
                "entropy": match["entropy"],
                "detection": "Entropy",
            }

            findings.append(
                calculate_risk(finding)
            )

    return findings


def scan_staged_files() -> list[dict]:
    """
    Scan all staged files.
    """

    findings = []

    for file_path in get_staged_files():
        findings.extend(
            scan_staged_file(file_path)
        )

    return findings


def print_git_findings(findings: list[dict]) -> None:
    """
    Print findings detected in staged files.
    """

    if not findings:
        print("\n✅ No secrets found in staged files.")
        return

    print(
        f"\n🚨 Found {len(findings)} "
        f"potential secret(s) in staged files:\n"
    )

    for finding in findings:

        print(
            f"⚠️  {finding['file']} "
            f"(line {finding['line']})"
        )

        print(
            f"   Type: {finding['type']}"
        )

        print(
            f"   Severity: {finding['severity']}"
        )

        print(
            f"   Confidence: "
            f"{finding['confidence'] * 100:.0f}%"
        )

        print(
            f"   Detection: {finding['detection']}"
        )

        print(
            f"   Match: {finding['match']}"
        )

        if "entropy" in finding:
            print(
                f"   Entropy: {finding['entropy']}"
            )

        print()


def has_blocking_findings(findings: list[dict]) -> bool:
    """
    Return True if any finding should block a commit.
    """

    return any(
        is_blocking_finding(finding)
        for finding in findings
    )


if __name__ == "__main__":

    print("\n🔐 Secret Leak Detector")
    print("=" * 30)

    if not is_git_repository():
        print("❌ This directory is not a Git repository.")
        raise SystemExit(1)

    staged_files = get_staged_files()

    if not staged_files:
        print("\nℹ️  No files are currently staged.")
        raise SystemExit(0)

    print(
        f"\n📦 Scanning {len(staged_files)} "
        f"staged file(s)...\n"
    )

    findings = scan_staged_files()

    print_git_findings(findings)

    if has_blocking_findings(findings):

        print(
            "🛑 COMMIT BLOCKED: "
            "High-risk secret detected."
        )

        raise SystemExit(1)

    print("✅ Commit check passed.")