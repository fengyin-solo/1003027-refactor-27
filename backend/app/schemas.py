"""接口出入参模型：列表、动作、错误三类回包与提交入参的统一结构。

字段名全平台统一：列表 {items,total,page,size}，动作 {ok,message,entry}，
错误 {ok,message}；提交入参的解析也只在这一处。
"""
from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class PageResult(BaseModel, Generic[T]):
    """列表回包：items/total/page/size 四个字段固定不变。"""

    items: list[T]
    total: int
    page: int = 1
    size: int = 20


class ActionResult(BaseModel):
    """动作回包：成功失败都走 ok/message/entry，不再另起一套字段。"""

    ok: bool
    message: str
    entry: dict[str, Any] | None = None


class ErrorResult(BaseModel):
    """错误回包：HTTP 层出错（404/400/422 等）同样只回 ok/message。"""

    ok: bool = False
    message: str


class EntryPayload(BaseModel):
    """登记或执行动作时提交的字段集合。

    兼容两种老调用：{"values": {...}} 和平铺的 {...}（前端页面一直用后者）；
    两种形态在这里归一成一份 values，业务代码不再分别处理。
    """

    model_config = ConfigDict(extra="allow")

    values: dict[str, Any] = Field(default_factory=dict)
    remark: str | None = None

    def submitted_values(self) -> dict[str, Any]:
        """取出本次提交的字段集合：优先 values，缺省时把平铺字段当作 values。"""
        if self.values:
            return self.values
        return dict(self.model_extra or {})


class RecheckItem(BaseModel):
    """单条历史提交按现行口径重判的结果。"""

    id: int | None
    ok: bool
    missing: list[str]


class RecheckReport(BaseModel):
    """历史提交重判报告：老记录原样保留，这里只回判定。"""

    module: str
    total: int
    passed: int
    failed: int
    items: list[RecheckItem]
