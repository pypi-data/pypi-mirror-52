#!/usr/bin/env python3

import datetime
import socket
import subprocess

from pathlib import Path

def pth_relative_to(pth, rel=Path('.')) :
	try :
		return pth.resolve().to_relative(rel.resolve())
	except :
		return pth

def to_relative_cmd(cmd_lst, cwd) :
	if cwd is None :
		return cmd_lst
	stack = list()
	for cmd in cmd_lst :
		if isinstance(cmd, Path) :
			try :
				stack.append(pth_relative_to(cmd, cwd))
			except ValueError :
				stack.append(cmd)
		else :
			stack.append(cmd)
	return stack

def run(* cmd_lst, cwd=None, timeout=None, blocking=True, bg_task=False, quiet=False) :

	cwd_rel = cwd if cwd is not None else Path('.')
	cwd_abs = cwd_rel.resolve()

	cmd_line = list()
	for cmd in cmd_lst :
		if isinstance(cmd, dict) :
			for k, v in cmd.items() :
				cmd_line.append('--' + str(k))
				cmd_line.append(str(v))
		else :
			cmd_line.append(str(cmd))

	cmd_header = '\x1b[44m{0} {1}{2} $\x1b[0m '.format(
		socket.gethostname(),
		"{0} ".format(Path(* cwd_abs.parts[-3:])) if cwd is not None else '',
		datetime.datetime.now().strftime('%H:%M:%S')
	)

	if not quiet :
		print(cmd_header + ' '.join(to_relative_cmd(cmd_line, cwd)))

	if bg_task :
		subprocess.Popen(cmd_line, cwd=(str(cwd) if cwd is not None else cwd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	else :
		ret = subprocess.run(cmd_line, cwd=(str(cwd) if cwd is not None else cwd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
		if blocking and ret.returncode != 0 :
			if not quiet :
				print('\n' + ' '.join(ret.args) + '\n' + ret.stderr.decode(sys.stderr.encoding) + '\n' + '-' * 32)
			ret.check_returncode()
		return ret