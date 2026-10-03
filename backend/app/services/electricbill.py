"""电费管理模块声明：只描述字段、状态与动作，逻辑走 services.base 的共用实现。"""
from __future__ import annotations

from app.services.base import ModuleSpec

SPEC = ModuleSpec(
    name="electricbill",
    label="电费管理",
    noun="电费记录",
    keyword_field="记录编号",
    list_fields=[
        "记录编号",
        "所属站点",
        "电表读数",
        "用电量",
        "电费金额",
        "缴费月份",
        "缴费状态",
        "票据编号",
    ],
    required_fields=[
        "记录编号",
        "所属站点",
        "电表读数",
    ],
    status_order=[
        "待缴费",
        "已缴费",
        "电费异常",
        "已核实",
    ],
    action_rules={"缴纳电费": "已缴费", "登记异常": "电费异常", "核实确认": "已核实"},
    negative_actions=[],
)
