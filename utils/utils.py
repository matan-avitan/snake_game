import sys
import os


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname('main.py')))
    final_path = os.path.join(base_path, relative_path)
    return final_path