"""节能改造模块声明：只描述字段、状态与动作，逻辑走 services.base 的共用实现。"""
from __future__ import annotations

from app.services.base import ModuleSpec

SPEC = ModuleSpec(
    name="energyeff",
    label="节能改造",
    noun="节能项目",
    keyword_field="项目编号",
    list_fields=[
        "项目编号",
        "所属站点",
        "改造内容",
        "预估节电率",
        "投资金额",
        "承包单位",
        "投资回收期",
        "项目状态",
    ],
    required_fields=[
        "项目编号",
        "所属站点",
        "改造内容",
    ],
    status_order=[
        "待立项",
        "改造中",
        "评估中",
        "已验收",
    ],
    action_rules={"申请立项": "改造中", "开始改造": "评估中", "验收评估": "已验收"},
    negative_actions=[],
)
