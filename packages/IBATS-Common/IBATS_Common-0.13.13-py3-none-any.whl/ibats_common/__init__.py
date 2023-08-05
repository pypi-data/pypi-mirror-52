#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/6/26 10:27
@File    : __init__.py.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import os
import re

from ibats_utils.mess import get_folder_path

module_root_path = get_folder_path(re.compile(r'^ibats[\w]+'), create_if_not_found=False)  # 'ibats_common'
root_parent_path = os.path.abspath(os.path.join(module_root_path, os.path.pardir)) \
    if module_root_path is not None else None
