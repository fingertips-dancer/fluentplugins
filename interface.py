import threading
from typing import Callable
from typing import Dict
from types import ModuleType

__interfaces__ = {}
IS_SINGLE = "isSingle"
INTERFACES = "interfaces"


class Interface():
    """ 接口"""

    def __init__(self, 
                 spec: Callable, 
                 isSingle: bool,
                 isOnlyResult: bool,
                 isAsync: bool):
        self.__spec = spec
        self.__isSingle = isSingle
        self.__isOnlyResult = isOnlyResult
        self.__isAsync = isAsync
        self.__hookimpls = []

    def __call__(self, *args, **kwargs):
        # 没有实现
        if len(self.__hookimpls) == 0: return []

        # 异步
        if self.__isAsync:
            for hm in self.__hookimpls:
                t = threading.Thread(target=hm, args=args, kwargs=kwargs)
                t.daemon = True
                t.start()
        else:
            rs = []
            for hm in self.__hookimpls:
                r = hm(*args, **kwargs)
                rs.append(r)
                # 返回单一结果
                if r and self.__isOnlyResult:
                    return r
            # 返回单一结果
            if self.__isSingle:
                return rs[0]
            return rs

    def register(self, hookimpl):
        """接口函数登记"""
        if self.__isSingle:
            assert len(self.__hookimpls) == 0, \
                "This hook was registered with only one implementation allowed, " \
                "but it was detected that the second implementation had been added"
        if hookimpl not in self.__hookimpls:
            self.__hookimpls.append(hookimpl)
        return hookimpl

    def unregister(self, hookimpl):
        if hookimpl in self.__hookimpls:
            self.__hookimpls.remove(hookimpl)

    def unloadPlugin(self,pluginName:str):
        """ 卸载一个插件, 该插件对这个接口的实现都将被卸载 """
        for hookimpl in self.__hookimpls.copy():
            if hookimpl.__module__.split(".")[-1] == pluginName:
                self.unregister(hookimpl)


    def unloadModule(self, module: ModuleType):
        """ 卸载一个 模块(module), 该模块(module)对这个接口的实现都将被卸载 """
        for hookimpl in self.__hookimpls.copy():
            if hookimpl.__module__ == module.__name__:
                self.unregister(hookimpl)
           
if __name__ == "__main__":
    # 定义的接口
    @interfaceHookspec()
    def interface1(t1, t2, t3) -> Dict:
        """
        :param t1:
        :param t2:
        :param t3:
        :return:
        """


    # 接口的实现
    @interface1.register
    def interface2(t1, t2, t3) -> Dict:
        print("t1", t1, "t2", t2, "t3", t3, )
        return {"test2": 2}


    @interface1.register
    def interface3(t1, t2, t3) -> Dict:
        print("t1", t1, "t2", t2, "t3", t3, )
        return {"test3": 3}


    r = interface1(1, t2=3, t3=3)
    print(r)


    class Test():
        @interfaceHookspec()
        @staticmethod
        def interface4(t1, t2, t3) -> Dict:
            """
            :param t1:
            :param t2:
            :param t3:
            :return:
            """

        @interfaceHookspec()
        def interface5(self, t1, t2, t3) -> Dict:
            """
            :param t1:
            :param t2:
            :param t3:
            :return:
            """


    test = Test()


    # 接口的实现
    @Test.interface4.register
    def interface2(t1, t2, t3) -> Dict:
        print("t1", t1, "t2", t2, "t3", t3, )
        return {"test2": 2}


    @test.interface5.register
    def interface5(t1, t2, t3) -> Dict:
        print("t1", t1, "t2", t2, "t3", t3, )
        return {"interface5": "interface5"}


    r: interface5 = interface3(t1=1, t2=3, t3=3)
