1. 在zenoss上安装zenpacks
zenpack --install ZenPacks.community.SMART

2. 在目标机器上，把script/smartmon复制到/opt下，在root用户或者/etc/crontab里加入

*/5 * * * * (/bin/sh /opt/smartmon/smartmon.sh)

smartmon.sh负责在/var/cache/snmp/中生成类似smart-health-sda的文件。

3. 在/etc/snmp/snmpd.conf中加入

extend  smartHealth /opt/smartmon/smart-health
extend  smartDeviceDescr /opt/smartmon/smart-health DeviceDescr 
extend  smartDeviceIndex /opt/smartmon/smart-health Index

smart-health读取/var/cache/snmp/smart-health-*，并分析后返回结果，以符合snmp扩展标准。

