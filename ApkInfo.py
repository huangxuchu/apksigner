#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
import os

import Config
import Constants
import KeystoreSupplier
from AndroidTools import Aapt, KeyTool
from utils import CmdUtils
import re


class Info:
    package_name = ""
    version_n = ""
    version_code = ""

    def __init__(self, package_name="", version_name="", version_code=""):
        self.package_name = package_name
        self.version_n = version_name
        self.version_code = version_code


def get_apk_info(apk_path):
    task = Config.AAPT2 + Aapt.AAPT2_DUMP_BADGING % (
        apk_path
    )
    msg = CmdUtils.popen(task)
    if len(msg) > 0:
        packageInfo = msg[0]
        # 获取包名
        mp = re.match("package: name='([^' ]*)", packageInfo)
        packageName = mp.group(1).strip()
        # 匹配版本code
        mvc = re.search("versionCode='(\\d+)'", packageInfo)
        versionCode = mvc.group(1).strip()
        # 匹配版本名称
        mvn = re.search("versionName='([^' ]*)", packageInfo)
        versionName = mvn.group(1).strip()
        print("获取包信息 packageName=%s versionName=%s versionCode=%s" % (packageName, versionName, versionCode))
        return Info(packageName, versionName, versionCode)
    else:
        return Info()


def show_keystore_list(keystore_name):
    k = KeystoreSupplier.get_keystore_by_name(keystore_name)
    _show_keystore_list(k)


def _show_keystore_list(keystore):
    kk = os.path.join(Config.NOVEL_KEYSTORE_PATH, keystore[Constants.KEYSTORE])
    kps = keystore[Constants.PASSWORD]
    print(f"签名文件: {kk}")
    print(f"签名配置: {str(keystore)}")
    CmdUtils.system(Config.KEY_TOOL + KeyTool.KEYTOOL_LIST_V % (kk, kps))


def show_keystore_list_by_package(package_name):
    k = KeystoreSupplier.get_keystore_by_package(package_name)
    _show_keystore_list(k)


if __name__ == "__main__":
    print("---------------- ApkInfo 启动 ----------------")
    KeystoreSupplier.init()
    parser = argparse.ArgumentParser(description='APK信息获取工具')
    parser.add_argument('-kn', '--keystoreName', type=str,
                        help='指定已配置的签名文件')
    parser.add_argument('-pn', '--packageName', type=str,
                        help='指定已配置的包名')
    parser.add_argument('-kl', '--keystoreList', action="store_true",
                        help='列出密钥库(keystore)中的条目')
    _args = parser.parse_args()
    _keystoreList = _args.keystoreList
    if _keystoreList:
        # 初始化keystore列表
        KeystoreSupplier.init(False)
        _packageName = _args.packageName
        _keystoreName = _args.keystoreName
        if _keystoreName:
            show_keystore_list(_keystoreName)
        elif _packageName:
            show_keystore_list_by_package(_packageName)
    print("---------------- ApkInfo 结束 ----------------")
    print("\n\n\n")
