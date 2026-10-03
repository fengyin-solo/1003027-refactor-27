"""门禁管理模块声明：只描述字段、状态与动作，逻辑走 services.base 的共用实现。"""
from __future__ import annotations

from app.services.base import ModuleSpec

SPEC = ModuleSpec(
    name="dooraccess",
    label="门禁管理",
    noun="门禁记录",
    keyword_field="门禁编号",
    list_fields=[
        "门禁编号",
        "所属站点",
        "开门方式",
        "进出人员",
        "进出时间",
        "授权状态",
        "异常记录",
        "门禁状态",
    ],
    required_fields=[
        "门禁编号",
        "所属站点",
        "开门方式",
    ],
    status_order=[
        "正常",
        "授权过期",
        "非法闯入",
        "已修复",
    ],
    action_rules={"续期授权": "授权过期", "记录闯入": "非法闯入", "修复门禁": "已修复"},
    negative_actions=[],
)
