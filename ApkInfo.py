#!/usr/bin/python
# -*- coding: UTF-8 -*-
class ApkInfo:
    package_name = ""
    version_n = ""
    version_code = ""

    def __init__(self, package_name, version_name, version_code):
        self.package_name = package_name
        self.version_n = version_name
        self.version_code = version_code
