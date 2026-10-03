"""拆站管理模块声明：只描述字段、状态与动作，逻辑走 services.base 的共用实现。"""
from __future__ import annotations

from app.services.base import ModuleSpec

SPEC = ModuleSpec(
    name="demolition",
    label="拆站管理",
    noun="拆站任务",
    keyword_field="任务编号",
    list_fields=[
        "任务编号",
        "拆除站点",
        "拆除原因",
        "拆除范围",
        "施工队伍",
        "计划工期",
        "物资回收",
        "任务状态",
    ],
    required_fields=[
        "任务编号",
        "拆除站点",
        "拆除原因",
    ],
    status_order=[
        "待审批",
        "已批复",
        "拆除中",
        "已拆除",
    ],
    action_rules={"提交审批": "已批复", "开始拆除": "拆除中", "回收完成": "已拆除"},
    negative_actions=[],
)
