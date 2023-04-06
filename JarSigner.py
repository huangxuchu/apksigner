#!/usr/bin/python3
# 文件工具类工具类

# 参数1：签名文件路径
# 参数2：签名后Apk文件输出路径
# 参数3：签名前Apk文件路径
# 参数4: 别名->weiddanxshuo
# 参数5：签名密码
# 事例: jarsigner -verbose -keystore /novel_keystore/weiddanxshuo.jks -signedjar /Downloads/sign.apk /Downloads/unsign.apk weiddanxshuo -storepass 123456
JARSIGNER_ORDER_SIGN = """ -verbose -keystore %s -signedjar %s %s %s -storepass %s"""
