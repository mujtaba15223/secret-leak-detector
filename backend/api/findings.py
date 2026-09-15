from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database.models import Finding


router = APIRouter(
    prefix="/findings",
    tags=["Findings"],
)


@router.get("/")
def get_findings(
    db: Session = Depends(get_db),
):
    """
    Return all findings stored in the database.
    """

    findings = (
        db.query(Finding)
        .order_by(Finding.id.desc())
        .all()
    )

    results = []

    for finding in findings:

        results.append(
            {
                "id": finding.id,
                "scan_id": finding.scan_id,
                "file": finding.file,
                "line": finding.line,
                "type": finding.type,
                "severity": finding.severity,
                "confidence": finding.confidence,
                "detection": finding.detection,
                "match": finding.match,
            }
        )

    return {
        "total": len(results),
        "findings": results,
    }