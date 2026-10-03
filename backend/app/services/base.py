"""模块共用实现：列表筛选、登记校验、动作流转与历史重判都收在这一份。

每个业务模块只剩一份 ModuleSpec 声明（字段、状态、动作），逻辑不再按模块各抄一遍。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.store import store
from app.validation import missing_required, submission_fingerprint


@dataclass(frozen=True)
class ModuleSpec:
    """一个业务模块的声明：接口文案、字段口径与可执行动作。"""

    name: str  # 路由与存储用的英文模块名
    label: str  # 中文模块名，用于错误说明与接口文档
    noun: str  # 单条记录的称谓，用于动作结果文案
    keyword_field: str  # 列表关键字检索对应的字段
    list_fields: list[str]  # 列表展示的字段
    required_fields: list[str]  # 登记时必查的字段
    status_order: list[str]  # 允许的状态序列
    action_rules: dict[str, str]  # 动作 -> 目标状态
    negative_actions: list[str] = field(default_factory=list)  # 执行后标记异常的动作

    @property
    def actions(self) -> list[str]:
        return list(self.action_rules)

    def created_message(self) -> str:
        return f"{self.noun}已登记"

    def duplicate_message(self) -> str:
        return f"相同的{self.noun}提交已存在，未重复登记"

    def done_message(self, action: str) -> str:
        return f"{self.noun}已{action}"

    def not_found_message(self, entry_id: int) -> str:
        return f"{self.noun} {entry_id} 不存在或已归档"

    def out_of_scope_message(self, action: str) -> str:
        return f"动作「{action}」不属于{self.label}可执行范围"


class ModuleService:
    """按模块声明跑通的共用业务逻辑。"""

    def __init__(self, spec: ModuleSpec) -> None:
        self.spec = spec

    def list_entries(
        self,
        *,
        keyword: str | None = None,
        status: str | None = None,
        page: int = 1,
        size: int = 20,
    ) -> tuple[list[dict[str, Any]], int]:
        rows = store.rows(self.spec.name)
        if keyword:
            rows = [row for row in rows if keyword in str(row.get(self.spec.keyword_field, ""))]
        if status:
            rows = [row for row in rows if row.get("status") == status]
        total = len(rows)
        start = max(page - 1, 0) * size
        return rows[start:start + size], total

    def get_entry(self, entry_id: int) -> dict[str, Any] | None:
        return store.find(self.spec.name, entry_id)

    def create_entry(self, values: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str], bool]:
        """登记一条记录：先按统一口径校验，再按提交指纹去重，最后才落库。

        返回 (记录, 缺漏字段, 是否命中重复提交)；命中重复时返回已存在的记录，不再落库。
        """
        missing = missing_required(values, self.spec.required_fields)
        if missing:
            return None, missing, False
        fingerprint = submission_fingerprint(values, self.spec.required_fields)
        rows = store.rows(self.spec.name)
        for row in rows:
            if submission_fingerprint(row, self.spec.required_fields) == fingerprint:
                return row, [], True
        entry = {"id": max((int(row.get("id", 0)) for row in rows), default=0) + 1}
        entry.update({field: values.get(field) for field in self.spec.required_fields})
        entry["status"] = self.spec.status_order[0]
        entry["pending"] = True
        entry["abnormal"] = False
        rows.append(entry)
        return entry, [], False

    def run_action(self, entry_id: int, action: str) -> tuple[dict[str, Any] | None, str]:
        spec = self.spec
        entry = store.find(spec.name, entry_id)
        if entry is None:
            return None, spec.not_found_message(entry_id)
        if action not in spec.action_rules:
            return None, spec.out_of_scope_message(action)
        target = spec.action_rules[action]
        if target not in spec.status_order:
            return None, f"目标状态「{target}」不在允许的状态序列里"
        entry["status"] = target
        entry["pending"] = target != spec.status_order[-1]
        entry["abnormal"] = action in spec.negative_actions
        return entry, spec.done_message(action)

    def review_entries(self) -> list[dict[str, Any]]:
        """按当前校验口径重判已存下的每条记录。

        老记录原样保留，这里只产出判定结果，不回写任何字段。
        """
        verdicts = []
        for row in store.rows(self.spec.name):
            missing = missing_required(row, self.spec.required_fields)
            verdicts.append({"id": row.get("id"), "ok": not missing, "missing": missing})
        return verdicts
