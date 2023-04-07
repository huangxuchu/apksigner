import os

# 签名配置文件路径
# eg: NOVEL_KEYSTORE_EXECL_PATH = "./example/novel_password.xlsx"
NOVEL_KEYSTORE_EXECL_PATH = "/Users/hongxiang/Develop/project_keystore/novel_password.xlsx"

# 存放签名文件的路径
# eg: NOVEL_KEYSTORE_PATH = "./example/novel_keystore"
NOVEL_KEYSTORE_PATH = "/Users/hongxiang/Develop/project_keystore/novel_keystore"

# 安卓sdk目录
ANDROID_SDK_HOME_PATH = "/Users/hongxiang/Library/Android/sdk"
ANDROID_SDK_VERSION = '32.0.0'

# apktool工具存放地址
APKTOOL_JAR = os.path.join(ANDROID_SDK_HOME_PATH, 'apktool', 'apktool.jar')
# apksigner工具地址
APKSIGNER = os.path.join(ANDROID_SDK_HOME_PATH, 'build-tools', ANDROID_SDK_VERSION, 'apksigner')
# aapt2
AAPT2 = os.path.join(ANDROID_SDK_HOME_PATH, 'build-tools', ANDROID_SDK_VERSION, 'aapt')

# jarsigner工具存放地址，有配置环境可以直接使用jarsigner
JAR_SIGNER = "jarsigner"

# keytool，有配置环境可以直接使用keytool
KEY_TOOL = "keytool"
