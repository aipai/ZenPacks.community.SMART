#!/bin/sh

# update smart parameters
for devfull in /dev/sd?; do
    dev=`/bin/echo $devfull | /bin/sed 's/^.*\(sd.\)$/\1/'`
    /usr/sbin/smartctl -n idle -H $devfull >/var/cache/snmp/smart-health-$dev.TMP
    /bin/mv /var/cache/snmp/smart-health-$dev.TMP /var/cache/snmp/smart-health-$dev
done

