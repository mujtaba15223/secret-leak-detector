import re


SECRET_PATTERNS = {
    "AWS Access Key": re.compile(
        r"\bAKIA[0-9A-Z]{16}\b"
    ),

    "GitHub Token": re.compile(
        r"\bgh[pousr]_[A-Za-z0-9_]{36,}\b"
    ),

    "JWT Token": re.compile(
        r"\beyJ[A-Za-z0-9_-]{10,}\."
        r"[A-Za-z0-9_-]{10,}\."
        r"[A-Za-z0-9_-]{10,}\b"
    ),

    "Private Key": re.compile(
        r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"
    ),

    "Generic API Key": re.compile(
        r"(?i)\b(?:api[_-]?key|apikey)\s*[:=]\s*"
        r"['\"]([^'\"]{16,})['\"]"
    ),

    "Generic Secret Key": re.compile(
        r"(?i)\b(?:secret[_-]?key|secret)\s*[:=]\s*"
        r"['\"]([^'\"]{16,})['\"]"
    ),

    "Password": re.compile(
        r"(?i)\bpassword\s*[:=]\s*"
        r"['\"]([^'\"]{6,})['\"]"
    ),

    "Access Token": re.compile(
        r"(?i)\b(?:access[_-]?token|auth[_-]?token)\s*[:=]\s*"
        r"['\"]([^'\"]{16,})['\"]"
    ),

    "Database URL": re.compile(
        r"(?i)\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?)://"
        r"[^:\s]+:[^@\s]+@[^/\s]+"
    ),
}


def detect_secrets(line: str) -> list[dict]:
    """
    Detect known secret patterns in a single line.
    """

    findings = []

    for secret_type, pattern in SECRET_PATTERNS.items():

        matches = pattern.finditer(line)

        for match in matches:
            findings.append(
                {
                    "type": secret_type,
                    "match": match.group(0),
                }
            )

    return findings