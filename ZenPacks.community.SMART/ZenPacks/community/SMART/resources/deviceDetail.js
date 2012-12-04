/*
###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2010, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################
*/

(function(){

var ZC = Ext.ns('Zenoss.component');


ZC.HardDiskPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'HardDisk',
            autoExpandColumn: 'title',
            fields: [
                {name: 'uid'},
                {name: 'severity'},            
                {name: 'status'},
                {name: 'title'},
                {name: 'hasMonitor'},
                {name: 'monitor'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'title',
                dataIndex: 'title',
                header: _t('Name')
            },{
                id: 'monitor',
                dataIndex: 'monitor',
                header: _t('Monitored'),
                renderer: Zenoss.render.monitor,
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status')
            }]
        });
        ZC.HardDiskPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('HardDiskPanel', ZC.HardDiskPanel);
ZC.registerName('HardDisk', _t('Hard Disk'), _t('Hard Disks'));
})();
