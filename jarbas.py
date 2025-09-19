#!/usr/bin/env python3

# author: Vitor Navarro
# date: 2025
# description: Script to automate the installation and configuration of CasaOS inside a Colima environment on macOS or Linux.
# license: Check COPYING

import sys
import subprocess
import argparse
import re

MACOS = 'mac'
LINUX = 'linux'

# Check for tools installation
def check_tool_installed(tool_name: str, version_arg:str='--version', check_string:str=None) -> bool:
	"""
	Check if a tool is installed by running tool_name as a command with version parameter and checking its output for either tool_name or check_string presence, i.e. $curl --version
	"""

	try:
		result = subprocess.check_output([tool_name, version_arg])	
		text = result.decode(sys.stdout.encoding).strip().lower()
		print(f"{tool_name} is installed: {text}")
		if check_string:
			return check_string.lower() in text
		else: 
			return tool_name in text
	except Exception as e:
		print(f"An error occurred while checking for {tool_name}: {e}")
		return False

def check_brew_installed() -> bool:
	return check_tool_installed('brew', '--version')

def check_colima_installed() -> bool:
	return check_tool_installed('colima', '--version')

def check_docker_installed() -> bool:
	return check_tool_installed('docker', '--version')

# Install tools
def install_brew():
	print("Homebrew is not installed. Installing Homebrew to proceed.")
	try:
		subprocess.run(['/bin/bash', '-c', "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"])
		print("Homebrew installed successfully.")
	except Exception as e:
		print(f"Failed to install Homebrew. Error:{e}")
		sys.exit(1)

def install_docker(os_type:str):
	print("Docker CLI is not installed. Installing Docker CLI to proceed.")
	try:
		if os_type == MACOS:
			subprocess.run(['brew', 'install', 'docker'])
		elif os_type == LINUX:
			subprocess.run(['sudo', 'apt-get', 'update'])
			subprocess.run(['sudo', 'apt-get', 'install', '-y', 'docker.io'])
		print("Docker CLI installed successfully.")
	except Exception as e:
		print(f"Failed to install Docker CLI. Error:{e}")
		sys.exit(1)

def install_colima(os_type:str):
	print("Colima is not installed. Installing Colima to proceed.")
	try:
		if os_type == MACOS:
			subprocess.run(['brew', 'install', 'colima'])
		elif os_type == LINUX:
			subprocess.run(['sudo', 'apt-get', 'update'])
			subprocess.run(['sudo', 'apt-get', 'install', '-y', 'colima'])
		print("Colima installed successfully.")
	except Exception as e:
		print(f"Failed to install Colima. Error:{e}")
		sys.exit(1)

# Setup colima environment
def setup_colima_environment(use_defaults=False, env_name="casaosenv"):
	if use_defaults:
		print("Setting up Colima with default configuration.")
		try:
			subprocess.run(['colima', 'start'])
		except Exception as e:
			print(f"Failed to start Colima with default settings. Error:{e}")
			sys.exit(1)
	else:
		print("Setting up Colima with custom configuration.")
		try:
			subprocess.run(['colima', 'start', '--profile', env_name ,'--cpu', '4', '--memory', '8',
'--disk', '10', '--network-address', '--vm-type','vz'])
		except Exception as e:
			print(f"Failed to start Colima. Error:{e}")
			sys.exit(1)
	print(f"Colima environment setup completed. Run 'colima status {env_name}' to check the status.")

def setup_casaos(env_name="casaosenv"):
	"""
	Setup CasaOS inside the Colima environment by executing the CasaOS installation script within the Colima VM.
	"""

	print("Setting up CasaOS inside Colima environment.")
	try:
		p = subprocess.run(['colima','ssh','-p',env_name], input='curl -fsSL https://get.casaos.io | sudo bash', stdout=subprocess.PIPE, text=True, stderr=subprocess.PIPE)
		print(p.returncode)
		print(p.stdout)
		print(p.stderr)

		print("CasaOS setup completed successfully.")
	except Exception as e:
		print(f"Failed to set up CasaOS. Error:{e}")
		sys.exit(1)

def colima_profile_exists(profile_name: str) -> bool:
	"""
	Check if a Colima profile exists by parsing the output of 'colima list' command.
	"""

	try:
		result = subprocess.check_output(['colima', 'list'], text=True)
		lines = result.strip().split('\n')
		# Skip header line
		for line in lines[1:]:
			columns = line.split()
			if columns and columns[0] == profile_name:
				return True
		return False
	except Exception as e:
		print(f"Error running colima list: {e}")
		return False
	
def get_colima_ip(profile_name: str) -> str:
	"""
	Get the IP address of the Colima VM by parsing the output of 'colima status' command.
	"""

	try:
		result = subprocess.run(['colima', 'status', profile_name], text=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)        
		match = re.search(r'address:\s*([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', result.stdout or result.stderr)
		if match:
			return match.group(1)
		else:
			print("IP address not found in output.")            
	except Exception as e:
		print(f"Error running colima status: {e}")
	return ""

# Main

def main():	
	parser = argparse.ArgumentParser()
	parser.add_argument("-os", help="Set mac for macOS or linux for Linux", choices=['mac', 'linux'], type=str, default='mac')
	parser.add_argument("-use_colima_defaults", help="Use colima default template file for configuration", type=bool, default=False)
	parser.add_argument("-env_name", help="Name of the colima environment", type=str, default="casaosenv")
	parser.add_argument("-destroy", help="Destroy the colima environment. When used with -env_name, it destroys the specified environment.", action='store_true')
	parser.add_argument("-setup_casaos", help="Setup CasaOS inside the colima environment. Use this when colima is already installed.", action='store_true')
	args = parser.parse_args()
	if args.destroy:
		print("Destruction flag detected. Running teardown...")
		subprocess.run(['colima', 'delete', args.env_name])
		exit(0)
	print(f"Operating System set to: {args.os}")
	print("Checking for required tools...")
	if args.os == MACOS and not check_brew_installed():
		install_brew()
	if not check_docker_installed():
		install_docker(args.os)
	print("All required tools are installed.")
	print("Configuring colima environment...")
	if not check_colima_installed():
		install_colima(args.os)		
		setup_colima_environment(args.use_colima_defaults, args.env_name)		
	else:		
		if colima_profile_exists(args.env_name):
			print(f"Colima profile '{args.env_name}' already exists.")
		else:
			print(f"Colima profile '{args.env_name}' doesn't exists.")
			setup_colima_environment(args.use_colima_defaults, args.env_name)
	if args.setup_casaos:
		setup_casaos(args.env_name)	
		print("Setup completed successfully.")
		ip = get_colima_ip(args.env_name)
		if ip:
			print(f"Access CasaOS at: http://{ip}:port (replace 'port' with the actual port number only if you changed it during setup)")
	exit(0)	

if __name__ == "__main__":
	main()