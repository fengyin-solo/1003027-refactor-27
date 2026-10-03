"""防雷接地模块声明：只描述字段、状态与动作，逻辑走 services.base 的共用实现。"""
from __future__ import annotations

from app.services.base import ModuleSpec

SPEC = ModuleSpec(
    name="lightningprot",
    label="防雷接地",
    noun="防雷装置",
    keyword_field="装置编号",
    list_fields=[
        "装置编号",
        "所属站点",
        "接地电阻",
        "防雷模块",
        "浪涌保护",
        "上次测试",
        "测试人员",
        "装置状态",
    ],
    required_fields=[
        "装置编号",
        "所属站点",
        "接地电阻",
    ],
    status_order=[
        "合格",
        "电阻超标",
        "模块劣化",
        "已更换",
    ],
    action_rules={"记录超标": "电阻超标", "记录劣化": "模块劣化", "安排更换": "已更换"},
    negative_actions=[],
)
