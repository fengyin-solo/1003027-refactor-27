"""业务服务汇总：按模块声明生成共用的 ModuleService 实例。

业务规则只有 app/services/base.py 一份实现，这里不再按模块各抄一遍。
"""
from __future__ import annotations

from app.modules import MODULES
from app.services.base import ModuleService

SERVICES: dict[str, ModuleService] = {spec.name: ModuleService(spec) for spec in MODULES}
