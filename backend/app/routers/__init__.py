"""业务模块路由汇总：所有模块共用 build_router 生成的一组接口。

模块之间的差异只剩 app/modules.py 里的声明，这里按声明批量生成并挂载。
"""
from __future__ import annotations

from app.modules import MODULES
from app.routers.base import build_router
from app.services import SERVICES

ROUTERS = [build_router(SERVICES[spec.name]) for spec in MODULES]
