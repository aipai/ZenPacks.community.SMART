from Globals import InitializeClass
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.HWComponent import *
from Products.ZenModel.ZenossSecurity import *
from cmath import *

SEV_CLEAN    = 0
SEV_DEBUG    = 1
SEV_INFO     = 2
SEV_WARNING  = 3
SEV_ERROR    = 4
SEV_CRITICAL = 5

import logging
log = logging.getLogger("zen.HardDisk")

def manage_addHardDisk(context, id, title = None, REQUEST = None):
    """make a filesystem"""
    hd = HardDisk(id, title)
    context._setObject(id, hd)
    hd = context._getOb(id)
    hd.index_object()

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()
                                     +'/manage_main') 

#addHardDisk = DTMLFile('dtml/addHardDisk',globals())

class HardDisk(HWComponent):
    status = 1
    portal_type = meta_type = 'HardDisk'
    
    _properties = HWComponent._properties + (
        {'id':'title', 'type':'string', 'mode':'w'},
        {'id':'status', 'type':'int', 'mode':'w'},
    )
    
    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont, "Products.ZenModel.DeviceHW", "smartes")),
        )
        
    statusmap ={
        0: 'OK',
        10: 'Debug',
        20: 'Other',
        30: 'No Data File',
        40: 'Warning',
        50: 'Device Failed',            
    }
    
    factory_type_information = (
        {
            'id'                : 'HardDisk',
            'meta_type'         : 'HardDisk',
            'description'       : """HardDisks""",
            'icon'              : 'HardDisk_icon.gif',
            'product'           : 'SMART',
            'factory'           : 'manage_addHardDiskSMART',
            'immediate_view'    : 'viewHardDiskSMART',
            'actions'           :
            (
                { 'id'          : 'status',
                  'name'        : 'Status',
                  'action'      : 'viewHardDiskSMART',
                  'permissions' : (ZEN_VIEW, )
                },
            )
        },
    )
    
    def statusSeverity(self, status=None):
        """
        Return the severity based on status
        0:'Clean', 1:'Debug', 2:'Info', 3:'Warning', 4:'Error', 5:'Critical'
        """
        if status is None: status = self.status
        return status/10
        
    def statusString(self, status=None):
        """
        Return the status string
        """
        if status is None: 
            status = self.status
        if status is None:
            return 'Unknown'

        if self.statusmap.has_key(status):
            return self.statusmap.get(status)
        else:
            status = (status/10)*10
            if self.statusmap.has_key(status):
                return self.statusmap.get(status)
            else:
                return 'Unknown'

    def getRRDNames(self):
        """ 
        Return the datapoint name of this filesystem 'usedBlocks_usedBlocks'
        """
        return ['health_health']
        
    def viewName(self):
        """
        Return the mount point name of a filesystem '/boot'
        """
        return self.title
    name = viewName
    
InitializeClass(HardDisk)
