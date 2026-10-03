"""蓄电池组模块声明：只描述字段、状态与动作，逻辑走 services.base 的共用实现。"""
from __future__ import annotations

from app.services.base import ModuleSpec

SPEC = ModuleSpec(
    name="battery",
    label="蓄电池组",
    noun="蓄电池组",
    keyword_field="电池组编号",
    list_fields=[
        "电池组编号",
        "电池类型",
        "额定容量",
        "所属站点",
        "放电时长",
        "内阻值",
        "投用日期",
        "电池状态",
    ],
    required_fields=[
        "电池组编号",
        "电池类型",
        "额定容量",
    ],
    status_order=[
        "容量合格",
        "容量下降",
        "需更换",
        "已更换",
    ],
    action_rules={"记录下降": "容量下降", "安排更换": "需更换", "完成更换": "已更换"},
    negative_actions=[],
)
