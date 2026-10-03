"""应急通信模块声明：只描述字段、状态与动作，逻辑走 services.base 的共用实现。"""
from __future__ import annotations

from app.services.base import ModuleSpec

SPEC = ModuleSpec(
    name="emergency",
    label="应急通信",
    noun="应急保障",
    keyword_field="保障编号",
    list_fields=[
        "保障编号",
        "保障类型",
        "保障地点",
        "通信车编号",
        "保障人员",
        "到达时间",
        "撤离时间",
        "保障状态",
    ],
    required_fields=[
        "保障编号",
        "保障类型",
        "保障地点",
    ],
    status_order=[
        "待响应",
        "响应中",
        "保障中",
        "已撤离",
    ],
    action_rules={"启动响应": "响应中", "调派车辆": "保障中", "撤离保障": "已撤离"},
    negative_actions=[],
)
