1. ��zenoss�ϰ�װzenpacks
zenpack --install ZenPacks.community.SMART

2. ��Ŀ������ϣ���script/smartmon���Ƶ�/opt�£���root�û�����/etc/crontab�����

*/5 * * * * (/bin/sh /opt/smartmon/smartmon.sh)

smartmon.sh������/var/cache/snmp/����������smart-health-sda���ļ���

3. ��/etc/snmp/snmpd.conf�м���

extend  smartHealth /opt/smartmon/smart-health
extend  smartDeviceDescr /opt/smartmon/smart-health DeviceDescr 
extend  smartDeviceIndex /opt/smartmon/smart-health Index

smart-health��ȡ/var/cache/snmp/smart-health-*���������󷵻ؽ�����Է���snmp��չ��׼��

