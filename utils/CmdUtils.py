import os
import subprocess


# 执行控制台命令，并返回日志（注意：日志过多的问题）
def popen(command):
    r = os.popen(command)  # 执行该命令
    info = r.readlines()  # 读取命令行的输出到一个list
    r.close()
    return info


# 执行命令行
def system(command):
    return os.system(command)


# 执行控制台命令，并返回日志（注意：日志过多的问题）
def subrun(command, result_succeed_msg: bool = False):
    # 执行控制台命令
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    # 检查命令执行是否成功
    if result.returncode == 0:
        if not result_succeed_msg:
            return result.returncode
        # 读取控制台输出信息
        output = result.stdout
        return str(output)
    else:
        # 输出错误消息
        error = result.stderr
        return str(error)
