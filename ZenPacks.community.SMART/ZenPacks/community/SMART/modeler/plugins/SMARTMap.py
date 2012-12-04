###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2007, 2009 Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

__doc__ = """SMARTMap

SMARTMap maps the phisical device to objects

"""

import re

from Products.ZenUtils.Utils import unsigned
from Products.DataCollector.plugins.DataMaps import ObjectMap
from Products.DataCollector.plugins.CollectorPlugin \
    import SnmpPlugin, GetTableMap

class SMARTMap(SnmpPlugin):

    maptype = "SMARTMap"
    compname = "hw"
    relname = "smartes"
    modname = "ZenPacks.community.SMART.HardDisk"
    deviceProperties = SnmpPlugin.deviceProperties + (
      'zSMARTMapIgnoreNames', 'zSMARTMapIgnoreTypes')

    snmpGetTableMaps = (
        GetTableMap('smTable', '.1.3.6.1.4.1.8072.1.3.2.4.1.2', 
        {
         '.16.115.109.97.114.116.68.101.118.105.99.101.73.110.100.101.120': 'snmpindex',
         '.16.115.109.97.114.116.68.101.118.105.99.101.68.101.115.99.114': 'title'}
         #'.11.115.109.97.114.116.72.101.97.108.116.104' : 'status',
         ),
    )


    def process(self, device, results, log):
        """Process SNMP information from this device"""
        log.info('Modeler %s processing data for device %s', self.name(), device.id)
        getdata, tabledata = results
        log.debug("%s tabledata = %s", device.id, tabledata)
        smtable = tabledata.get("smTable")
        if smtable is None:
            log.error("Unable to get data for %s from smTable"
                          " -- skipping model" % device.id)
            return None

        skipfsnames = getattr(device, 'zSMARTMapIgnoreNames', None)
        skipfstypes = getattr(device, 'zSMARTMapIgnoreTypes', None)
        maps = []
        rm = self.relMap()
        for sm in smtable.values():
            om = self.objectMap(sm)
            om.id = self.prepId(om.title)
            log.info("SMARTMap %s, %s", device.id, str(om))
            rm.append(om)
        maps.append(rm)
        return maps


