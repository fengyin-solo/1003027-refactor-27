"""空调管理模块声明：只描述字段、状态与动作，逻辑走 services.base 的共用实现。"""
from __future__ import annotations

from app.services.base import ModuleSpec

SPEC = ModuleSpec(
    name="ac",
    label="空调管理",
    noun="空调",
    keyword_field="空调编号",
    list_fields=[
        "空调编号",
        "空调类型",
        "制冷量",
        "所属站点",
        "运行电流",
        "设定温度",
        "回风温度",
        "空调状态",
    ],
    required_fields=[
        "空调编号",
        "空调类型",
        "制冷量",
    ],
    status_order=[
        "正常",
        "制冷不足",
        "压缩机故障",
        "已更换",
    ],
    action_rules={"登记不足": "制冷不足", "登记故障": "压缩机故障", "安排更换": "已更换"},
    negative_actions=[],
)
