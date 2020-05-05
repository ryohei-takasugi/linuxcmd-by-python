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

def str_to_array(run_result):
    result = []
    for line in run_result.stdout.decode("utf8").split("\n"):
        if is_not_empty(line.rsplit()): result.append(line.rsplit())
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


def free(opt = None):
    def one_line_convert(run_result_a, col):
        tmp = {}
        result = {}
        for row in range(1, len(run_result_a)):
            if len(run_result_a[row]) > col:
                tmp.update(set_hash(run_result_a[row][0][:-1], run_result_a[row][col]))
        result.update(set_hash(run_result_a[0][col], tmp))
        return result

    def convert(run_result_a):
        result = {}
        run_result_a[0].insert(0, "dmmy_head")
        for col in range(1, len(run_result_a[0])):
            result.update(one_line_convert(run_result_a, col))
        return result

    if opt is None:
        return convert(str_to_array(process_run("free")))
    else:
        return convert(str_to_array(process_run("free " + opt)))


def df(opt = None):
    def get_head_list(run_result_a):
        result = []
        for i in range(1, len(run_result_a)):
            result.append(run_result_a[i][-1])
        return result

    def one_line_convert(run_result_a, row):
        tmp = {}
        result = {}
        head = get_head_list(run_result_a)
        for col in range(1, len(run_result_a[0])):
            if len(run_result_a[row]) > col:
                tmp.update(set_hash(run_result_a[0][col], run_result_a[row][col]))
        result.update(set_hash(head[row - 1], tmp))
        return result

    def convert(run_result_a):
        result = {}
        for row in range(1, len(run_result_a)):
            result.update(one_line_convert(run_result_a, row))
        return result

    if opt is None:
        return convert(str_to_array(process_run("df")))
    else:
        return convert(str_to_array(process_run("df " + opt)))