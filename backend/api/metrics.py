from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database.models import Scan, Finding
from backend.services.metrics_service import get_metrics


router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"],
)


@router.get("/")
def metrics(
    db: Session = Depends(get_db),
):
    return get_metrics(db)


@router.delete("/clear")
def clear_data(
    db: Session = Depends(get_db),
):
    """
    Delete all scan and finding history.
    """

    db.query(Finding).delete()
    db.query(Scan).delete()

    db.commit()

    return {
        "message": "Scan history cleared successfully.",
        "status": "ok",
    }