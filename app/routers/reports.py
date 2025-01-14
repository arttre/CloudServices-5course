from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.auth import get_current_user
from app.services.reports import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/monthly")
async def get_monthly_report(current_user=Depends(get_current_user)):
    report = await ReportService().generate_monthly_report(current_user.id)
    if not report["categories"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No data available for the report"
        )
    return report
