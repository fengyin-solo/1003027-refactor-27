"""场租合同模块声明：只描述字段、状态与动作，逻辑走 services.base 的共用实现。"""
from __future__ import annotations

from app.services.base import ModuleSpec

SPEC = ModuleSpec(
    name="rental",
    label="场租合同",
    noun="场租合同",
    keyword_field="合同编号",
    list_fields=[
        "合同编号",
        "站点名称",
        "出租方",
        "年租金",
        "签约日期",
        "到期日期",
        "续租条款",
        "合同状态",
    ],
    required_fields=[
        "合同编号",
        "站点名称",
        "出租方",
    ],
    status_order=[
        "执行中",
        "即将到期",
        "续租中",
        "已到期",
    ],
    action_rules={"登记到期": "即将到期", "申请续租": "续租中", "确认到期": "已到期"},
    negative_actions=[],
)
