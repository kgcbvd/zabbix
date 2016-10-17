#!/usr/bin/python3
import os
import json
import sys

disks = os.popen("sg_map |awk '{print $1'}").read()
disks = disks.split("\n")
try:
        dev_type=sys.argv[1]
except IndexError:
        print('Use {0} dev_type'.format(sys.argv[0]))
        sys.exit(1)
data = []
for disk in disks:
        dev_name_type = {}
        if disk:
                if dev_type == 'sat':
                        line = "smartctl -d {0} -i -A {1} |grep -q 'ATA' > /dev/null".format(dev_type, disk)
                elif dev_type == 'scsi':
                        line = "smartctl -d {0} -i -A {1} |grep -q 'SAS' > /dev/null".format(dev_type, disk)
                else:
                        print("Please use dev_type scsi for SAS or sat for SATA")
                        sys.exit(1)
                exit_code = os.system(line)
                if not exit_code:
                        dev_name_type["{#DEVNAME}"] = disk
                        dev_name_type["{#DEVTYPE}"] = dev_type
                        data.append(dev_name_type)

print(json.dumps({"data": data}))
