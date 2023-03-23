import re
import subprocess


"""
https://github.com/peci1/nvidia-htop/blob/master/nvidia-htop.py
"""


def main():
    processes, pid = get_processes()
    user, cpu, mem, time, command = parse_processes(processes, pid)
    print(user)
    print(pid)
    print(cpu)
    print(mem)
    print(time)
    print(command)


def get_processes():
    pid = []

    # Query the PIDs using ps
    ps_format = "pid,user,%cpu,%mem,etime,command"
    ps_call = subprocess.run(["ps", "-o", ps_format, "-p", ",".join(pid)], stdout=subprocess.PIPE)
    processes = ps_call.stdout.decode().split("\n")
    return processes, pid


def parse_processes(processes, pid):
    user, cpu, mem, time, command = [], [], [], [], []
    # Parse ps output
    for line in processes:
        if line.strip().startswith("PID") or len(line) == 0:
            continue
        parts = re.split(r'\s+', line.strip(), 5)
        # idx = pid.index(parts[0])
        for idx in filter(lambda p: pid[p] == parts[0], range(len(pid))):
            user[idx] = parts[1]
            cpu[idx] = parts[2]
            mem[idx] = parts[3]
            time[idx] = parts[4] if "-" not in parts[4] else parts[4].split("-")[0] + " days"
            command[idx] = parts[5]
    return user, cpu, mem, time, command


if __name__ == '__main__':
    main()
