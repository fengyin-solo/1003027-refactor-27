"""基站台账模块声明：只描述字段、状态与动作，逻辑走 services.base 的共用实现。"""
from __future__ import annotations

from app.services.base import ModuleSpec

SPEC = ModuleSpec(
    name="site",
    label="基站台账",
    noun="基站",
    keyword_field="基站编号",
    list_fields=[
        "基站编号",
        "基站名称",
        "基站类型",
        "所属区县",
        "经纬度坐标",
        "铁塔高度",
        "入网日期",
        "基站状态",
    ],
    required_fields=[
        "基站编号",
        "基站名称",
        "基站类型",
    ],
    status_order=[
        "运行中",
        "退服中",
        "已退网",
        "已拆除",
    ],
    action_rules={"登记退服": "退服中", "申请退网": "已退网", "拆站完成": "已拆除"},
    negative_actions=[],
)
