"""铁塔管理模块声明：只描述字段、状态与动作，逻辑走 services.base 的共用实现。"""
from __future__ import annotations

from app.services.base import ModuleSpec

SPEC = ModuleSpec(
    name="tower",
    label="铁塔管理",
    noun="铁塔",
    keyword_field="铁塔编号",
    list_fields=[
        "铁塔编号",
        "铁塔类型",
        "设计高度",
        "平台数量",
        "所属站点",
        "建成年份",
        "上次检测",
        "铁塔状态",
    ],
    required_fields=[
        "铁塔编号",
        "铁塔类型",
        "设计高度",
    ],
    status_order=[
        "正常",
        "倾斜超标",
        "锈蚀",
        "已拆除",
    ],
    action_rules={"登记倾斜": "倾斜超标", "防腐处理": "锈蚀", "拆塔完成": "已拆除"},
    negative_actions=[],
)
