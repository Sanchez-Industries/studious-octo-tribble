#!/usr/bin/python3
#coding: utf-8

# LIBRARY'S IMPORTATION
from _typeshed import NoneType
from os import system 

# DEFAULT DESTINATION OF THE PLAYLOAD INJECTION
playload_destination = "/etc/ssh/ssh_config"

# DEFAULT CONFIGURATIONS READY TO BE INJECTED INSIDE `/etc/ssh/ssh_config` FILE
short_name_Host = ""
optionnal_setting_PasswordAuthentication = "no"
optionnal_setting_CheckHostIP = "yes"
ssh_destination_server_port = 22
server_domain_name_or_ip_addr = None
User = "root"
commented_IdentityFile = ""
ssh_folder_of_user_path = "~/.ssh/"
dynamic_port_of_proxy = 4712

# DEFAULT BASH SCRIPT CODE OF THE FILE inside the `/opt/` folder
custom_command_on_beginning_launch = ""
custom_command_on_try_connect = ""
custom_command_on_disconnect = ""
# the same var `short_name_Host` from ssh_config settings are re-used for the connection bash script and this bash code are called by the systemd service !
restartAfterSec = 60


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


current_configuration_number_of_SOCKS5_host = 1
script_location_for_call_by_the_service = "/opt/auto-connect-SOCKS5-number_{current_configuration_number_of_SOCKS5_host}.sh".format(
            current_configuration_number_of_SOCKS5_host=current_configuration_number_of_SOCKS5_host 
    )

service_description = "automatic SOCKS5 ssh reconnection"

setting_unrecommended_to_mods_StartLimitIntervalSec = 0
setting_unrecommended_to_mods_RestartSec = 1
setting_unrecommended_to_mods_User = "root"
setting_unrecommended_to_mods_Restart = "always"

automatic_socks5_connection_systemd_service = """
[Unit]
Description={service_description}
After=network.target
StartLimitIntervalSec= {setting_unrecommended_to_mods_StartLimitIntervalSec}

[Service]
Type=simple
Restart={setting_unrecommended_to_mods_Restart}
RestartSec={setting_unrecommended_to_mods_RestartSec}
User={setting_unrecommended_to_mods_User}
ExecStart=/bin/bash {script_location_for_call_by_the_service}
[Install]
WantedBy=multi-user.target
""".format( script_location_for_call_by_the_service = script_location_for_call_by_the_service,
            service_description = service_description,
            setting_unrecommended_to_mods_StartLimitIntervalSec = setting_unrecommended_to_mods_StartLimitIntervalSec,
            setting_unrecommended_to_mods_RestartSec = setting_unrecommended_to_mods_RestartSec,
            setting_unrecommended_to_mods_User = setting_unrecommended_to_mods_User,
            setting_unrecommended_to_mods_Restart = setting_unrecommended_to_mods_Restart )

class Studious_Playload_Injector(object):
    def __init__(self):
        pass

    def setDestinationOfInjection(self, destined_filepath):
        self.destination_filepath = destined_filepath

    def setPlayloadToInjection(self, playload):
        self.loaded_playload = playload

    def inject(self, destination_filepath = None, configured_playload = None):
        if type(destination_filepath) == NoneType:
            destination_filepath = self.destination_filepath
        if type(configured_playload) == NoneType:
            configured_playload = self.loaded_playload

        try:
            #injection operations, from the playload of configuration to the destination file, at the end of file, writing in append mode
            with open(destination_filepath, "a") as configuration_file:
                configuration_file.write("\n{}".format(configured_playload))
                configuration_file.close()
        except Exception as e:
            print("\nError ! : \n{e}".format( e = e ))
            exit(-1)


#inject the configuration of saved socks5 connection configuration to `/etc/ssh/ssh_config` at the end of file, writing in append mode

