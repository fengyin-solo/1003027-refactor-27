"""馈线巡检模块声明：只描述字段、状态与动作，逻辑走 services.base 的共用实现。"""
from __future__ import annotations

from app.services.base import ModuleSpec

SPEC = ModuleSpec(
    name="feeder",
    label="馈线巡检",
    noun="馈线",
    keyword_field="馈线编号",
    list_fields=[
        "馈线编号",
        "所属站点",
        "馈线长度",
        "接头数量",
        "防水情况",
        "接地电阻",
        "巡检日期",
        "馈线状态",
    ],
    required_fields=[
        "馈线编号",
        "所属站点",
        "馈线长度",
    ],
    status_order=[
        "正常",
        "防水失效",
        "接地超标",
        "已修复",
    ],
    action_rules={"登记失效": "防水失效", "登记超标": "接地超标", "安排修复": "已修复"},
    negative_actions=[],
)
