#!/usr/bin/python3
#coding: utf-8

from os import system 

short_name_Host = ""
optionnal_setting_PasswordAuthentication = "no"
optionnal_setting_CheckHostIP = "yes"
ssh_destination_server_port = 22
server_domain_name_or_ip_addr = None
User = "root"
commented_IdentityFile = ""
ssh_folder_of_user_path = "~/.ssh/"
dynamic_port_of_proxy = 4712


# Declaration and formating the playload configuration for fast injection to the system
playload_to_ssh_config = """
Host {short_name_Host}
	PasswordAuthentication {optionnal_setting_PasswordAuthentication}
	CheckHostIP {optionnal_setting_CheckHostIP}
	ConnectTimeout 0
	Port {ssh_destination_server_port}
	Hostname  {server_domain_name_or_ip_addr}
	User {User}
	Protocol 2
	{commented_IdentityFile}IdentityFile {ssh_folder_of_user_path}{ssh_id_file}
	DynamicForward {dynamic_port_of_proxy}
	RequestTTY no
	SessionType none
""".format( short_name_Host=short_name_Host,
            optionnal_setting_PasswordAuthentication = optionnal_setting_PasswordAuthentication,
            optionnal_setting_CheckHostIP = optionnal_setting_CheckHostIP,
            ssh_destination_server_port = ssh_destination_server_port,
            server_domain_name_or_ip_addr = server_domain_name_or_ip_addr,
            User = User,
            commented_IdentityFile = commented_IdentityFile,
            ssh_folder_of_user_path = ssh_folder_of_user_path,
            dynamic_port_of_proxy = dynamic_port_of_proxy )

#inject the configuration of saved socks5 connection configuration to `/etc/ssh/ssh_config` at the end of file, writing in append mode
with open("/etc/ssh/ssh_config", "a") as ssh_configuration_file:
    ssh_configuration_file.write("\n{}".format(playload_to_ssh_config))
    ssh_configuration_file.close()


custom_command_on_beginning_launch = ""
custom_command_on_try_connect = ""
custom_command_on_disconnect = ""
short_name_Host = ""
restartAfterSec = 60

playload_bash_file_autoSOCKS5_sh="""
{custom_command_on_beginning_launch}
while :
do
    {custom_command_on_try_connect}
    /usr/bin/ssh {short_name_Host}
    {custom_command_on_disconnect}
    sleep {restartAfterSec}
done
""".format( custom_command_on_beginning_launch = custom_command_on_beginning_launch,
            custom_command_on_try_connect = custom_command_on_try_connect,
            custom_command_on_disconnect = custom_command_on_disconnect,
            short_name_Host = short_name_Host,
            restartAfterSec = restartAfterSec
          )

automatic_socks5_connection_systemd_service = """
[Unit]
Description=automatic SOCKS5 ssh reconnection
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=root
ExecStart=/bin/bash /opt/autoSOCKS5.sh
[Install]
WantedBy=multi-user.target
"""