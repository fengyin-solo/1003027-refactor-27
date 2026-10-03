"""巡检作业模块声明：只描述字段、状态与动作，逻辑走 services.base 的共用实现。"""
from __future__ import annotations

from app.services.base import ModuleSpec

SPEC = ModuleSpec(
    name="patrol",
    label="巡检作业",
    noun="巡检任务",
    keyword_field="任务编号",
    list_fields=[
        "任务编号",
        "巡检站点",
        "巡检人员",
        "计划日期",
        "巡检路线",
        "发现问题",
        "处置措施",
        "任务状态",
    ],
    required_fields=[
        "任务编号",
        "巡检站点",
        "巡检人员",
    ],
    status_order=[
        "待巡检",
        "巡检中",
        "已巡检",
        "待复查",
    ],
    action_rules={"开始巡检": "巡检中", "提交巡检": "已巡检", "发起复查": "待复查"},
    negative_actions=[],
)
