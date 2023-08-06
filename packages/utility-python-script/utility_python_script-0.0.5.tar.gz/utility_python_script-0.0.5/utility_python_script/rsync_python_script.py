#!/usr/bin/python3
"""
# rsync-python-script.py
Rsync files specified in a `JSON` config. If a mountpoint is specified, then only `rsync` if the
mountpoint is mounted.
"""
import errno
import json
import os
import sys

from helputils.core import mkdir_p, log, ismount_remote, rsync, find_mountpoint


def main():
    with open('/etc/utility-python-script/rsync-python-script.json') as config_file:
        conf_mod = json.load(config_file)
    rsync_args = [
        "--delete",
        "--ignore-errors",
        "--links",
        "--modify-window=1",
        "--perms",
        "--progress",
        "--recursive",
        "--times",
        "--whole-file",
        "-v"
    ]
    for k, task in conf_mod.items():
        mps = task.get("mp", None)
        if mps:
            for mp in mps:
                if not mp == find_mountpoint(mp):
                    log.error("(ERROR) Required mount point %s is not available." % mp)
                    sys.exit()
        rsync(task["src"], task["dst"], rsync_args=rsync_args)
