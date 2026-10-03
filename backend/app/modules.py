"""业务模块声明：每个模块只登记自己用到的字段、状态序列与动作规则。

接口与业务逻辑的共用实现分别在 app/routers/base.py 和 app/services/base.py，
模块之间的差异全部收敛到这里；新增模块时加一条 ModuleSpec 即可，不用再抄一遍结构。
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ModuleSpec:
    """一个业务模块的声明：路由、校验、状态流转都按这份声明生成。"""

    name: str  # 模块键，同时用于路由前缀与存储表名，如 "site"
    label: str  # 模块中文名，如 "基站台账"
    entity: str  # 单条记录的中文名，如 "基站"
    list_fields: list[str]  # 列表与导出展示的字段
    required_fields: list[str]  # 提交时必查的字段（校验口径）
    status_order: list[str]  # 允许的状态序列
    action_rules: dict[str, str]  # 动作 -> 目标状态
    negative_actions: list[str] = field(default_factory=list)  # 执行后计入异常的动作

    @property
    def keyword_field(self) -> str:
        """关键字检索命中的字段：各模块都取第一个必填字段（编号）。"""
        return self.required_fields[0]


MODULES: list[ModuleSpec] = [
    ModuleSpec(
        name="site",
        label="基站台账",
        entity="基站",
        list_fields=["基站编号", "基站名称", "基站类型", "所属区县", "经纬度坐标", "铁塔高度", "入网日期", "基站状态"],
        required_fields=["基站编号", "基站名称", "基站类型"],
        status_order=["运行中", "退服中", "已退网", "已拆除"],
        action_rules={"登记退服": "退服中", "申请退网": "已退网", "拆站完成": "已拆除"},
    ),
    ModuleSpec(
        name="tower",
        label="铁塔管理",
        entity="铁塔",
        list_fields=["铁塔编号", "铁塔类型", "设计高度", "平台数量", "所属站点", "建成年份", "上次检测", "铁塔状态"],
        required_fields=["铁塔编号", "铁塔类型", "设计高度"],
        status_order=["正常", "倾斜超标", "锈蚀", "已拆除"],
        action_rules={"登记倾斜": "倾斜超标", "防腐处理": "锈蚀", "拆塔完成": "已拆除"},
    ),
    ModuleSpec(
        name="power",
        label="动力配套",
        entity="电源设备",
        list_fields=["设备编号", "设备类型", "额定功率", "所属站点", "投用日期", "上次检修", "下次检修日", "设备状态"],
        required_fields=["设备编号", "设备类型", "额定功率"],
        status_order=["正常运行", "降额运行", "故障停机", "已报废"],
        action_rules={"降额运行": "降额运行", "故障停机": "故障停机", "申请报废": "已报废"},
    ),
    ModuleSpec(
        name="battery",
        label="蓄电池组",
        entity="蓄电池组",
        list_fields=["电池组编号", "电池类型", "额定容量", "所属站点", "放电时长", "内阻值", "投用日期", "电池状态"],
        required_fields=["电池组编号", "电池类型", "额定容量"],
        status_order=["容量合格", "容量下降", "需更换", "已更换"],
        action_rules={"记录下降": "容量下降", "安排更换": "需更换", "完成更换": "已更换"},
    ),
    ModuleSpec(
        name="genset",
        label="发电机组",
        entity="发电机组",
        list_fields=["机组编号", "机组型号", "额定功率", "所属站点", "上次试机", "油量储备", "启动状态", "机组状态"],
        required_fields=["机组编号", "机组型号", "额定功率"],
        status_order=["待命", "发电中", "故障", "维修中"],
        action_rules={"启动发电": "发电中", "关闭机组": "待命", "登记故障": "维修中"},
    ),
    ModuleSpec(
        name="rectifier",
        label="开关电源",
        entity="开关电源",
        list_fields=["电源编号", "额定功率", "所属站点", "整流模块数", "负载率", "输出电压", "模块故障", "电源状态"],
        required_fields=["电源编号", "额定功率", "所属站点"],
        status_order=["正常", "模块缺失", "输出异常", "已更换"],
        action_rules={"记录缺失": "模块缺失", "记录异常": "输出异常", "安排更换": "已更换"},
    ),
    ModuleSpec(
        name="ac",
        label="空调管理",
        entity="空调",
        list_fields=["空调编号", "空调类型", "制冷量", "所属站点", "运行电流", "设定温度", "回风温度", "空调状态"],
        required_fields=["空调编号", "空调类型", "制冷量"],
        status_order=["正常", "制冷不足", "压缩机故障", "已更换"],
        action_rules={"登记不足": "制冷不足", "登记故障": "压缩机故障", "安排更换": "已更换"},
    ),
    ModuleSpec(
        name="antenna",
        label="天馈系统",
        entity="天馈设备",
        list_fields=["天馈编号", "天线类型", "工作频段", "所属站点", "挂高", "方位角", "驻波比", "天馈状态"],
        required_fields=["天馈编号", "天线类型", "工作频段"],
        status_order=["正常", "驻波异常", "下倾偏移", "已调整"],
        action_rules={"记录异常": "驻波异常", "记录偏移": "下倾偏移", "安排调整": "已调整"},
    ),
    ModuleSpec(
        name="transmission",
        label="传输设备",
        entity="传输设备",
        list_fields=["设备编号", "传输类型", "带宽容量", "所属站点", "光口状态", "电口状态", "误码率", "设备状态"],
        required_fields=["设备编号", "传输类型", "带宽容量"],
        status_order=["正常", "光口告警", "误码超标", "已修复"],
        action_rules={"记录告警": "光口告警", "记录误码": "误码超标", "安排修复": "已修复"},
    ),
    ModuleSpec(
        name="feeder",
        label="馈线巡检",
        entity="馈线",
        list_fields=["馈线编号", "所属站点", "馈线长度", "接头数量", "防水情况", "接地电阻", "巡检日期", "馈线状态"],
        required_fields=["馈线编号", "所属站点", "馈线长度"],
        status_order=["正常", "防水失效", "接地超标", "已修复"],
        action_rules={"登记失效": "防水失效", "登记超标": "接地超标", "安排修复": "已修复"},
    ),
    ModuleSpec(
        name="lightningprot",
        label="防雷接地",
        entity="防雷装置",
        list_fields=["装置编号", "所属站点", "接地电阻", "防雷模块", "浪涌保护", "上次测试", "测试人员", "装置状态"],
        required_fields=["装置编号", "所属站点", "接地电阻"],
        status_order=["合格", "电阻超标", "模块劣化", "已更换"],
        action_rules={"记录超标": "电阻超标", "记录劣化": "模块劣化", "安排更换": "已更换"},
    ),
    ModuleSpec(
        name="firealarm",
        label="消防设施",
        entity="消防设施",
        list_fields=["设施编号", "设施类型", "所属站点", "灭火剂量", "上次检查", "有效期至", "检查人员", "设施状态"],
        required_fields=["设施编号", "设施类型", "所属站点"],
        status_order=["合格", "压力不足", "已过期", "已更换"],
        action_rules={"登记不足": "压力不足", "登记过期": "已过期", "安排更换": "已更换"},
    ),
    ModuleSpec(
        name="dooraccess",
        label="门禁管理",
        entity="门禁记录",
        list_fields=["门禁编号", "所属站点", "开门方式", "进出人员", "进出时间", "授权状态", "异常记录", "门禁状态"],
        required_fields=["门禁编号", "所属站点", "开门方式"],
        status_order=["正常", "授权过期", "非法闯入", "已修复"],
        action_rules={"续期授权": "授权过期", "记录闯入": "非法闯入", "修复门禁": "已修复"},
    ),
    ModuleSpec(
        name="patrol",
        label="巡检作业",
        entity="巡检任务",
        list_fields=["任务编号", "巡检站点", "巡检人员", "计划日期", "巡检路线", "发现问题", "处置措施", "任务状态"],
        required_fields=["任务编号", "巡检站点", "巡检人员"],
        status_order=["待巡检", "巡检中", "已巡检", "待复查"],
        action_rules={"开始巡检": "巡检中", "提交巡检": "已巡检", "发起复查": "待复查"},
    ),
    ModuleSpec(
        name="fuel",
        label="油料管理",
        entity="油料记录",
        list_fields=["记录编号", "所属站点", "油料类型", "调入量", "当前存量", "发电消耗", "油料日期", "油料状态"],
        required_fields=["记录编号", "所属站点", "油料类型"],
        status_order=["储备充足", "油量偏低", "需补油", "已补充"],
        action_rules={"记录消耗": "油量偏低", "申请补油": "需补油", "完成补油": "已补充"},
    ),
    ModuleSpec(
        name="rental",
        label="场租合同",
        entity="场租合同",
        list_fields=["合同编号", "站点名称", "出租方", "年租金", "签约日期", "到期日期", "续租条款", "合同状态"],
        required_fields=["合同编号", "站点名称", "出租方"],
        status_order=["执行中", "即将到期", "续租中", "已到期"],
        action_rules={"登记到期": "即将到期", "申请续租": "续租中", "确认到期": "已到期"},
    ),
    ModuleSpec(
        name="electricbill",
        label="电费管理",
        entity="电费记录",
        list_fields=["记录编号", "所属站点", "电表读数", "用电量", "电费金额", "缴费月份", "缴费状态", "票据编号"],
        required_fields=["记录编号", "所属站点", "电表读数"],
        status_order=["待缴费", "已缴费", "电费异常", "已核实"],
        action_rules={"缴纳电费": "已缴费", "登记异常": "电费异常", "核实确认": "已核实"},
    ),
    ModuleSpec(
        name="demolition",
        label="拆站管理",
        entity="拆站任务",
        list_fields=["任务编号", "拆除站点", "拆除原因", "拆除范围", "施工队伍", "计划工期", "物资回收", "任务状态"],
        required_fields=["任务编号", "拆除站点", "拆除原因"],
        status_order=["待审批", "已批复", "拆除中", "已拆除"],
        action_rules={"提交审批": "已批复", "开始拆除": "拆除中", "回收完成": "已拆除"},
    ),
    ModuleSpec(
        name="emergency",
        label="应急通信",
        entity="应急保障",
        list_fields=["保障编号", "保障类型", "保障地点", "通信车编号", "保障人员", "到达时间", "撤离时间", "保障状态"],
        required_fields=["保障编号", "保障类型", "保障地点"],
        status_order=["待响应", "响应中", "保障中", "已撤离"],
        action_rules={"启动响应": "响应中", "调派车辆": "保障中", "撤离保障": "已撤离"},
    ),
    ModuleSpec(
        name="energyeff",
        label="节能改造",
        entity="节能项目",
        list_fields=["项目编号", "所属站点", "改造内容", "预估节电率", "投资金额", "承包单位", "投资回收期", "项目状态"],
        required_fields=["项目编号", "所属站点", "改造内容"],
        status_order=["待立项", "改造中", "评估中", "已验收"],
        action_rules={"申请立项": "改造中", "开始改造": "评估中", "验收评估": "已验收"},
    ),
]

MODULES_BY_NAME: dict[str, ModuleSpec] = {spec.name: spec for spec in MODULES}
