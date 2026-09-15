import math
import re


# Minimum length for a string to be considered
# for entropy analysis.
MIN_LENGTH = 16

# Entropy threshold.
# Higher values indicate more randomness.
ENTROPY_THRESHOLD = 4.0


def calculate_entropy(value: str) -> float:
    """
    Calculate Shannon entropy of a string.
    """

    if not value:
        return 0.0

    frequency = {}

    for character in value:
        frequency[character] = (
            frequency.get(character, 0) + 1
        )

    entropy = 0.0
    length = len(value)

    for count in frequency.values():
        probability = count / length
        entropy -= probability * math.log2(probability)

    return entropy


def extract_candidates(line: str) -> list[str]:
    """
    Extract possible secret-like strings from a line.
    """

    return re.findall(
        r"[A-Za-z0-9+/=_\-]{16,}",
        line
    )


def detect_high_entropy(line: str) -> list[dict]:
    """
    Detect suspicious high-entropy strings.
    """

    findings = []

    candidates = extract_candidates(line)

    for candidate in candidates:

        entropy = calculate_entropy(candidate)

        if entropy >= ENTROPY_THRESHOLD:
            findings.append(
                {
                    "type": "High Entropy String",
                    "match": candidate,
                    "entropy": round(entropy, 2),
                }
            )

    return findings