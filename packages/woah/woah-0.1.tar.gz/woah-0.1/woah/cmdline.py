import time
import os
import shutil
import sys
import psutil

# TODO these should go in a config. We take no args.

scale = 1.2  # allow oversubscription for io wait
backoff_initial = 1.0
backoff_max = 60.0
backoff_factor = 1.61

def main(cmd=None):
    if cmd is None:
        cmd = sys.argv[1:]
    if not cmd:
        print("No command provided", file=sys.stderr)
        sys.exit(1)
    binary = shutil.which(cmd[0])
    if not binary:
        print(f"Cannot find {cmd[0]}", file=sys.stderr)
        sys.exit(1)

    cpus = psutil.cpu_count() * scale
    wait = backoff_initial
    first = True
    while True:
        n = psutil.getloadavg()[0]
        if n < cpus:
            if not first:
                print(f"{n:.2f} < {cpus:.2f}, passed", file=sys.stderr)
            break
        print(f"{n:.2f} >= {cpus:.2f}, waiting {wait:.2f}s", file=sys.stderr)
        time.sleep(wait)

        wait = min(wait * backoff_factor, backoff_max)
        first = False

    os.execv(binary, cmd)

if __name__ == '__main__':
    main(sys.argv[1:])
