INSTALL
1. in the machine where zenoss is installed
zenpack --install ZenPacks.community.SMART

2. in the target machine which is monitored
copy script/smartmon to /opt, and add the following line in /etc/crontab or crontab of root's.

*/5 * * * * (/bin/sh /opt/smartmon/smartmon.sh)

smartmon.sh will generate files like smart-health-sda in /var/cache/snmp/

3. open /etc/snmp/snmpd.conf, and add the following lines

extend  smartHealth /opt/smartmon/smart-health
extend  smartDeviceDescr /opt/smartmon/smart-health DeviceDescr 
extend  smartDeviceIndex /opt/smartmon/smart-health Index

smart-health will read files /var/cache/snmp/smart-health-*, analyze content and return result, which is according to snmp standards.

