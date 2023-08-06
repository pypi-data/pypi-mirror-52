#!/usr/bin/python
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2012, Edouard DUPIN, all right reserved
##
## @license MPL v2.0 (see license file)
##

from realog import debug
from island import tools
from island import env
from island import config
from island import commands
from island import multiprocess
import os

##
## @brief Get the global description of the current action
## @return (string) the description string (fist line if reserved for the overview, all is for the specific display)
##
def help():
	return "Init a island repository (need 'fetch' after)"

##
## @brief Add argument to the specific action
## @param[in,out] my_args (death.Arguments) Argument manager
## @param[in] section Name of the currect action
##
def add_specific_arguments(my_args, section):
	my_args.add("b", "branch", haveParam=True, desc="Select branch to display")
	my_args.add("m", "manifest", haveParam=True, desc="Name of the manifest")

##
## @brief Execute the action required.
##
## @return error value [0 .. 50] the <0 value is reserved system ==> else, what you want.
##         None : No error (return program out 0)
##         -5   : env.ret_manifest_is_not_existing      : Manifest does not exit
##         -10  : env.ret_action_is_not_existing        : ACTION is not existing
##         -11  : env.ret_action_executing_system_error : ACTION execution system error
##         -12  : env.ret_action_wrong_parameters       : ACTION Wrong parameters
##         -13  : env.ret_action_partial_done           : ACTION partially done
##
def execute(_arguments):
	if len(_arguments) == 0:
		debug.error("Missing argument to execute the current action ...")
	
	# the configuration availlable:
	branch = "master"
	manifest_name = "default.xml"
	address_manifest = ""
	for elem in _arguments:
		if elem.get_option_name() == "branch":
			debug.info("find branch name: '" + elem.get_arg() + "'")
			branch = elem.get_arg()
		elif elem.get_option_name() == "manifest":
			debug.info("find mmanifest name: '" + elem.get_arg() + "'")
			manifest_name = elem.get_arg()
		elif elem.get_option_name() == "":
			if address_manifest != "":
				debug.error("Manifest adress already set : '" + address_manifest + "' !!! '" + elem.get_arg() + "'")
			address_manifest = elem.get_arg()
		else:
			debug.error("Wrong argument: '" + elem.get_option_name() + "' '" + elem.get_arg() + "'")
	
	if address_manifest == "":
		debug.error("Init: Missing manifest name")
	
	debug.info("Init with: '" + address_manifest + "' branch='" + branch + "' name of manifest='" + manifest_name + "'")
	
	
	# check if .XXX exist (create it if needed)
	if     os.path.exists(env.get_island_path()) == True \
	   and os.path.exists(env.get_island_path_config()) == True \
	   and os.path.exists(env.get_island_path_manifest()) == True:
		debug.error("System already init: path already exist: '" + str(env.get_island_path()) + "'")
	tools.create_directory(env.get_island_path())
	# check if the git of the manifest if availlable
	
	# create the file configuration:
	conf = config.get_unique_config()
	conf.set_manifest(address_manifest)
	conf.set_branch(branch)
	conf.set_manifest_name(manifest_name)
	conf.store()
	
	#clone the manifest repository
	cmd = "git clone " + address_manifest + " --branch " + branch + " " + env.get_island_path_manifest()
	
	debug.info("clone the manifest")
	ret = multiprocess.run_command_direct(cmd)
	
	if ret == "":
		return True
	
	if ret == False:
		# all is good, ready to get the system work corectly
		return True
	debug.info("'" + ret + "'")
	debug.error("Init does not work")
	return False


