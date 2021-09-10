#!/usr/bin/python3
#coding: utf-8

# LIBRARY'S IMPORTATION
from os import system 
from StudiousParasites.StudiousPlayloadInjector import Studious_Playload_Injector as PlayloadInjector
import argparse
from pathlib import Path
from copy import deepcopy

# args Parsing of the command line tool
parser = argparse.ArgumentParser()
parser.add_argument("-f","--force", action="store_true",
                    help="forcing and bypass all conditionnal lock of the guided configuration.")
parser.add_argument("-I","--inject-into-existing-targets", action="store_true",
                    help="enable the (to an configuration file already existing) target selection feature.")
parser.add_argument("-M","--modularity-config-mode", action="store_true",
                    help="enable the modularity mode of configuration injection feature.")
parser.add_argument("-0","--disable-config-writing-function", action="store_true",
                    help="disable all call of the final writes of the configuration.")
parser.add_argument("-D","--dump-selected-config", action="store_true",
                    help="dump the selected configuration targeted to load into an buffer.")
parser.add_argument("-B","--backup-creation-from-buffer", action="store_true",
                    help="create backup configurations files from data of the dumping buffer.")
args = parser.parse_args()

# DEFAULT DESTINATION OF THE PLAYLOAD INJECTION
playload_destination = "/etc/ssh/ssh_config"

# DEFAULT CONFIGURATIONS READY TO BE INJECTED INSIDE `/etc/ssh/ssh_config` FILE
short_name_Host = "socks5-n{current_configuration_number_of_SOCKS5_host}".format(
            current_configuration_number_of_SOCKS5_host = current_configuration_number_of_SOCKS5_host 
    )
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

# SYSTEMD PLAYLOAD TO SET THE SERVICE CONFIGURED INTO THE SYSTEM
service_description = "automatic SOCKS5 ssh reconnection"
current_configuration_number_of_SOCKS5_host = 1
script_location_to_be_called_by_the_service = "/opt/auto-connect-SOCKS5-number_{current_configuration_number_of_SOCKS5_host}.sh".format(
            current_configuration_number_of_SOCKS5_host = current_configuration_number_of_SOCKS5_host 
    )
# ???~~~???~~~???
ssh_addon_modules_filename = "SOCKS5_ssh_addon_modules_n-{current_configuration_number_of_SOCKS5_host}.conf".format(
            current_configuration_number_of_SOCKS5_host = current_configuration_number_of_SOCKS5_host 
    )
#   =================
# =====================(RECOMMENDED: DO NOT CHANGE)
# OTHER SPECIFICS CONFIGURATIONS LINES ARGS (RECOMMENDED: DO NOT CHANGE)
setting_unrecommended_to_mods_StartLimitIntervalSec = 0
setting_unrecommended_to_mods_RestartSec = 1
setting_unrecommended_to_mods_User = "root"
setting_unrecommended_to_mods_Restart = "always"
name_of_addons_modules_folder = "SOCKS5"
name_of_modular_configurations_folder = "ssh_config.d"
# =====================(RECOMMENDED: DO NOT CHANGE)



# little some injections ...
modularity_mode_folder_path = "/etc/ssh/{name_of_modular_configurations_folder}/{name_of_addons_modules_folder}".format(
            name_of_addons_modules_folder = name_of_addons_modules_folder,
            name_of_modular_configurations_folder = name_of_modular_configurations_folder
    )


# Automatic bash script for connect into SOCKS5 (PLAYLOAD SAMPLE)
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
# | | | |
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
            service_description = service_description,
            setting_unrecommended_to_mods_StartLimitIntervalSec = setting_unrecommended_to_mods_StartLimitIntervalSec,
            setting_unrecommended_to_mods_RestartSec = setting_unrecommended_to_mods_RestartSec,
            setting_unrecommended_to_mods_User = setting_unrecommended_to_mods_User,
            setting_unrecommended_to_mods_Restart = setting_unrecommended_to_mods_Restart )
# | | | |
# script for preparation of an new config file in an better way and more... terribly modular !! (PLAYLOAD SAMPLE)
modularity_mode_of_configuration_injection = """
sudo mkdir -p {modularity_mode_folder_path}
# line with grep and I don't know to reconfigure or add the missing include call of modules inside `/etc/ssh/ssh_config.d/`
sudo touch {modularity_mode_folder_path}/{ssh_addon_modules_filename}
""".format(
            ssh_addon_modules_filename = ssh_addon_modules_filename,
            name_of_modular_configurations_folder = name_of_modular_configurations_folder,
            modularity_mode_folder_path = modularity_mode_folder_path
          )

def test_target_path_existance(targeted_path, type_precision_mode=False):
    target_path = Path(targeted_path)
    if type_precision_mode:
        if target_path.is_file():
            return {"exists": True,"type": "file"} 
        elif target_path.is_dir():
            return {"exists": True,"type": "folder"}
        elif (not (target_path.exists())):
            return {"exists": False,"type": None}
    elif not type_precision_mode:
        return target_path.exists()

def test_target_path_and_wait_specifics_results(targeted_path, wait_exists_results = True, wait_type_results = None):
    results_of_testing = test_target_path_existance(targeted_path,True)
    if (type(wait_exists_results) != bool) or (type(wait_exists_results) != int):
        print("`wait_exists_results` argument of `test_target_path_and_wait_specifics_results` function require an boolean or an integer variable ! not an type : `{}` !".format(type(wait_exists_results)))
        exit(-1)
    else:
        if wait_exists_results:
            # wait the exists confirmation from the testing function
            if wait_type_results == None:
                # not an precise type for results wanted, just exists test
                return results_of_testing["exists"] == True
            elif wait_type_results == "file":
                # precise type `file` for results wanted, because that exist
                return (results_of_testing["exists"] == True) and (results_of_testing["type"] == "file")
            elif wait_type_results == "folder":
                # precise type `file` for results wanted, because that exist
                return (results_of_testing["exists"] == True) and (results_of_testing["type"] == "folder")
        elif not wait_exists_results:
            # wait the no-exists confirmation from the testing function
            return results_of_testing["exists"] == False

def check_config_number_availability(code_number,modularity_mode=False):
    testing_targets_list = []
    #
    script_location_to_be_called_by_the_service = "/opt/auto-connect-SOCKS5-number_{current_configuration_number_of_SOCKS5_host}.sh".format(
            current_configuration_number_of_SOCKS5_host = code_number 
    )
    #
    testing_targets_list.append(script_location_to_be_called_by_the_service)
    #
    if modularity_mode:
        #
        ssh_addon_modules_filename = "SOCKS5_ssh_addon_modules_n-{current_configuration_number_of_SOCKS5_host}.conf".format(
                current_configuration_number_of_SOCKS5_host = code_number 
        )
        #
        modularity_mode_folder_path = "/etc/ssh/{name_of_modular_configurations_folder}/{name_of_addons_modules_folder}".format(
                name_of_addons_modules_folder = name_of_addons_modules_folder,
                name_of_modular_configurations_folder = name_of_modular_configurations_folder
        )
        #
        checking_destination_filepath = "{modularity_mode_folder_path}/{ssh_addon_modules_filename}".format(
                modularity_mode_folder_path = modularity_mode_folder_path,
                ssh_addon_modules_filename = ssh_addon_modules_filename
        )
        #
        testing_targets_list.append(checking_destination_filepath)
    elif not modularity_mode:
        testing_targets_list.append(playload_destination)
    #
    tested_results_sample = [test_target_path_and_wait_specifics_results(i,wait_exists_results=False,wait_type_results=None) for i in testing_targets_list]
    if tested_results_sample.count(True) == len(tested_results_sample):
        return {
                "status": "available",
                "amount": 1.0,
                "module_files_mode": modularity_mode,
                "number_config_id": code_number
               }
    elif tested_results_sample.count(True) < len(tested_results_sample):
        if tested_results_sample.count(True) > 0:
            return {
                    "status": "partially",
                    "amount": (tested_results_sample.count(True) / (len(tested_results_sample)*1.0)),
                    "module_files_mode": modularity_mode,
                    "number_config_id": code_number
                }
        elif tested_results_sample.count(True) == 0:
            return {
                    "status": "unavailable",
                    "amount": 0.0,
                    "module_files_mode": modularity_mode,
                    "number_config_id": code_number
                }

def find_next_config_number_available(check_numbers_range=(1,1*10**6),modularity_mode=False):
    totally_used_id_numbers,partially_used_id_numbers=[],[]
    result_found = None
    flag_of_nothing = None
    for n in range(check_numbers_range[0],check_numbers_range[1]):
        sample_explained_results = check_config_number_availability(code_number=n,modularity_mode=modularity_mode)
        if (sample_explained_results["status"] == "available") and (sample_explained_results["amount"] == 1.0):
            flag_of_nothing = False
            result_found = n
            break
        if (sample_explained_results["status"] == "partially") and (sample_explained_results["amount"] < 1.0):
            partially_used_id_numbers.append(n)
            flag_of_nothing = False
        if (sample_explained_results["status"] == "unavailable") and (sample_explained_results["amount"] == 0.0):
            totally_used_id_numbers.append(n)
            if flag_of_nothing == None: 
                flag_of_nothing = True
    #
    return {"free_id_number":result_found, 
            "flag_of_nothing":flag_of_nothing, 
            "partially_used_id_numbers":partially_used_id_numbers, 
            "totally_used_id_numbers":totally_used_id_numbers}

#yeah that can be use for any languages ! Enjoy !
#                                                                                 EN     FR    DE   ES            EN     FR    DE    ES 
def YesOrNoQuestion( asked_question="Confirmation{YN_default_choice}",yes_words=["yes","oui","ja","sí"],no_words=["no","non","nein","no"],
                     YN_default_choice="yes", ask_loop_if_unknow_reply=True, case_sensitive=False, selected_index_reply_lists=None,
                     no_input_is_default_validation=True, upper_case_forced_wanted_reply = False, full_type_forced_wanted_reply = False
                   ):
    O_YN_default_choice = deepcopy(YN_default_choice)
    yes_char, no_char = O_YN_default_choice[0], no_words[yes_words.index(O_YN_default_choice)][0]
    while True:
        if selected_index_reply_lists != None:
            if (-1 < selected_index_reply_lists < len(yes_words)) and (-1 < selected_index_reply_lists < len(no_words)):
                if not full_type_forced_wanted_reply:
                    yes_char = yes_char[selected_index_reply_lists][0]
                    no_char = no_char[selected_index_reply_lists][0]
        if YN_default_choice == "yes":
            yes_char = yes_char.upper()
            no_char = no_char.lower()
        elif YN_default_choice == "no":
            yes_char = yes_char.lower()
            no_char = no_char.upper()
        #
        YN_default_choice = "({yes_char}/{no_char})?".format( yes_char = yes_char, no_char = no_char )
        ask_msg = asked_question.format(YN_default_choice=YN_default_choice)
        reply = input(ask_msg)
        if (no_input_is_default_validation) and (len(reply)==0): 
            if (O_YN_default_choice.lower() == "yes"):
                reply = True
            elif (O_YN_default_choice.lower() == "no"):
                reply = False
            else:
                reply = None
            break
        #
        if not case_sensitive:
            reply = reply.lower()
            YN_default_choice = YN_default_choice.lower()
        #
        elif case_sensitive:
            if upper_case_forced_wanted_reply:
                yes_words = [i.upper() for i in yes_words]
                no_words = [i.upper() for i in no_words]
                YN_default_choice = YN_default_choice.upper()
            if (selected_index_reply_lists != None):
                if (-1 < selected_index_reply_lists < len(yes_words)) and (-1 < selected_index_reply_lists < len(no_words)):
                    yes_words, no_words = list( yes_words[selected_index_reply_lists] ), list( no_words[selected_index_reply_lists] )
        if full_type_forced_wanted_reply:
            for w in yes_words:
                if w == reply:
                    return True
            for w in no_words:
                if w == reply:
                    return False
        if not full_type_forced_wanted_reply:
            for w in yes_words:
                if reply in w[0:len(reply)]:
                    return True
            for w in no_words:
                if reply in w[0:len(reply)]:
                    return False
        else:
            if not ask_loop_if_unknow_reply: 
                reply = None 
                break
    return reply
    

# customisation_asks steps
results_config_id_numbers = find_next_config_number_available(modularity=args.modularity_config_mode)
"""
1 - found an free number if `args.inject_into_existing_targets` are disabled, else he take existing targets lists for next
"""

"""
    1.1 - he attribute the number and call setters to inject value into data related
    1.2 - he made the declaration of defaults value for the `DEFAULT DESTINATION OF THE PLAYLOAD INJECTION`
    1.3 - he made declaration and injections generation(with the id_number) for `DEFAULT CONFIGURATIONS READY TO BE INJECTED INSIDE ssh_config filetype`
"""

"""
    ##if `args.inject_into_existing_targets` are disabled
    1.4 - he start interrogation

        A.1 - Ask questions to made the custom config data to injection can be ready at the end of program
            Questions )..:

            #if `args.inject_into_existing_targets` are disabled
            |Do you want customize the generated names of this configuration ? [N]|
                -|  
                1|  "short_name_Host [{short_name_Host}] (y/N) ?"
                2|  "script_location_to_be_called_by_the_service [{script_location_to_be_called_by_the_service}] (y/N) ?"
                3|  "ssh_addon_modules_filename [{ssh_addon_modules_filename}] (y/N) ?"
                4|  "script_location_to_be_called_by_the_service [{script_location_to_be_called_by_the_service}] (y/N) ?"
            |Do you want customize the default ssh configuration presets ? [Y]|
                -|
                1|  "User [{User}] (Y/n) ?"
                2|  "server_domain_name_or_ip_addr [{server_domain_name_or_ip_addr}] (Y/n) ?"
                3|  "ssh_destination_server_port [{ssh_destination_server_port}] (Y/n) ?"
                4|  "dynamic_port_of_proxy [{dynamic_port_of_proxy}] (y/N) ?"
                5|  "commented_IdentityFile [{commented_IdentityFile}] (Y/n) ?"
                !|  "~~~*~~~*~~~*~~~*~~~*~~~*~~*~~~*~~~*~~~*~~~*~~~*~~~"
                !|  "~~~*~~~*~~~*~~~*optionnal settings*~~~*~~~*~~~*~~~"
                !|  "~~~*~~~*~~~*~~~*~~~*~~~*~~*~~~*~~~*~~~*~~~*~~~*~~~"
                6|  "optionnal_setting_PasswordAuthentication [{optionnal_setting_PasswordAuthentication}] (y/N) ?"
                7|  "optionnal_setting_CheckHostIP [{optionnal_setting_CheckHostIP}] (y/N) ?"
            #if `args.modularity_config_mode` and `args.inject_into_existing_targets` are disabled
            |Do you want customize the default playload destination ? [N]|
                -|
                1|  "playload_destination [{playload_destination}] (y/N) ?"
                2|  "ssh_folder_of_user_path [{ssh_folder_of_user_path}] (y/N) ?"
    1.5 - injection of first playload in-memory (ssh custom configuration file)
"""
# ~~~ * ~~~ * ~~~ * ~~~ * ~~~ * ~~~ * ~~~ * ~~~ * ~~~ * ~~~ * ~~~ * ~~~ * ~~~ * ~~~ * ~~~
# Declaration and formating the playloads configuration for fast injections to the system
# ~~~ * ~~~ * ~~~ * ~~~ * ~~~ * ~~~ * ~~~ * ~~~ * ~~~ * ~~~ * ~~~ * ~~~ * ~~~ * ~~~ * ~~~
# SSH_CONFIG configuration (PLAYLOAD SAMPLE)
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
# | | | |


"""
2 - if `args.inject-into-existing-targets` is enabled the search focusing on unavailable and partially
"""


#if args.inject_into_existing_targets:


#inject the configuration of saved socks5 connection configuration to `/etc/ssh/ssh_config` at the end of file, writing in append mode


# Creation of the Object for Playload Injections from `studious-octo-tribble/StudiousParasites/StudiousPlayloadInjector.py`
ParasitesConfigTool = PlayloadInjector()
