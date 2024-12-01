import os,sys
from types import ModuleType
from typing import List, Callable

from .interface import Interface


class PluginManaer():
    def __init__(self):
        self.__pluginDir__: List[str] = []
        self.__plugins__: List[ModuleType] = []
        self.__interfaces__: List[Interface] = []

    def registerPluginDirPath(self, path) -> None:
        """
        登记一个plugin文件夹路径,其中的子文件都会被认为的plugin
        :param path: 路径
        """
        # 相对路径 -> 标准路径
        path = os.path.abspath(path)
        # 项目路径
        script_path = os.getcwd()
        # 如果在项目路径内
        if len(path) >= len(script_path) and path[:len(script_path)] == script_path:
            # 将绝对路径转换为相对于起始路径的相对路径
            relative_path = os.path.relpath(path, script_path)
            self.__pluginDir__.append(relative_path)
        else:
            self.__pluginDir__.append(path)

    def _import_plugin_a_module(self, module: str):
        """ import (considerate whether it need to reload)"""
        import importlib
        # 1. the module have been imported
        if module in sys.modules:
            module = importlib.reload(sys.modules[module])
        # 2.the module never been imported
        else:
            module = importlib.import_module(module)
        self.__plugins__.append(module)

    def _importPluginModule(self, module: str, libPath:str):
        """ import """
        # 是否存在
        if module in os.listdir(libPath):
            # 绝对路径
            if not os.path.isabs(libPath):
                self._import_plugin_a_module(module=libPath.replace(os.sep, ".") + "." + module)
                return
            # 绝对路径
            else:
                # 将路径添加到根路径
                # 将特定路径添加到模块搜索路径中
                if pluginDir not in sys.path: sys.path.insert(0, module)
                # import
                self._import_plugin_a_module(module=module)
                return
        raise Exception("the plugin is not exists")

    def loadPlugin(self, pluginName: str):
        """ 加载一个插件 """
        import os, sys
        for pluginDir in self.__pluginDir__:
            # 相对路径
            if pluginName in os.listdir(pluginDir):
                self._importPluginModule(module=pluginName,libPath=pluginDir)
                return
        else:
            raise Exception("the plugin is not exists")

    def unloadPlugin(self, pluginName: str):
        """ 卸载一个插件 """
        # 1. 卸载 plugin 的 登记
        for plugin in self.__plugins__:
            # 1.1 获取名字
            # 1.2 可能是相对路径的导入
            _pluginName = plugin.__name__.split(".")[-1]
            if _pluginName == pluginName:
                self.__plugins__.remove(plugin)
                break
        else:
            raise Exception(f"the plugin<{pluginName}> is not exists")

        # 2. 将接口的实现卸载
        for interface in self.__interfaces__:
            interface.unloadModule(plugin)


    def loadAllPlugins(self):
        """ 加载全部插件 """
        import os, sys
        # 文件夹
        for pluginDir in self.__pluginDir__:
            for pluginName in os.listdir(pluginDir):
                self._importPluginModule(module=pluginName, libPath=pluginDir)
    def interfaceHookspec(self,
                          isSingle: bool = False,
                          isOnlyResult: bool = False,
                          isAsync: bool = False) -> Callable:
        """
        reigster a plugin hookspec
        :param interface: interface
        :param isSingle:
            Is it only a func for the interface
            是否只允许一个函数进行响应,如果True,装饰函数只会允许一个接口函数响应
        :param isOnlyResult:
            只获取一个结果,尽可能执行更多的function,遇到 not None 时结束执行
        :param isAsync:
            是否异步,如果设置为True,将不会有返回值
        :return:
        """

        def wapper(spec: Callable) -> Interface:
            interface = Interface(spec=spec,
                                  isOnlyResult=isOnlyResult,
                                  isSingle=isSingle,
                                  isAsync=isAsync)
            self.__interfaces__.append(interface)
            return interface

        return wapper

    def allPlugins(self, loaded: bool = False):
        """
        all plugins in paths reigisted
        :param loaded: Does it return only plugin loaded
        :return: 
        """
        if loaded:
            return self.__plugins__

        plugins = []
        # 文件夹
        for pluginDir in self.__pluginDir__:
            plugins += [{"module": plugin_name, "from": pluginDir} for plugin_name in os.listdir(pluginDir)]
        return plugins


__inner_plugin_manager__ = PluginManaer()
registerPluginDirPath = __inner_plugin_manager__.registerPluginDirPath
loadAllPlugins = __inner_plugin_manager__.loadAllPlugins
interfaceHookspec = __inner_plugin_manager__.interfaceHookspec

if __name__ == "__main__":
    registerPluginDirPath(path="./plugin")
    registerPluginDirPath(path="E:\study\project\mylib")
    # print(__pluginDir__)
