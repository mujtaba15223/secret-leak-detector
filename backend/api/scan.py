from pathlib import Path
import shutil
import subprocess
import tempfile

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


def is_github_url(value: str) -> bool:
    return (
        value.startswith("https://github.com/")
        or value.startswith("http://github.com/")
    )


def clone_github_repo(url: str) -> str | None:
    """
    Clone a GitHub repository into a temporary directory.
    """

    temp_dir = tempfile.mkdtemp(
        prefix="secret_scan_"
    )

    result = subprocess.run(
        [
            "git",
            "clone",
            "--depth",
            "1",
            url,
            temp_dir,
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )

    if result.returncode != 0:
        shutil.rmtree(
            temp_dir,
            ignore_errors=True,
        )
        return None

    return temp_dir


@router.post("/")
def scan(
    request: ScanRequest,
    db: Session = Depends(get_db),
):
    """
    Scan a local directory or GitHub repository.
    """

    scan_directory_path = request.directory
    temporary_directory = None

    if is_github_url(request.directory):

        temporary_directory = clone_github_repo(
            request.directory
        )

        if temporary_directory is None:
            return {
                "error": "Unable to clone GitHub repository."
            }

        scan_directory_path = temporary_directory

    findings = scan_directory(
        scan_directory_path
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

    if temporary_directory:
        shutil.rmtree(
            temporary_directory,
            ignore_errors=True,
        )

    return {
        "scan_id": scan_record.id,
        "directory": request.directory,
        "total_findings": len(findings),
        "findings": findings,
    }