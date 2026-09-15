def deduplicate_findings(findings: list[dict]) -> list[dict]:
    """
    Merge multiple detections of the same secret.

    Example:
        AWS Access Key + Generic API Key + Entropy
        on the same line will become one finding.
    """

    grouped = {}

    severity_order = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4,
    }

    for finding in findings:

        key = (
            finding.get("file"),
            finding.get("line"),
        )

        if key not in grouped:
            grouped[key] = finding
            continue

        existing = grouped[key]

        existing_score = severity_order.get(
            existing.get("severity", "LOW"),
            1,
        )

        new_score = severity_order.get(
            finding.get("severity", "LOW"),
            1,
        )

        # Keep the most severe finding.
        if new_score > existing_score:
            grouped[key] = finding

    return list(grouped.values())