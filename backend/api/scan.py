from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database.models import Scan, Finding

from scanner.scanner import scan_directory
from scanner.finding_deduplicator import deduplicate_findings


router = APIRouter(
    prefix="/scan",
    tags=["Scanning"],
)


class ScanRequest(BaseModel):
    directory: str


@router.post("/")
def scan(
    request: ScanRequest,
    db: Session = Depends(get_db),
):
    """
    Scan a directory and store the results.
    """

    findings = scan_directory(
        request.directory
    )

    findings = deduplicate_findings(
        findings
    )

    scan_record = Scan(
        directory=request.directory,
        total_findings=len(findings),
    )

    db.add(scan_record)
    db.commit()
    db.refresh(scan_record)

    for finding in findings:

        finding_record = Finding(
            scan_id=scan_record.id,
            file=finding["file"],
            line=finding["line"],
            type=finding["type"],
            severity=finding["severity"],
            confidence=finding["confidence"],
            detection=finding["detection"],
            match=finding["match"],
        )

        db.add(finding_record)

    db.commit()

    return {
        "scan_id": scan_record.id,
        "directory": request.directory,
        "total_findings": len(findings),
        "findings": findings,
    }