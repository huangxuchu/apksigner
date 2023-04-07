class ApkSigner:
    # 签名命令 参数：1=签名.jks或.keystore文件路径, 2=签名文件密码, 3=别名, 4=别名密码, 5=apk文件路径
    APKSIGNER_ORDER_SIGN = """ sign --ks %s --ks-pass pass:%s --ks-key-alias %s --key-pass pass:%s %s"""


class Aapt:
    # 获取apk的信息
    AAPT2_DUMP_BADGING = """ dump badging %s"""


class KeyTool:
    # 获取keystore的md5 参数：1=keystore文件路径, 2=keystore的密码
    KEYTOOL_LIST_V = """ -list -v -keystore %s -storepass %s"""
