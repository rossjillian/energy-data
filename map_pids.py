import re
import sys
import subprocess


"""
https://github.com/peci1/nvidia-htop/blob/master/nvidia-htop.py
"""


def main():
    processes, pid, gpu_num, gpu_mem, user, cpu, mem, time, command = get_processes()
    user, cpu, mem, time, command = parse_processes(processes, pid, user, cpu, mem, time, command)
    print(user)
    print(pid)
    print(cpu)
    print(mem)
    print(time)
    print(command)


def get_pids(lines):
    is_new_format = False
    # Copy the utilization upper part verbatim
    for i in range(len(lines)):
        if not lines[i].startswith("| Processes:"):
            pass
        else:
            while not lines[i].startswith("|===="):
                m = re.search(r'GPU\s*GI\s*CI', lines[i])
                if m is not None:
                    is_new_format = True
                i += 1
            i += 1
            break

    gpu_num_idx = 1
    pid_idx = 2 if not is_new_format else 4
    gpu_mem_idx = -3
    pid, gpu_num, gpu_mem, user, cpu, mem, time, command = [], [], [], [], [], [], [], []
    while not lines[i].startswith("+--"):
        if "Not Supported" in lines[i]:
            i += 1
            continue
        line = lines[i]
        line = re.split(r'\s+', line)
        gpu_num.append(line[gpu_num_idx])
        pid.append(line[pid_idx])
        gpu_mem.append(line[gpu_mem_idx])
        user.append("")
        cpu.append("")
        mem.append("")
        time.append("")
        command.append("")
        i += 1
    return pid, gpu_num, gpu_mem, user, cpu, mem, time, command


def get_processes():
    ps_call = subprocess.run('nvidia-smi', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if ps_call.returncode != 0:
        print('nvidia-smi exited with error code {}:'.format(ps_call.returncode))
        print(ps_call.stdout.decode() + ps_call.stderr.decode())
        sys.exit()
    lines_proc = ps_call.stdout.decode().split("\n")
    lines = [line + '\n' for line in lines_proc[:-1]]
    lines += lines_proc[-1]

    pid, gpu_num, gpu_mem, user, cpu, mem, time, command = get_pids(lines)

    # Query the PIDs using ps
    ps_format = "pid,user,%cpu,%mem,etime,command"
    ps_call = subprocess.run(["ps", "-o", ps_format, "-p", ",".join(pid)], stdout=subprocess.PIPE)
    processes = ps_call.stdout.decode().split("\n")
    return processes, pid, gpu_num, gpu_mem, user, cpu, mem, time, command


def parse_processes(processes, pid, user, cpu, mem, time, command):
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
