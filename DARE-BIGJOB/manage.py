#!/usr/bin/env python
import os
import sys

sys.path.append("apps")
full_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(full_path, "deployment"))


if __name__ == "__main__":
    #!/usr/bin/python
    new_args = []
    for arg in sys.argv:
        if arg == '--dev':
            os.environ['APPENV'] = 'Development'
        else:
            new_args.append(arg)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dare-site.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(new_args)
