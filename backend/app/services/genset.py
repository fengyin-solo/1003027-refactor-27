"""发电机组模块声明：只描述字段、状态与动作，逻辑走 services.base 的共用实现。"""
from __future__ import annotations

from app.services.base import ModuleSpec

SPEC = ModuleSpec(
    name="genset",
    label="发电机组",
    noun="发电机组",
    keyword_field="机组编号",
    list_fields=[
        "机组编号",
        "机组型号",
        "额定功率",
        "所属站点",
        "上次试机",
        "油量储备",
        "启动状态",
        "机组状态",
    ],
    required_fields=[
        "机组编号",
        "机组型号",
        "额定功率",
    ],
    status_order=[
        "待命",
        "发电中",
        "故障",
        "维修中",
    ],
    action_rules={"启动发电": "发电中", "关闭机组": "待命", "登记故障": "维修中"},
    negative_actions=[],
)
