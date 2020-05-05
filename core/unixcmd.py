# Python 3.6.9
# Ubuntu 18.04.4 LTS (Bionic Beaver)

import subprocess
import re


def process_run(cmd):
    print(cmd)
    try:
        return subprocess.run(cmd, shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    except:
        print("subprocess.run() failed")
        sys.exit()

def is_not_empty(data):
    if not data:       return False
    if len(data) == 0: return False
    if data == [[]]:   return False
    return True

def get_max_length(data_a):
    max_len = 0
    for i, line in enumerate(data_a):
        if max_len < len(line): max_len = len(line)
    return max_len

def str_to_array(run_result):
    result = []
    tmp = []
    for i, line in enumerate(run_result.stdout.decode("utf8").split("\n")):
        tmp.append(line.split())
    length = get_max_length(tmp[1:])
    for line in run_result.stdout.decode("utf8").split("\n"):
        if is_not_empty(line.split(None, length - 1)): result.append(line.split(None, length - 1))
    return result

def transpose_2d(data):
    length = get_max_length(data)
    result = [[None] * (len(data)) for i in range(1, length + 1)]
    for i, line in enumerate(data):
        for j, d in enumerate(line):
            if is_not_empty(data[i][j]) : result[j][i] = data[i][j]
    return result

def set_hash(key, value):
    result = {}
    if type(value) is str:
        if re.compile('\A\d+\Z').match(value):
            result[key] = int(value)
        else:
            result[key] = value
    else:
        result[key] = value
    return result

def main_routine(key_lv1, key_lv2, target):
    result = {}
    for i, lv1 in enumerate(key_lv1):
        tmp = {}
        for j, lv2 in enumerate(key_lv2):
            if is_not_empty(target[i][j]):
                tmp.update(set_hash(lv2, target[i][j]))
        result.update(set_hash(lv1, tmp))
    return result

def free(opt = None):
    def is_feasible(opt):
        if "s" in opt:    return False
        if "c" in opt:    return False
        if "v" in opt:    return False
        if "help" in opt: return False
        return True

    def get_head_list(run_result_a):
        key_lv2 = []
        for i in range(1, len(run_result_a)):
            key_lv2.append(run_result_a[i][0])
        return key_lv2

    def get_target_list(run_result_a):
        tmp = []
        for line in run_result_a[1:]:
            tmp.append(line[1:])
        return transpose_2d(tmp)

    def convert(run_result_a):
        key_lv1 = run_result_a[0]
        key_lv2 = get_head_list(run_result_a)
        target = get_target_list(run_result_a)
        return main_routine(key_lv1, key_lv2, target)

    if opt is None:
        return convert(str_to_array(process_run("free")))
    else:
        if is_feasible(opt):
            return convert(str_to_array(process_run("free " + opt)))
        else:
            print("error: This options cannot be used.")
            print("       -s N, --seconds N  repeat printing every N seconds")
            print("       -c N, --count N    repeat printing N times, then exit")
            print("       --version          output version information and exit")
            print("       --help")

def df(opt = None):
    def is_feasible(opt):
        if "v" in opt:    return False
        if "help" in opt: return False
        return True

    def get_head_list(run_result_a):
        result = []
        for i in range(1, len(run_result_a)):
            result.append(run_result_a[i][-1])
        return result

    def convert(run_result_a):
        key_lv1 = get_head_list(run_result_a)
        key_lv2 = run_result_a[0]
        target  = run_result_a[1:]
        return main_routine(key_lv1, key_lv2, target)

    if opt is None:
        return convert(str_to_array(process_run("df")))
    else:
        if is_feasible(opt):
            return convert(str_to_array(process_run("df " + opt)))
        else:
            print("error: This options cannot be used.")
            print("       --version          output version information and exit")
            print("       --help")