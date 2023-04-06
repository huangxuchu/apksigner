class ApkSigner:
    # 签名命令 参数：1=签名.jks或.keystore文件路径, 2=签名文件密码, 3=别名, 4=别名密码, 5=apk文件路径
    APKSIGNER_ORDER_SIGN = """ sign --ks %s --ks-pass pass:%s --ks-key-alias %s --key-pass pass:%s %s"""
    # 获取apk包签名md5 参数：1=apk文件路径
    KEYTOOL_ORDER_APK_SIGN_INFO = """keytool -printcert -jarfile %s"""
    # 获取keystore的md5 参数：1=keystore文件路径, 2=keystore的密码
    KEYTOOL_ORDER_KEYSTORE_INFO = """keytool -list -v -keystore %s -storepass %s"""


class Aapt:
    AAPT2_DUMP_BADGING = """ dump badging %s"""
