#!venv/bin/python
import os
import psutil
import sys
import time
import json
from subprocess import Popen

pickup_stats = ['username', 'cpu_num', 'cpu_percent', 'cwd']

def proc_probe(ps_proc, log_entry):
    try:
        update_probe = ps_proc.as_dict(attrs=pickup_stats)
        log_entry['log_time'].append(time.time())
        for attr in pickup_stats:
            log_entry[attr].append(update_probe[attr])
    except psutil.NoSuchProcess as e:
        return False
    return True

def execute_command(cmd):
    proc = Popen(cmd)
    ps_proc = psutil.Process(proc.pid)
    init_probe = ps_proc.as_dict(attrs=['pid', 'name', 'username', 'cpu_num', 'cpu_percent', 'create_time', 'cwd', 'cmdline'])
    log_entry = dict(init_probe)
    log_entry['log_time'] = [time.time()]
    for attr in pickup_stats:
        log_entry[attr] = [log_entry[attr]]
    while proc_probe(ps_proc, log_entry):
        try:
            proc.wait(timeout=.1)
        except:
            pass
    log_entry['duration'] = log_entry['log_time'][-1:][0] - log_entry['log_time'][0]

    try:
        open('/tmp/psmon.log', 'a').write(json.dumps(log_entry))
    except:
        pass

    return proc.returncode

if __name__ == '__main__':
    sys.exit(execute_command(sys.argv[1:]))

