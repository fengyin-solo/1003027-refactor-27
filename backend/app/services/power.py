"""动力配套模块声明：只描述字段、状态与动作，逻辑走 services.base 的共用实现。"""
from __future__ import annotations

from app.services.base import ModuleSpec

SPEC = ModuleSpec(
    name="power",
    label="动力配套",
    noun="电源设备",
    keyword_field="设备编号",
    list_fields=[
        "设备编号",
        "设备类型",
        "额定功率",
        "所属站点",
        "投用日期",
        "上次检修",
        "下次检修日",
        "设备状态",
    ],
    required_fields=[
        "设备编号",
        "设备类型",
        "额定功率",
    ],
    status_order=[
        "正常运行",
        "降额运行",
        "故障停机",
        "已报废",
    ],
    action_rules={"降额运行": "降额运行", "故障停机": "故障停机", "申请报废": "已报废"},
    negative_actions=[],
)
