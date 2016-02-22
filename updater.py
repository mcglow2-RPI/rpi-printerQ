import paramiko
from config import settings

def update_printer():
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(settings['SSH_SERVER'], username = settings['SSH_USERNAME'], password = settings['SSH_PASSWORD'])

	stdin, stdout, stderr = ssh.exec_command("lpq -P" + "vcpalw")
	output = stdout.readlines()
	print(output)

	ssh.close()

if __name__ == '__main__':
	update_printer()