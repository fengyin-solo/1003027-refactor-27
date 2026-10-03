"""消防设施模块声明：只描述字段、状态与动作，逻辑走 services.base 的共用实现。"""
from __future__ import annotations

from app.services.base import ModuleSpec

SPEC = ModuleSpec(
    name="firealarm",
    label="消防设施",
    noun="消防设施",
    keyword_field="设施编号",
    list_fields=[
        "设施编号",
        "设施类型",
        "所属站点",
        "灭火剂量",
        "上次检查",
        "有效期至",
        "检查人员",
        "设施状态",
    ],
    required_fields=[
        "设施编号",
        "设施类型",
        "所属站点",
    ],
    status_order=[
        "合格",
        "压力不足",
        "已过期",
        "已更换",
    ],
    action_rules={"登记不足": "压力不足", "登记过期": "已过期", "安排更换": "已更换"},
    negative_actions=[],
)
