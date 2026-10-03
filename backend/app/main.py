"""通信基站运维管理平台 后端服务入口。

启动：uvicorn app.main:app --host 127.0.0.1 --port 8000
健康检查：GET /api/health
"""
from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.routers import ROUTERS
from app.schemas import ErrorResult
from app.services import SERVICES
from app.store import store

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
if not logger.handlers and not logging.getLogger().handlers:
    # uvicorn 只配置自己的 logger；root 没有处理器时给 app 补一个，重判结果才看得到。
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter("%(levelname)s [%(name)s] %(message)s"))
    logger.addHandler(_handler)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # 校验口径以当前模块声明为准：启动时把已存下的历史提交按新口径重判一遍，
    # 只记录判定结果，老记录原样保留。
    for name, service in SERVICES.items():
        verdicts = service.review_entries()
        invalid = sum(1 for verdict in verdicts if not verdict["ok"])
        if invalid:
            logger.warning("历史提交重判：%s 共 %d 条，%d 条未通过当前校验口径", name, len(verdicts), invalid)
        else:
            logger.info("历史提交重判：%s 共 %d 条，全部通过当前校验口径", name, len(verdicts))
    yield


app = FastAPI(title="通信基站运维管理平台", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def handle_http_exception(_: Request, exc: HTTPException) -> JSONResponse:
    """错误回包统一成 ok/message 一套字段，detail 保留给按老结构解析的调用方。"""
    message = exc.detail if isinstance(exc.detail, str) else "请求未通过校验"
    result = ErrorResult(message=message, detail=exc.detail)
    return JSONResponse(status_code=exc.status_code, content=jsonable_encoder(result))


@app.exception_handler(RequestValidationError)
async def handle_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
    """入参解析失败也走同一套错误字段，不再直接抛出框架默认结构。"""
    result = ErrorResult(message="入参未通过校验，请检查字段类型与必填项", detail=jsonable_encoder(exc.errors()))
    return JSONResponse(status_code=422, content=jsonable_encoder(result))


for router in ROUTERS:
    app.include_router(router)


@app.get("/api/health")
def health() -> dict[str, object]:
    """健康检查：确认服务已经监听、示例数据已经就绪。"""
    return {"ok": True, "app": settings.app_name, "modules": len(store.module_names())}


@app.get("/api/overview")
def overview() -> dict[str, object]:
    """运营概览：把各业务模块的待处理量汇总成看板卡片。"""
    return store.overview()
