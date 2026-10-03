"""接口出入参的共用结构：列表、动作、错误三类回包只在这里定义一份。

字段名全平台统一，老调用方按原有字段（items/total、ok/message、detail）解析仍然成立。
各业务模块的字段口径不再逐个建模，改由 services 里的模块声明描述。
"""
from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class PageResult(BaseModel, Generic[T]):
    """列表回包：分页字段统一为 items/total/page/size。"""

    items: list[T]
    total: int
    page: int = 1
    size: int = 20


class ActionResult(BaseModel):
    """动作回包：成功失败都是 ok/message/entry 一套字段。

    dedup 标记命中重复提交、按原记录返回的情况，老调用方忽略该字段即可。
    """

    ok: bool
    message: str
    entry: dict[str, Any] | None = None
    dedup: bool = False


class ErrorResult(BaseModel):
    """错误回包：ok 恒为 False，message 是可读说明。

    detail 与 message 同源，保留给按 FastAPI 老结构（{"detail": ...}）解析的调用方。
    """

    ok: bool = False
    message: str
    detail: Any = None


class EntryPayload(BaseModel):
    """登记或执行动作时提交的字段集合。

    动作名兼容两种提交方式：values 里带 action（接口文档的写法），
    或顶层直接给 action（页面入口的写法），两种入口读到的结果一致。
    """

    model_config = ConfigDict(extra="allow")

    values: dict[str, Any] = Field(default_factory=dict)
    remark: str | None = None

    def action_name(self) -> str:
        """取出本次请求的动作名；values.action 优先，顶层 action 兜底。"""
        action: Any = self.values.get("action")
        if action is None and self.model_extra:
            action = self.model_extra.get("action")
        return str(action or "").strip()
