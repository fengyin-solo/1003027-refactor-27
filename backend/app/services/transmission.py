"""传输设备模块声明：只描述字段、状态与动作，逻辑走 services.base 的共用实现。"""
from __future__ import annotations

from app.services.base import ModuleSpec

SPEC = ModuleSpec(
    name="transmission",
    label="传输设备",
    noun="传输设备",
    keyword_field="设备编号",
    list_fields=[
        "设备编号",
        "传输类型",
        "带宽容量",
        "所属站点",
        "光口状态",
        "电口状态",
        "误码率",
        "设备状态",
    ],
    required_fields=[
        "设备编号",
        "传输类型",
        "带宽容量",
    ],
    status_order=[
        "正常",
        "光口告警",
        "误码超标",
        "已修复",
    ],
    action_rules={"记录告警": "光口告警", "记录误码": "误码超标", "安排修复": "已修复"},
    negative_actions=[],
)
