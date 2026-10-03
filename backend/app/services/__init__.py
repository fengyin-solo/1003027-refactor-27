"""业务模块声明汇总：每个模块一份 SPEC，共用逻辑在 services.base。

按别名导入再汇总：模块名有可能和内置名撞车（某个业务模块就叫 dict、list
这种名字时），按名字直接 import 会把内置类型覆盖掉。
"""
from __future__ import annotations

from app.services import ac as spec_ac
from app.services import antenna as spec_antenna
from app.services import battery as spec_battery
from app.services import demolition as spec_demolition
from app.services import dooraccess as spec_dooraccess
from app.services import electricbill as spec_electricbill
from app.services import emergency as spec_emergency
from app.services import energyeff as spec_energyeff
from app.services import feeder as spec_feeder
from app.services import firealarm as spec_firealarm
from app.services import fuel as spec_fuel
from app.services import genset as spec_genset
from app.services import lightningprot as spec_lightningprot
from app.services import patrol as spec_patrol
from app.services import power as spec_power
from app.services import rectifier as spec_rectifier
from app.services import rental as spec_rental
from app.services import site as spec_site
from app.services import tower as spec_tower
from app.services import transmission as spec_transmission
from app.services.base import ModuleService, ModuleSpec

_SPEC_MODULES = [spec_site, spec_tower, spec_power, spec_battery, spec_genset, spec_rectifier, spec_ac, spec_antenna, spec_transmission, spec_feeder, spec_lightningprot, spec_firealarm, spec_dooraccess, spec_patrol, spec_fuel, spec_rental, spec_electricbill, spec_demolition, spec_emergency, spec_energyeff]

SPECS: dict[str, ModuleSpec] = {module.SPEC.name: module.SPEC for module in _SPEC_MODULES}
SERVICES: dict[str, ModuleService] = {name: ModuleService(spec) for name, spec in SPECS.items()}

__all__ = ["ModuleService", "ModuleSpec", "SERVICES", "SPECS"]
