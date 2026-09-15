SEVERITY_LEVELS = {
    "CRITICAL": 4,
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1,
}


SECRET_RISK = {
    "AWS Access Key": {
        "severity": "CRITICAL",
        "confidence": 0.99,
    },

    "GitHub Token": {
        "severity": "CRITICAL",
        "confidence": 0.99,
    },

    "Private Key": {
        "severity": "CRITICAL",
        "confidence": 1.00,
    },

    "Database URL": {
        "severity": "CRITICAL",
        "confidence": 0.98,
    },

    "JWT Token": {
        "severity": "HIGH",
        "confidence": 0.95,
    },

    "Generic API Key": {
        "severity": "HIGH",
        "confidence": 0.90,
    },

    "Generic Secret Key": {
        "severity": "HIGH",
        "confidence": 0.90,
    },

    "Password": {
        "severity": "HIGH",
        "confidence": 0.88,
    },

    "Access Token": {
        "severity": "HIGH",
        "confidence": 0.90,
    },

    "High Entropy String": {
        "severity": "MEDIUM",
        "confidence": 0.70,
    },
}


def calculate_risk(finding: dict) -> dict:
    """
    Calculate severity and confidence for a finding.
    """

    secret_type = finding.get("type", "Unknown")

    risk = SECRET_RISK.get(
        secret_type,
        {
            "severity": "LOW",
            "confidence": 0.50,
        },
    )

    return {
        **finding,
        "severity": risk["severity"],
        "confidence": risk["confidence"],
    }


def is_blocking_finding(finding: dict) -> bool:
    """
    Determine whether a finding should block a Git commit.
    """

    severity = finding.get("severity", "LOW")

    return severity in {
        "CRITICAL",
        "HIGH",
    }