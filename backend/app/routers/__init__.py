"""业务模块路由汇总：所有模块共用一份装配（routers.base），按声明生成。"""
from __future__ import annotations

from fastapi import APIRouter

from app.routers.base import build_router
from app.services import SERVICES

ROUTERS: list[APIRouter] = [build_router(service) for service in SERVICES.values()]
