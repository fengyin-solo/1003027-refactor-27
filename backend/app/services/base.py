"""业务规则共用实现：筛选、登记、状态流转、重判的写法全平台只此一份。

每个模块的差异只剩 app/modules.py 里的一条 ModuleSpec 声明；
状态流转只允许在这里改，路由层不做业务判断。
"""
from __future__ import annotations

from typing import Any

from app.modules import ModuleSpec
from app.store import store


def _text(value: Any) -> str:
    """把提交值归一成可比较的文本：None 当空串，首尾空白不算内容。"""
    return str(value or "").strip()


class ModuleService:
    """一个业务模块的通用规则：列表、登记、动作、历史重判。"""

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

    def validate_submission(self, values: dict[str, Any]) -> list[str]:
        """入参校验全平台只此一处：按模块声明的必填字段查缺，返回缺项清单。"""
        return [field for field in self.spec.required_fields if not _text(values.get(field))]

    def _fingerprint(self, values: dict[str, Any]) -> tuple[str, ...]:
        """提交的指纹：按必填字段归一化后取值，同一份提交得到同一个指纹。"""
        return tuple(_text(values.get(field)) for field in self.spec.required_fields)

    def create_entry(self, values: dict[str, Any]) -> tuple[dict[str, Any] | None, bool, list[str]]:
        """登记一条记录，返回 (记录, 是否新增, 缺失字段)。

        同一份提交重复提交只落一次：指纹与存量记录一致时直接沿用原记录。
        """
        missing = self.validate_submission(values)
        if missing:
            return None, False, missing
        rows = store.rows(self.spec.name)
        fingerprint = self._fingerprint(values)
        for row in rows:
            if self._fingerprint(row) == fingerprint:
                return row, False, []
        entry: dict[str, Any] = {"id": max((int(row.get("id", 0)) for row in rows), default=0) + 1}
        entry.update({field: values.get(field) for field in self.spec.required_fields})
        entry["status"] = self.spec.status_order[0]
        entry["pending"] = True
        entry["abnormal"] = False
        rows.append(entry)
        return entry, True, []

    def run_action(self, entry_id: int, action: str) -> tuple[dict[str, Any] | None, str]:
        entry = store.find(self.spec.name, entry_id)
        if entry is None:
            return None, f"{self.spec.entity} {entry_id} 不存在或已归档"
        if action not in self.spec.action_rules:
            return None, f"动作「{action}」不属于{self.spec.label}可执行范围"
        target = self.spec.action_rules[action]
        if target not in self.spec.status_order:
            return None, f"目标状态「{target}」不在允许的状态序列里"
        entry["status"] = target
        entry["pending"] = target != self.spec.status_order[-1]
        entry["abnormal"] = action in self.spec.negative_actions
        return entry, f"{self.spec.entity}已{action}"

    def recheck_entries(self) -> dict[str, Any]:
        """按现行校验口径重判已存下的历史提交；老记录原样保留，只回判定结果。"""
        items: list[dict[str, Any]] = []
        for row in store.rows(self.spec.name):
            missing = self.validate_submission(row)
            items.append({"id": row.get("id"), "ok": not missing, "missing": missing})
        passed = sum(1 for item in items if item["ok"])
        return {
            "module": self.spec.name,
            "total": len(items),
            "passed": passed,
            "failed": len(items) - passed,
            "items": items,
        }
