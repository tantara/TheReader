#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TheReader.settings")

	from django.core.management import execute_from_command_line

	project_root = os.path.dirname(os.path.realpath(__file__))
	sys.path.append(os.path.join(project_root, 'utils'))

	execute_from_command_line(sys.argv)
