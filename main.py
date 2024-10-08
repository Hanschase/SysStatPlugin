from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.command.operator import operator_class,CommandOperator
from pkg.command import operator, entities, cmdmgr, errors
from pkg.plugin.events import *

import os
import psutil


# 注册命令
@operator_class(name="sys", help ="查看系统状态", usage="!cmd 或者 !sysstat")
class SysStatcmd(CommandOperator):
    """
    注册插件说明而已，实现还是靠插件实现
    """
    async def execute(
            self,
            context: entities.ExecuteContext
    ):
        pass
# 注册插件
@register(name="SysStat", description="查看系统状态(原作者：RockChinQ，Hanschase修改版)", version="0.1", author="Hanshcase")
class SysStatPlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        pass

    @handler(PersonCommandSent)
    @handler(GroupCommandSent)
    async def command_send(self, ctx: EventContext):
        if ctx.event.command == "sysstat" or ctx.event.command == "sys":
            ctx.prevent_default()
            ctx.prevent_postorder()
            core_mem = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
            sysmem_info = psutil.virtual_memory()
            cpu_info = psutil.cpu_times
            disk_info = psutil.disk_usage('/')
            cpu_ststs = psutil.cpu_stats()
            cpu_freq = psutil.cpu_freq()
            
            res = f"""====系统状态====
进程内存占用: {core_mem:.2f}MB
总内存: {sysmem_info.total / 1024 / 1024:.2f}MB
已用内存: {sysmem_info.used / 1024 / 1024:.2f}MB
空闲内存: {sysmem_info.free / 1024 / 1024:.2f}MB
内存使用率: {sysmem_info.percent:.2f}%
CPU使用率: {psutil.cpu_percent(interval=1):.2f}%
总磁盘空间: {disk_info.total / 1024 / 1024 / 1024:.2f}GB
已用磁盘空间: {disk_info.used / 1024 / 1024 / 1024:.2f}GB
空闲磁盘空间: {disk_info.free / 1024 / 1024 / 1024:.2f}GB
磁盘使用率: {disk_info.percent:.2f}%
============"""

            ctx.add_return("reply",[res.strip()])

    # 插件卸载时触发
    def __del__(self):
        pass
