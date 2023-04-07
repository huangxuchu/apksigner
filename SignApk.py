"""
为apk包签名。
需求：
1、批量签名apk
2、多个签名文件可选
逻辑：
1、网页上传apk文件到本地的temp文件夹下，并生成时间戳的文件夹。没有temp文件夹时需要自动生成。
2、签名程序获取本地temp目录下的时间错文件夹的目录下的所有apk
"""
import argparse
import os

import ApkInfo
import Config
import Constants
import KeystoreSupplier
from AndroidTools import ApkSigner
from JarSigner import JARSIGNER_ORDER_SIGN
from utils import FileUtils, DateUtils, CmdUtils

TAG = 'SignApk'

# 正在执行的任务
signing_task = []


def jar_signer(keystore_name, task_id, apk_path, output_path):
    if not _check_apk_path_valid(apk_path):
        return
    if keystore_name is None or len(keystore_name) == 0:
        print("使用jarsigner工具签名[--keystore]参数不能为空")
        return
    keystore = KeystoreSupplier.get_keystore_by_name(keystore_name)
    task_id = _get_task_id(task_id)
    print(
        '开始jarsigner签名: task=%s keystore=%s apk_path=%s output_path%s' % (task_id, keystore, apk_path, output_path))
    task = Config.JAR_SIGNER + JARSIGNER_ORDER_SIGN % (
        os.path.join(keystore[Constants.KEYSTORE_FOLDER], keystore[Constants.KEYSTORE]),
        os.path.join(output_path),
        apk_path,
        keystore[Constants.ALIAS],
        keystore[Constants.PASSWORD])
    code = os.system(task)
    return code


def sign_batch(keystore, task_id, input_path, output_path):
    """
    批量签名
    :param keystore: apk的签名文件
    :param task_id: 任务id
    :param input_path: 批量签名存放任务的目录
    :param output_path: 签名后的输出目录
    :return:
    """
    if not FileUtils.isdir(input_path) or not FileUtils.isdir(output_path):
        print(f'请输入正确的文件夹路径地址 apkPath={input_path} outputPath={output_path}')
        return
    if task_id is None or len(task_id) == 0:
        task_id = DateUtils.date_time()
    print('签名 task=%s apk_path=%s output_path=%s' % (task_id, input_path, output_path))
    print('Using Apksigner ' + (CmdUtils.popen(Config.APKSIGNER + ' --version')[0]).strip())
    if task_id in signing_task:
        return
    signing_task.append(task_id)
    taskPath = os.path.join(input_path)
    apkList = os.listdir(taskPath)
    apkList.sort()
    for apk in apkList:
        if not apk.endswith(".apk"):
            continue
        apk_path = os.path.join(taskPath, apk)
        code = _sign(keystore, apk_path)
        if code == 0:
            apk_sign = apk.replace(".apk", "_sign.apk")
            os.renames(apk_path, os.path.join(output_path, apk_sign))
            os.remove(apk_path + r'.idsig')
    signing_task.remove(task_id)


def sign(keystore, task_id, apk_path, output_path):
    """
    签名方法，签名后apk名称变为 xxx.apk->xxx_sign.apk
    :param keystore: apk的签名文件
    :param task_id: 任务id
    :param apk_path: apk的目录
    :param output_path: 签名后的输出目录
    :return:
    """
    if not _check_apk_path_valid(apk_path):
        return
    task_id = _get_task_id(task_id)
    print('签名 task=%s apk_path=%s output_path=%s' % (task_id, apk_path, output_path))
    print('Using Apksigner ' + (CmdUtils.popen(Config.APKSIGNER + ' --version')[0]).strip())
    signing_patch = apk_path + ".signing"
    FileUtils.copy(apk_path, signing_patch)
    code = _sign(keystore, signing_patch)
    if code == 0:
        apk_signed = os.path.basename(signing_patch).replace(".apk.signing", "_sign.apk")
        os.renames(signing_patch, os.path.join(output_path, task_id, apk_signed))
        os.remove(signing_patch + r'.idsig')
    else:
        print(f'签名失败 code={code}')


def _check_apk_path_valid(apk_path):
    v = apk_path.endswith(".apk")
    if not v:
        raise Exception("参数apkPath错误，不是有效的Apk文件")
    return v


def _get_task_id(task_id):
    if task_id is None or len(task_id) == 0:
        task_id = DateUtils.date_time()
    return task_id


def _sign(keystore, apk_path):
    if keystore is None or len(keystore) == 0:
        package_name = ApkInfo.get_apk_info(apk_path).package_name
        keystore = KeystoreSupplier.get_keystore_by_package(package_name)
    else:
        keystore = KeystoreSupplier.get_keystore_by_name(keystore)
    print("签名keystore=" + str(keystore))
    task = Config.APKSIGNER + ApkSigner.APKSIGNER_ORDER_SIGN % (
        os.path.join(keystore[Constants.KEYSTORE_FOLDER], keystore[Constants.KEYSTORE]),
        keystore[Constants.PASSWORD],
        keystore[Constants.ALIAS],
        keystore[Constants.ALIAS_PASSWORD],
        apk_path)
    code = os.system(task)
    return code


def _parse_dc(info):
    """
    解析指纹证书的字符串
    :param info:
    :return:
    """
    key = "证书指纹:"
    start = False
    DC = []
    for line in info:
        line = line.strip()
        if start:
            if line.startswith("MD5:"):
                DC.append(line)
            elif line.startswith("SHA1:"):
                DC.append(line)
            elif line.startswith("SHA256:"):
                DC.append(line)
                break
        if not start:
            start = line.startswith(key)
    return DC


def _parse_output_path(input_args):
    output_path = input_args.outputPath
    if output_path is not None and len(output_path) > 0:
        return output_path
    apk_path = input_args.apkPath
    sb = input_args.signBatch
    js = input_args.jarsigner
    if js:
        return apk_path.replace(".apk", "_sign.apk")
    elif sb:
        return apk_path
    else:
        return FileUtils.dirname(apk_path)


if __name__ == "__main__":
    print("---------------- SignApk 启动 ----------------")
    parser = argparse.ArgumentParser(description='APK签名工具')
    parser.add_argument('-a', '--apkPath', metavar='FILE', type=str, required=True,
                        help='要处理的Apk文件，如果是执行signBatch命令，请输入Apk所在的文件夹路径')
    parser.add_argument('-k', '--keystore', type=str,
                        help='是否指定已配置的签名文件')
    parser.add_argument('-o', '--outputPath', type=str,
                        help='是否指定Apk输出地址，默认为当前文件夹')
    parser.add_argument('-js', '--jarsigner', action="store_true",
                        help='是否使用jarsigner给apk包签名')
    parser.add_argument('-ski', '--showKeystoreInfo', action="store_true",
                        help='是否展示Execl表格签名信息')
    parser.add_argument('-sb', '--signBatch', action="store_true",
                        help='是否批量执行签名Apksigner.sign命令，批量签名将会删除源Apk文件，请注意备注')
    _args = parser.parse_args()
    _apkPath = _args.apkPath
    _keystoreName = _args.keystore
    _showKeystoreInfo = _args.showKeystoreInfo
    _signBatch = _args.signBatch
    _jarsigner = _args.jarsigner
    # 初始化keystore列表
    KeystoreSupplier.init(_showKeystoreInfo)
    print('处理的APK: ', _apkPath)
    outputPath = _parse_output_path(_args)
    print('输出地址: ', outputPath)
    if _keystoreName:
        print('签名文件: ', _keystoreName)
    else:
        print('签名文件: 使用Apk包名对应的配置签名')
    # 默认使用安卓的签名工具
    # 如果有jarsinger参数，使用jarsinger给apk签名
    # 如果有signBatch参数，使用批量给apk签名
    if _jarsigner:
        jar_signer(_keystoreName, None, _apkPath, outputPath)
    elif _signBatch:
        sign_batch(_keystoreName, None, _apkPath, outputPath)
    else:
        sign(_keystoreName, None, _apkPath, outputPath)
    print("---------------- SignApk 结束 ----------------")
    print("\n\n\n")
