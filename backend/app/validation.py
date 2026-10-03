"""入参校验的唯一入口：全平台只在这里核对提交内容。

各业务模块不再各自抄一遍校验逻辑，只声明自己用到的字段；
校验口径（哪些字段必填、提交指纹怎么算）调整后，历史提交也按这里的实现重判。
"""
from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from typing import Any


def missing_required(values: Mapping[str, Any], required: Sequence[str]) -> list[str]:
    """按模块声明的必填字段核对提交内容，返回缺漏或空白的字段名。"""
    return [field for field in required if not str(values.get(field) or "").strip()]


def submission_fingerprint(values: Mapping[str, Any], fields: Sequence[str]) -> str:
    """把一份提交按声明字段规整成稳定指纹。

    同一份提交（声明字段逐一相同）指纹相同，重复提交时据此只落一次；
    空白差异（首尾空格、非字符串类型）不影响指纹。
    """
    canonical = {field: str(values.get(field) or "").strip() for field in fields}
    return json.dumps(canonical, ensure_ascii=False, sort_keys=True)
