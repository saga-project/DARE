#!/usr/bin/env python
import os
import sys
from django.core.management import execute_from_command_line

sys.path.append("apps")
full_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(full_path, "deployment"))


if __name__ == "__main__":
    os.environ['APPENV'] = 'Development'
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dare-site.settings")
    execute_from_command_line()
