#插件1
from howfo.plugins import Plugins

class Plugin1(Plugins):
    def __init__(self):
        pass

    #实现接入点的接口
    def Start(self):
        print "I am plugin1 , I am a menu!"