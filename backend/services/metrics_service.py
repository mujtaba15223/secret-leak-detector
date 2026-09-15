from sqlalchemy.orm import Session

from backend.database.models import Scan, Finding


def get_metrics(db: Session) -> dict:
    """
    Calculate security compliance metrics.
    """

    total_scans = db.query(Scan).count()

    total_findings = db.query(Finding).count()

    critical_findings = (
        db.query(Finding)
        .filter(Finding.severity == "CRITICAL")
        .count()
    )

    high_findings = (
        db.query(Finding)
        .filter(Finding.severity == "HIGH")
        .count()
    )

    medium_findings = (
        db.query(Finding)
        .filter(Finding.severity == "MEDIUM")
        .count()
    )

    clean_scans = (
        db.query(Scan)
        .filter(Scan.total_findings == 0)
        .count()
    )

    return {
        "total_scans": total_scans,
        "total_findings": total_findings,
        "critical_findings": critical_findings,
        "high_findings": high_findings,
        "medium_findings": medium_findings,
        "blocked_commits": 0,
        "clean_scans": clean_scans,
    }