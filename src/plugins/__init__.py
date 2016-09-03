# -*- coding: utf-8 -*-

import glob, os, importlib, time

JOB_INSTANCE_CLASS = "ExpandWorker"


class BaseWorker(object):
    def __init__(self, idx = 0):
        self.idx = idx
    
    def run(self):
        pass

    def is_valid(self):
        if os.getppid() == 1:
            return False
        else:
            return True




def list_module():
    package_path = os.path.dirname(os.path.abspath(__file__))
    python_files = os.path.join(package_path, "*.py")

    modules = {}
    for f in glob.glob(python_files):
        module_name = os.path.splitext(os.path.basename(f))[0]
        module = importlib.import_module(__name__ + '.' + module_name)

        if  hasattr(module, JOB_INSTANCE_CLASS):
            modules[module_name] = module
    return modules


def has_module(module_name):
    modules = list_module()
    if module_name in modules:
        return True
    else:
        return False


def module(module_name):
    modules = list_module()
    if module_name in modules:
        return modules[module_name]
    else:
        return None