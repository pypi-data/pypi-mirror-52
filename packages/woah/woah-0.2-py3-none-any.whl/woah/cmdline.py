"""
The woah tool lets you wait while your system's loadavg is high.  For example:

    woah echo hi

will wait for a reasonable loadavg before running `echo hi`
"""

import os
import shutil
import sys
import time
from multiprocessing import cpu_count

# TODO these should go in a config. We take no args.

scale = 1.2  # allow oversubscription for io wait
backoff_secs_initial = 1.0
backoff_secs_max = 60.0
backoff_factor = 1.61


def backoff_msg(s, first):
    print(s, file=sys.stderr)


def pass_msg(s, first):
    if not first:
        print(s, file=sys.stderr)


def main(cmd=None):
    if cmd is None:
        cmd = sys.argv[1:]
    if not cmd:
        print("ERROR: No command provided", file=sys.stderr)
        print(__doc__.rstrip(), file=sys.stderr)
        sys.exit(1)
    binary = shutil.which(cmd[0])
    if not binary:
        print(f"ERROR: Cannot find {cmd[0]}", file=sys.stderr)
        print(__doc__.rstrip(), file=sys.stderr)
        sys.exit(1)

    cpus = cpu_count() * scale
    wait = backoff_secs_initial
    first = True
    while True:
        n = os.getloadavg()[0]
        if n < cpus:
            pass_msg(f"{n:.2f} < {cpus:.2f}, passed", first)
            break
        backoff_msg(f"{n:.2f} >= {cpus:.2f}, waiting {wait:.2f}s", first)
        time.sleep(wait)

        wait = min(wait * backoff_factor, backoff_secs_max)
        first = False

    os.execv(binary, cmd)


if __name__ == "__main__":  # pragma: no cover (test_exec runs this)
    main()
