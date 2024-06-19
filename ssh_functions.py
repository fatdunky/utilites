'''
Created on 4 Dec. 2017

@author: mcrick
'''

import pexpect, tempfile, sys, logging,os, traceback
from pexpect import pxssh

def ssh_with_password(host, cmd, user, password, util_timeout=120, bg_run=False):

		ret_val = ""
		try:
				s = pxssh.pxssh(timeout=util_timeout,options={"StrictHostKeyChecking": "no", "ServerAliveInterval": "30", "ConnectTimeout":"10"})
				s.login(host, user, password,  login_timeout=util_timeout)
				logging.debug("ssh_cmd=%s",cmd)
				s.sendline(cmd)                 # run a command
				s.prompt()                      # match the prompt
				ret_val = s.before              # print everything before the prompt.
				s.logout()
		except pxssh.ExceptionPxssh as e:
				logging.info("pxssh failed on login.")
				logging.info(e)
		except Exception as e:
				logging.info("pxssh caught exception.")
				logging.info(e)

		return ret_val

def ssh_hop_with_password(host1, host2, cmd, user1, user2, password1, password2, util_timeout=120, bg_run=False):
		ret_val = ""
		try:
				s = pxssh.pxssh(timeout=util_timeout,options={"StrictHostKeyChecking": "no", "ServerAliveInterval": "30", "ConnectTimeout":"10"})
				s.login(host1, username=user1, password=password1)
				logging.debug("host1=%s",host1)
				s.login(host2, username=user2, password=password2, spawn_local_ssh=False)
				logging.debug("host2=%s",host2)
				logging.debug("ssh_cmd=%s",cmd)
				s.sendline(cmd)                 # run a command
				s.prompt()                      # match the prompt
				ret_val = s.before              # print everything before the prompt.
				s.sendline('exit') # logout is very slow here?
				s.logout()
		except pxssh.ExceptionPxssh as e:
				logging.info("pxssh failed on login.")
				logging.info(e)
		except Exception as e:
				logging.info("pxssh caught exception.")
				logging.info(e)
				exc_type, exc_value, exc_tb = sys.exc_info()
				logging.info(traceback.format_exception(exc_type, exc_value, exc_tb))

		return ret_val



def ssh_with_password_old(host, cmd, user, password, timeout=30, bg_run=False):
		"""SSH'es to a host using the supplied credentials and executes a command.
		Throws an exception if the command doesn't return 0.
		bgrun: run command in the background"""

		fname = tempfile.mktemp()

		try:
				fout = open(fname, 'w')

				options = "-vvv -o 'StrictHostKeyChecking no' -o 'ConnectTimeout 10' -o 'PubkeyAuthentication=no'"
				if bg_run:
						options += ' -f'
				ssh_cmd = 'ssh %s@%s %s "%s"' % (user, host, options, cmd)
				logging.debug("ssh_cmd=%s",ssh_cmd)
				child = pexpect.spawn(ssh_cmd, timeout=timeout)
				child.expect(['password:'])
				child.sendline(password)
				#python3 complains unless we use the buffer
				if (sys.version_info >= (3, 0)):
						logging.debug("python3+ using buffer")
						child.logfile = fout.buffer
				else:
						logging.debug("python2+ not using buffer")
						child.logfile = fout
				child.expect(pexpect.EOF)
				child.close()
				fout.close()

				fin = open(fname, 'r')
				stdout = fin.read()
				fin.close()
		except:
				print("Exception was thrown")
				print((sys.exc_info()[0]))
				print("debug information:")
				print((str(child)))

		finally:
				fout.close()

		#if 0 != child.exitstatus:
				#raise Exception(stdout)

		return stdout

def scp_with_password(host, sfile, destination, user, password):
		"""scp to a host using the supplied credentials and executes a command.
		Throws an exception if the command doesn't return 0.
		bgrun: run command in the background"""

		fname = tempfile.mktemp()
		fout = open(fname, 'w')

		options = "-l 3600 -C -q -o 'StrictHostKeyChecking no' -o 'ConnectTimeout 10' -o 'PubkeyAuthentication=no'"

		ssh_cmd = 'scp %s %s@%s:%s %s' % (options,user, host, sfile, destination)
		child = pexpect.spawn(ssh_cmd)
		child.expect(['password: '])
		child.sendline(password)
		#python3 complains unless we use the buffer
		if (sys.version_info >= (3, 0)):
				child.logfile = fout.buffer
		else:
				child.logfile = fout
		child.expect(pexpect.EOF)
		child.close()
		fout.close()

		fin = open(fname, 'r')
		stdout = fin.read()
		fin.close()

		if 0 != child.exitstatus:
				raise Exception(stdout)

		return stdout

def scp_with_no_password(host, sfile, destination, user, password):
		"""scp to a host using the supplied credentials and executes a command.
		Throws an exception if the command doesn't return 0.
		bgrun: run command in the background"""

		fname = tempfile.mktemp()
		fout = open(fname, 'w')

		options = "-l 3600 -C -q -o 'StrictHostKeyChecking no' -o 'ConnectTimeout 10' -o 'PubkeyAuthentication=no'"

		ssh_cmd = 'scp %s %s@%s:%s %s' % (options,user, host, sfile, destination)
		child = pexpect.spawn(ssh_cmd)
		#python3 complains unless we use the buffer
		if (sys.version_info >= (3, 0)):
				child.logfile = fout.buffer
		else:
				child.logfile = fout
		child.expect(pexpect.EOF)
		child.close()
		fout.close()

		fin = open(fname, 'r')
		stdout = fin.read()
		fin.close()

		if 0 != child.exitstatus:
				raise Exception(stdout)

		return stdout

def ssh_no_password(host, cmd, user, util_timeout=300, bg_run=False):
		ret_val = ""
		try:
				s = pxssh.pxssh(timeout=util_timeout,options={"StrictHostKeyChecking": "no", "ServerAliveInterval": "30", "ConnectTimeout":"10", "PreferredAuthentications":"hostbased,publickey"})
				s.login(host, user, login_timeout=util_timeout)
				logging.debug("ssh_cmd=%s",cmd)
				s.sendline(cmd)                 # run a command
				s.prompt()                      # match the prompt
				ret_val = s.before              # print everything before the prompt.
				s.logout()
		except pxssh.ExceptionPxssh as e:
				logging.info("pxssh failed on login.")
				logging.info(e)
		except Exception as e:
				logging.info("pxssh caught exception.")
				logging.info(e)

		return ret_val


def ssh_no_password_old(host, cmd, timeout=30, bg_run=False):
		"""SSH'es to a host using the supplied credentials and executes a command.
		Throws an exception if the command doesn't return 0.
		bgrun: run command in the background"""

		fname = tempfile.mktemp()
		fout = open(fname, 'w')

		options = "q -n -o 'StrictHostKeyChecking no' -o 'ConnectTimeout 10' -o 'PreferredAuthentications hostbased,publickey'"
		if bg_run:
				options += ' -f'
		ssh_cmd = 'ssh %s "%s"' % (host, options, cmd)
		child = pexpect.spawn(ssh_cmd, timeout=timeout)
		#python3 complains unless we use the buffer
		if (sys.version_info >= (3, 0)):
				child.logfile = fout.buffer
		else:
				child.logfile = fout
		child.expect(pexpect.EOF)
		child.close()
		fout.close()

		fin = open(fname, 'r')
		stdout = fin.read()
		fin.close()

		if 0 != child.exitstatus:
				raise Exception(stdout)

		return stdout
