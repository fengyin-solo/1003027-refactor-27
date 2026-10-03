"""接口层共用实现：列表、详情、登记、动作、导出、重判的写法全平台统一。

每个模块的接口由 build_router 按 ModuleSpec 生成，不再逐模块抄写；
回包字段名统一：列表 {items,total,page,size}，动作 {ok,message,entry}，
错误由 app.main 的异常处理器统一成 {ok,message}。
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query

from app.config import settings
from app.schemas import ActionResult, EntryPayload, PageResult, RecheckReport
from app.services.base import ModuleService


def build_router(service: ModuleService) -> APIRouter:
    """按模块声明生成一组接口；路由顺序固定，固定路径先于 {entry_id} 匹配。"""
    spec = service.spec
    router = APIRouter(prefix=f"/api/{spec.name}", tags=[spec.label])
    actions_desc = "、".join(spec.action_rules)
    statuses_desc = "、".join(spec.status_order)

    @router.get("/export")
    def export_entries() -> dict[str, Any]:
        items, total = service.list_entries(page=1, size=10000)
        return {"module": spec.name, "total": total, "items": items}

    export_entries.__doc__ = f"导出{spec.label}清单：返回当前过滤条件下的全量数据。"

    @router.get("/recheck", response_model=RecheckReport)
    def recheck_entries() -> RecheckReport:
        return RecheckReport(**service.recheck_entries())

    recheck_entries.__doc__ = f"按现行校验口径重判{spec.label}历史提交；老记录原样保留，只回判定结果。"

    @router.get("", response_model=PageResult[dict])
    def list_entries(
        keyword: str | None = Query(default=None, description=f"按{spec.keyword_field}检索"),
        status: str | None = Query(default=None, description=statuses_desc),
        page: int = 1,
        size: int = 20,
    ) -> PageResult[dict]:
        if size > settings.page_size_max:
            raise HTTPException(status_code=400, detail=f"每页最多 {settings.page_size_max} 条，请缩小分页范围")
        items, total = service.list_entries(keyword=keyword, status=status, page=page, size=size)
        return PageResult(items=items, total=total, page=page, size=size)

    list_entries.__doc__ = f"按{spec.keyword_field}与状态过滤{spec.label}列表；没有数据时返回空页，不报错。"

    @router.get("/{entry_id}", response_model=dict)
    def get_entry(entry_id: int) -> dict:
        entry = service.get_entry(entry_id)
        if entry is None:
            raise HTTPException(status_code=404, detail=f"{spec.entity} {entry_id} 不存在或已归档")
        return entry

    get_entry.__doc__ = f"读取单条{spec.entity}明细；不存在时给出可读的错误说明。"

    @router.post("", response_model=ActionResult)
    def create_entry(payload: EntryPayload) -> ActionResult:
        entry, created, missing = service.create_entry(payload.submitted_values())
        if missing:
            return ActionResult(ok=False, message=f"缺少必填字段：{'、'.join(missing)}")
        if not created:
            return ActionResult(ok=True, message=f"{spec.entity}已登记（重复提交，未新增）", entry=entry)
        return ActionResult(ok=True, message=f"{spec.entity}已登记", entry=entry)

    create_entry.__doc__ = (
        f"登记一条{spec.entity}，缺字段时说明原因而不是静默丢弃；同一份提交重复提交只落一次。"
    )

    @router.post("/{entry_id}/actions", response_model=ActionResult)
    def run_action(entry_id: int, payload: EntryPayload) -> ActionResult:
        action = str(payload.submitted_values().get("action") or "").strip()
        entry, message = service.run_action(entry_id, action)
        if entry is None:
            return ActionResult(ok=False, message=message)
        return ActionResult(ok=True, message=message, entry=entry)

    run_action.__doc__ = f"对单条{spec.entity}执行{actions_desc}；不允许的动作会被拦下并说明原因。"

    return router
