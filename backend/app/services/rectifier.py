"""开关电源模块声明：只描述字段、状态与动作，逻辑走 services.base 的共用实现。"""
from __future__ import annotations

from app.services.base import ModuleSpec

SPEC = ModuleSpec(
    name="rectifier",
    label="开关电源",
    noun="开关电源",
    keyword_field="电源编号",
    list_fields=[
        "电源编号",
        "额定功率",
        "所属站点",
        "整流模块数",
        "负载率",
        "输出电压",
        "模块故障",
        "电源状态",
    ],
    required_fields=[
        "电源编号",
        "额定功率",
        "所属站点",
    ],
    status_order=[
        "正常",
        "模块缺失",
        "输出异常",
        "已更换",
    ],
    action_rules={"记录缺失": "模块缺失", "记录异常": "输出异常", "安排更换": "已更换"},
    negative_actions=[],
)
