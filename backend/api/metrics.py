from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.services.metrics_service import get_metrics


router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"],
)


@router.get("/")
def metrics(
    db: Session = Depends(get_db),
):
    """
    Return security compliance metrics.
    """

    return get_metrics(db)