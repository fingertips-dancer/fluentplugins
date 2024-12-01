from fluentplugins import PluginManaer

manager = PluginManaer()


class PluginInterface():
    @manager.interfaceHookspec(isSingle=False, isOnlyResult=False, isAsync=False)
    def interface1(self, param1, param2):
        pass

    @manager.interfaceHookspec(isSingle=False, isOnlyResult=True, isAsync=False)
    def interface2(self, param1, param2):
        pass

    @manager.interfaceHookspec(isSingle=False, isOnlyResult=False, isAsync=True)
    def interface3(self, param1, param2):
        pass



if __name__ == "__main__":
    manager = PluginManaer()
