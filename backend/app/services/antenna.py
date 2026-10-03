"""天馈系统模块声明：只描述字段、状态与动作，逻辑走 services.base 的共用实现。"""
from __future__ import annotations

from app.services.base import ModuleSpec

SPEC = ModuleSpec(
    name="antenna",
    label="天馈系统",
    noun="天馈设备",
    keyword_field="天馈编号",
    list_fields=[
        "天馈编号",
        "天线类型",
        "工作频段",
        "所属站点",
        "挂高",
        "方位角",
        "驻波比",
        "天馈状态",
    ],
    required_fields=[
        "天馈编号",
        "天线类型",
        "工作频段",
    ],
    status_order=[
        "正常",
        "驻波异常",
        "下倾偏移",
        "已调整",
    ],
    action_rules={"记录异常": "驻波异常", "记录偏移": "下倾偏移", "安排调整": "已调整"},
    negative_actions=[],
)
