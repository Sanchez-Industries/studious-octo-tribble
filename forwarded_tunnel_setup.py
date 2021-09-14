#!/usr/bin/python3
#coding: utf-8
# LIBRARY'S IMPORTATION
from os import system
from StudiousParasites.StudiousPlayloadInjector import Studious_Playload_Injector as PlayloadInjector
ParasitesConfigTool = PlayloadInjector()
import argparse
from pathlib import Path
import sys
# args Parsing of the command line tool
parser = argparse.ArgumentParser("Forwarded Tunnel Setup - v1")
#
# Args to set usages modes
parser.add_argument("connection_name", type=str,
                    help="Name of the connection setting.")
parser.add_argument("-s", "--script-location-filepath", type=str,
                    help="Script ,default is an bash script into /opt/ and name start with `autotunnel`.")
parser.add_argument("-fp","--forwarding-ports", type=str,
                    help="Set ports redirections setting (e.g.: `-fp 80:8080`).", required=True)
parser.add_argument("-p","--SSH-server-port", type=int,
                    help="Set port for SSH Session setting (e.g.: `-p 22`).")
parser.add_argument("-i","--SSH-id-filepath", type=str,
                    help="Set identity file for SSH Session setting (e.g.: `-i ~/.ssh/id_rsa`).", required=True)
parser.add_argument("-u","--SSH-server-username", type=str,
                    help="Set UserName for SSH Session setting (e.g.: `-u root`)", required=True)
parser.add_argument("-d","--SSH-server-domain-name", type=str,
                    help="Set domain name for SSH Session setting (e.g.: `-d exemple.com`)", required=True)
#
args = parser.parse_args()
#
if args.SSH_server_port:
    SSH_server_port = args.SSH_server_port
else:
    SSH_server_port = 22
#
if args.SSH_server_username:
    SSH_server_username = args.SSH_server_username
#
ConnectionName = args.connection_name
#
if args.script_location_filepath:
    script_location_to_be_called_by_the_service = args.script_location_filepath
else:
    script_location_to_be_called_by_the_service = "/opt/autotunnel_p{}.sh".format(args.forwarding_ports.replace(":","-"))
#
service_location_systemd_file = "/etc/systemd/system/autotunnel_p{}.service".format(args.forwarding_ports.replace(":","-"))
#
# =====================(RECOMMENDED: DO NOT CHANGE)
# OTHER SPECIFICS CONFIGURATIONS LINES ARGS (RECOMMENDED: DO NOT CHANGE)
setting_unrecommended_to_mods_StartLimitIntervalSec = 0
setting_unrecommended_to_mods_RestartSec = 1
setting_unrecommended_to_mods_User = "root"
setting_unrecommended_to_mods_Restart = "always"
##name_of_addons_modules_folder = "SOCKS5"
##name_of_modular_configurations_folder = "ssh_config.d"
# =====================(RECOMMENDED: DO NOT CHANGE)
#
# Configuration of the systemd service (PLAYLOAD SAMPLE)
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
ExecStart=/bin/bash {script_location_to_be_called_by_the_service}
[Install]
WantedBy=multi-user.target
""".format( script_location_to_be_called_by_the_service = script_location_to_be_called_by_the_service,
            service_description = "{} Script - ( {} )".format(
                ConnectionName, 
                args.forwarding_ports.replace(":","->")
            ),
            setting_unrecommended_to_mods_StartLimitIntervalSec = setting_unrecommended_to_mods_StartLimitIntervalSec,
            setting_unrecommended_to_mods_RestartSec = setting_unrecommended_to_mods_RestartSec,
            setting_unrecommended_to_mods_User = setting_unrecommended_to_mods_User,
            setting_unrecommended_to_mods_Restart = setting_unrecommended_to_mods_Restart )
ParasitesConfigTool.init()
ParasitesConfigTool.setDestinationOfInjection(service_location_systemd_file)
ParasitesConfigTool.setPlayloadToInjection(automatic_socks5_connection_systemd_service)
ParasitesConfigTool.inject()
#
#
local_port,dest_port = args.forwarding_ports.split(":")
playload_bash_file_autoSOCKS5_sh="""
while :
do
    ssh -p {SSH_server_port} -i {SSH_id_filepath} -tt -R 0.0.0.0:{local_port}:localhost:{dest_port} -R 0.0.0.0:{dest_port}:localhost:{local_port} {SSH_server_username}@{SSH_server_domain_name}
    sleep 60
done
""".format( 
            SSH_server_port = SSH_server_port,
            SSH_id_filepath = args.SSH_id_filepath,
            SSH_server_username = SSH_server_username,
            SSH_server_domain_name = args.SSH_server_domain_name,
            local_port = local_port,
            dest_port = dest_port
          )
ParasitesConfigTool.init()
ParasitesConfigTool.setDestinationOfInjection(script_location_to_be_called_by_the_service)
ParasitesConfigTool.setPlayloadToInjection(playload_bash_file_autoSOCKS5_sh)
ParasitesConfigTool.inject()
# ~~~
system("sudo chmod +x {script_path}".format(
        script_path = script_location_to_be_called_by_the_service
    )
)
system("sudo systemctl enable --now {service_name}".format(
        service_name = "autotunnel_p{}.service".format(
            args.forwarding_ports.replace(":","-")
        )
    )
)
# ~~~ SOCKS5 SERVICE. DEPLOY DONE ~~~