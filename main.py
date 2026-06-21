from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.exceptions import AppException


app = FastAPI(title="Bazmly")


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "code": exc.code},
    )


from app.modules.routers import router
app.include_router(router)




