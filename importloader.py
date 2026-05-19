#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import re

SAFE_MODULE_RE = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

def _valid_name(name):
	if not isinstance(name, str):
		return False
	if not SAFE_MODULE_RE.match(name):
		return False
	# prevent importing dangerous built-in or system modules
	blocked = {'os', 'sys', 'subprocess', 'shutil', 'socket', 'importlib',
			   '__builtin__', 'builtins', 'ctypes', 'inspect', 'code'}
	return name not in blocked

def load(name):
	if not _valid_name(name):
		return None
	try:
		obj = __import__(name)
		try:
			reload(obj)
		except NameError:
			pass
		return obj
	except Exception:
		pass

	try:
		import importlib
		obj = importlib.__import__(name)
		importlib.reload(obj)
		return obj
	except Exception:
		pass

def loads(namelist):
	for name in namelist:
		obj = load(name)
		if obj is not None:
			return obj
