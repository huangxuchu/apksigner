# 签名信息 key=包名
from types import MappingProxyType

import Config
import Constants
from utils import ExcelFileUtils

_keystore = {}


def keystore():
    if len(_keystore) == 0:
        raise Exception("KeystoreSupplier未初始化，请调用init方法进行初始化")
    return MappingProxyType(_keystore)


def get_keystore_by_package(package_name, show_keystore_info=False):
    init(show_keystore_info)
    k = _keystore[package_name]
    if k is None or len(k) == 0:
        raise Exception(
            '未获取到签名数据，请检查"keystore"的配置文件是否存在，并确认是否配置包名为\"%s\"的行。' % package_name)
    return k


def get_keystore_by_name(keystore_name, show_keystore_info=False):
    init(show_keystore_info)
    k = ""
    for v in _keystore.values():
        if v[Constants.KEYSTORE] == keystore_name:
            k = v
            break
    if k is None or len(k) == 0:
        raise Exception(
            '未获取到签名数据，请检查"keystore"的配置文件是否存在，并确认是否配置签名为\"%s\"的行。' % keystore_name)
    return k


def init(show_keystore_info=False):
    global _keystore
    if len(_keystore) == 0:
        if show_keystore_info:
            print("+++++++ 加载Execl文件配置数据 开始 +++++++")
        sheet = ExcelFileUtils.get_sheet(Config.NOVEL_KEYSTORE_EXECL_PATH, ExcelFileUtils.DEFAULT_SHEET_ONE)
        obj = {}
        for rowOfCellObjects in sheet["A2":"G50"]:
            element = {}
            packageName = ""
            for cellObj in rowOfCellObjects:
                coordinate = cellObj.coordinate
                value = ""
                if cellObj.value is not None:
                    value = cellObj.value
                if coordinate.startswith("A"):
                    element[Constants.APP_NAME] = value
                elif coordinate.startswith("B"):
                    if value is None or len(value) <= 0:
                        break
                    element[Constants.PACKAGE_NAME] = value
                    packageName = value
                elif coordinate.startswith("C"):
                    element[Constants.KEYSTORE] = value
                elif coordinate.startswith("D"):
                    element[Constants.PASSWORD] = value
                elif coordinate.startswith("E"):
                    element[Constants.ALIAS] = value
                elif coordinate.startswith("F"):
                    element[Constants.ALIAS_PASSWORD] = value
                elif coordinate.startswith("G"):
                    element[Constants.REMARK] = value
                if show_keystore_info:
                    print(coordinate + "->" + value)
            if len(element) > 0 and Constants.PACKAGE_NAME in element:
                obj[packageName] = element
        if show_keystore_info:
            print("+++++++ 加载Execl文件配置数据 结束 +++++++")
        _keystore = obj
