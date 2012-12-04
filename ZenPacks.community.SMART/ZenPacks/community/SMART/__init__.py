
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.DeviceHW import DeviceHW
from Products.ZenRelations.RelSchema import *
DeviceHW._relations += (("smartes", ToManyCont(ToOne, "ZenPacks.community.SMART.HardDisk", "hw")), )

from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenUtils.ZenScriptBase import ZenScriptBase

class ZenPack(ZenPackBase):
    """ ZenPack loader
    """
    def install(self, app):
        ZenPackBase.install(self, app)
        self._buildRelations()
        self._setupCollectorPlugins(app.zport.dmd)

    def upgrade(self, app):
        ZenPackBase.upgrade(self, app)
        self._buildRelations()
        self._setupCollectorPlugins(app.zport.dmd)
        
    def remove(self, app, junk):
        self._cleanupOurPlugins(app.zport.dmd)
        ZenPackBase.remove(self, app, junk)
        DeviceHW._relations = tuple([x for x in DeviceHW._relations if x[0] not in ['smartes',]])
        self._buildRelations()
    
    def _buildRelations(self):
        for d in self.dmd.Devices.getSubDevices():
            d.hw.buildRelations()

    def _setupCollectorPlugins(self, dmd):

        def addPlugins(obj):
            if obj.hasProperty('zCollectorPlugins'):
                newPlugins = []
                for plugin in obj.zCollectorPlugins:
                    newPlugins.append(plugin)
                    if plugin == 'zenoss.snmp.DeviceMap':
                        newPlugins.append('SMARTMap')

                obj.zCollectorPlugins = newPlugins

        if hasattr(dmd.Devices, 'Server'):
#            addPlugins(dmd.Devices.Server)
            if hasattr(dmd.Devices.Server, 'Linux'):
                addPlugins(dmd.Devices.Server.Linux)
#            if hasattr(dmd.Devices.Server, 'Windows'):
#                addPlugins(dmd.Devices.Server.Windows)

    def _cleanupCollectorPlugins(self, dmd, plugin_list):
        obj_list = [dmd.Devices] + dmd.Devices.getSubOrganizers() + \
                dmd.Devices.getSubDevices()

        for thing in obj_list:
            if not thing.hasProperty('zCollectorPlugins'): continue
            newPlugins = []
            for plugin in thing.zCollectorPlugins:
                if plugin in plugin_list:
                    continue
                newPlugins.append(plugin)
            thing.zCollectorPlugins = newPlugins

    def _cleanupOurPlugins(self, dmd):
        self._cleanupCollectorPlugins(dmd, ('SMARTMap'))
        
        