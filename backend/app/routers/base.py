"""模块接口的共用装配：列表、登记、动作、导出、重判五类端点只定义一次。

各模块的差异都在 ModuleSpec 声明里；这里按声明生成路由，保证所有模块的回包结构一致。
注意 /export、/review 要注册在 /{entry_id} 之前，否则会被当成 entry_id 解析。
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query

from app.config import settings
from app.schemas import ActionResult, EntryPayload, PageResult
from app.services.base import ModuleService


def build_router(service: ModuleService) -> APIRouter:
    """按模块声明生成一套标准接口。"""
    spec = service.spec
    router = APIRouter(prefix=f"/api/{spec.name}", tags=[spec.label])
    actions = "、".join(spec.actions)
    statuses = "、".join(spec.status_order)

    @router.get(
        "",
        response_model=PageResult[dict],
        description=f"按{spec.keyword_field}与状态过滤{spec.label}列表；没有数据时返回空页，不报错。",
    )
    def list_entries(
        keyword: str | None = Query(default=None, description=f"按{spec.keyword_field}检索"),
        status: str | None = Query(default=None, description=statuses),
        page: int = 1,
        size: int = settings.page_size_default,
    ) -> PageResult[dict]:
        if size > settings.page_size_max:
            raise HTTPException(status_code=400, detail=f"每页最多 {settings.page_size_max} 条，请缩小分页范围")
        items, total = service.list_entries(keyword=keyword, status=status, page=page, size=size)
        return PageResult(items=items, total=total, page=page, size=size)

    @router.get(
        "/export",
        description=f"导出{spec.label}清单：返回当前过滤条件下的全量数据。",
    )
    def export_entries() -> dict[str, Any]:
        items, total = service.list_entries(page=1, size=10000)
        return {"module": spec.name, "items": items, "total": total, "page": 1, "size": total}

    @router.get(
        "/review",
        description=f"按当前校验口径重判{spec.label}已存下的提交；老记录原样保留，只返回判定结果。",
    )
    def review_entries() -> dict[str, Any]:
        verdicts = service.review_entries()
        invalid = sum(1 for verdict in verdicts if not verdict["ok"])
        return {"module": spec.name, "total": len(verdicts), "invalid": invalid, "items": verdicts}

    @router.get(
        "/{entry_id}",
        response_model=dict,
        description=f"读取单条{spec.noun}明细；不存在时给出可读的错误说明。",
    )
    def get_entry(entry_id: int) -> dict:
        entry = service.get_entry(entry_id)
        if entry is None:
            raise HTTPException(status_code=404, detail=spec.not_found_message(entry_id))
        return entry

    @router.post(
        "",
        response_model=ActionResult,
        description=f"登记一条{spec.noun}，缺字段时说明原因而不是静默丢弃；同一份提交重复提交只落一次。",
    )
    def create_entry(payload: EntryPayload) -> ActionResult:
        entry, missing, duplicated = service.create_entry(payload.values)
        if missing:
            return ActionResult(ok=False, message=f"缺少必填字段：{'、'.join(missing)}")
        if duplicated:
            return ActionResult(ok=True, message=spec.duplicate_message(), entry=entry, dedup=True)
        return ActionResult(ok=True, message=spec.created_message(), entry=entry)

    @router.post(
        "/{entry_id}/actions",
        response_model=ActionResult,
        description=f"对单条{spec.noun}执行{actions}；不允许的动作会被拦下并说明原因。",
    )
    def run_action(entry_id: int, payload: EntryPayload) -> ActionResult:
        entry, message = service.run_action(entry_id, payload.action_name())
        if entry is None:
            return ActionResult(ok=False, message=message)
        return ActionResult(ok=True, message=message, entry=entry)

    return router
