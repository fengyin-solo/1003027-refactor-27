"""油料管理模块声明：只描述字段、状态与动作，逻辑走 services.base 的共用实现。"""
from __future__ import annotations

from app.services.base import ModuleSpec

SPEC = ModuleSpec(
    name="fuel",
    label="油料管理",
    noun="油料记录",
    keyword_field="记录编号",
    list_fields=[
        "记录编号",
        "所属站点",
        "油料类型",
        "调入量",
        "当前存量",
        "发电消耗",
        "油料日期",
        "油料状态",
    ],
    required_fields=[
        "记录编号",
        "所属站点",
        "油料类型",
    ],
    status_order=[
        "储备充足",
        "油量偏低",
        "需补油",
        "已补充",
    ],
    action_rules={"记录消耗": "油量偏低", "申请补油": "需补油", "完成补油": "已补充"},
    negative_actions=[],
)
