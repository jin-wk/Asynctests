from datetime import datetime
from fastapi import APIRouter
from starlette.responses import Response, JSONResponse


router = APIRouter(tags=["index"])


@router.get("/")
async def index():
    now = datetime.now()
    local_now = now.astimezone()
    local_tz = local_now.tzinfo
    local_tzname = local_tz.tzname(local_now)

    return Response(
        f"API Server Current Time ({local_tzname}: {now.strftime('%Y-%m-%d %H:%M:%S')})"
    )


@router.get("/test")
async def test():
    return JSONResponse({"message": "test"})
