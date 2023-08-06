#!/usr/bin/python
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2012, Edouard DUPIN, all right reserved
##
## @license MPL v2.0 (see license file)
##
import os
import sys
import fnmatch
import copy
# Local import
from . import host
from . import tools
from realog import debug
from . import env
from . import actions
import death.Arguments as arguments
import death.ArgElement as arg_element
is_init = False

debug.set_display_on_error("    ==========================\n    ==  Some error occured  ==\n    ==========================")


def init():
	global is_init;
	if is_init == True:
		return
	# import local island files
	list_of_island_files = tools.import_path_local(os.path.join(tools.get_current_path(__file__), 'actions'), base_name = env.get_system_base_name() + "*.py")
	actions.init(list_of_island_files)
	# import project actions files
	list_of_island_files = tools.import_path_local(env.get_island_root_path(), 2, [".island", ".git", "archive"], base_name = env.get_system_base_name() + "*.py")
	actions.init(list_of_island_files)
	is_init = True

# initialize the system ...
init()


debug.verbose("List of actions: " + str(actions.get_list_of_action()))

my_args = arguments.Arguments()
my_args.add_section("option", "Can be set one time in all case")
my_args.add("h", "help", desc="Display this help")
my_args.add("",  "version", desc="Display the application version")
my_args.add("v", "verbose", list=[
								["0","None"],
								["1","error"],
								["2","warning"],
								["3","info"],
								["4","debug"],
								["5","verbose"],
								["6","extreme_verbose"],
								], desc="display debug level (verbose) default =2")
my_args.add("c", "color", desc="Display message in color")
my_args.add("n", "no-fetch-manifest", haveParam=False, desc="Disable the fetch of the manifest")
my_args.add("F", "filter", haveParam=True, desc="Filter the action on a list of path or subpath: -f library")
my_args.add("f", "folder", haveParam=False, desc="Display the folder instead of the git repository name")
my_args.add("w", "wait", haveParam=True, desc="Wait between 2 acces on the server (needed when the server is really slow to remove ssh connection) (default=" + str(env.get_wait_between_sever_command()) + ")")
my_args.set_stop_at(actions.get_list_of_action())
local_argument = my_args.parse()

##
## @brief Display the help of this package.
##
def usage():
	color = debug.get_color_set()
	# generic argument displayed : 
	my_args.display()
	print("		Action availlable" )
	list_actions = actions.get_list_of_action();
	for elem in list_actions:
		print("			" + color['green'] + elem + color['default'])
		print("					" + actions.get_action_help(elem))
	"""
	print("		" + color['green'] + "init" + color['default'])
	print("			initialize a 'island' interface with a manifest in a git ")
	print("		" + color['green'] + "sync" + color['default'])
	print("			Syncronise the currect environement")
	print("		" + color['green'] + "status" + color['default'])
	print("			Dump the status of the environement")
	"""
	print("	ex: " + sys.argv[0] + " -c init http://github.com/atria-soft/manifest.git")
	print("	ex: " + sys.argv[0] + " sync")
	exit(0)

##
## @brief Display the version of this package.
##
def version():
	color = debug.get_color_set()
	import pkg_resources
	print("version: " + str(pkg_resources.get_distribution('island').version))
	foldername = os.path.dirname(__file__)
	print("source folder is: " + foldername)
	exit(0)

def check_boolean(value):
	if    value == "" \
	   or value == "1" \
	   or value == "true" \
	   or value == "True" \
	   or value == True:
		return True
	return False

# preparse the argument to get the verbose element for debug mode
def parse_generic_arg(argument, active):
	debug.extreme_verbose("parse arg : " + argument.get_option_name() + " " + argument.get_arg() + " active=" + str(active))
	if argument.get_option_name() == "help":
		if active == False:
			usage()
		return True
	elif argument.get_option_name() == "version":
		if active == False:
			version()
		return True
	elif argument.get_option_name()=="jobs":
		if active == True:
			#multiprocess.set_core_number(int(argument.get_arg()))
			pass
		return True
	elif argument.get_option_name()=="wait":
		if active == True:
			env.set_wait_between_sever_command(int(argument.get_arg()))
		return True
	elif argument.get_option_name() == "verbose":
		if active == True:
			debug.set_level(int(argument.get_arg()))
		return True
	elif argument.get_option_name() == "folder":
		if active == True:
			env.set_display_folder_instead_of_git_name(True)
		return True
	elif argument.get_option_name() == "color":
		if active == True:
			if check_boolean(argument.get_arg()) == True:
				debug.enable_color()
			else:
				debug.disable_color()
		return True
	elif argument.get_option_name() == "filter":
		if active == True:
			env.set_filter_command(str(argument.get_arg()))
		return True
	elif argument.get_option_name() == "no-fetch-manifest":
		if active == False:
			env.set_fetch_manifest(False)
		return True
	return False

# open configuration of island:
config_file = env.get_island_path_user_config()
if os.path.isfile(config_file) == True:
	sys.path.append(os.path.dirname(config_file))
	debug.debug("Find basic configuration file: '" + config_file + "'")
	# the file exist, we can open it and get the initial configuration:
	configuration_file = __import__(env.get_system_config_name()[:-3])
	
	if "get_exclude_path" in dir(configuration_file):
		data = configuration_file.get_exclude_path()
		debug.debug(" get default config 'get_exclude_path' val='" + str(data) + "'")
		env.set_exclude_search_path(data)
	
	if "get_default_color" in dir(configuration_file):
		data = configuration_file.get_default_color()
		debug.debug(" get default config 'get_default_color' val='" + str(data) + "'")
		parse_generic_arg(arg_element.ArgElement("color", str(data)), True)
	
	if "get_default_debug_level" in dir(configuration_file):
		data = configuration_file.get_default_debug_level()
		debug.debug(" get default config 'get_default_debug_level' val='" + str(data) + "'")
		parse_generic_arg(arg_element.ArgElement("verbose", str(data)), True)
	
	if "get_default_folder" in dir(configuration_file):
		data = configuration_file.get_default_folder()
		debug.debug(" get default config 'get_default_folder' val='" + str(data) + "'")
		parse_generic_arg(arg_element.ArgElement("folder", str(data)), True)
	
	if "get_default_wait" in dir(configuration_file):
		data = configuration_file.get_default_wait()
		debug.debug(" get default config 'get_default_wait' val='" + str(data) + "'")
		parse_generic_arg(arg_element.ArgElement("wait", str(data)), True)
	
	if "get_default_filter" in dir(configuration_file):
		data = configuration_file.get_default_filter()
		debug.debug(" get default config 'get_default_filter' val='" + str(data) + "'")
		parse_generic_arg(arg_element.ArgElement("filter", str(data)), True)
	


# parse default unique argument:
for argument in local_argument:
	parse_generic_arg(argument, True)

# remove all generic arguments:
new_argument_list = []
for argument in local_argument:
	if parse_generic_arg(argument, False) == True:
		continue
	new_argument_list.append(argument)

# now the first argument is: the action:
if len(new_argument_list) == 0:
	debug.warning("--------------------------------------")
	debug.warning("Missing the action to do ...")
	debug.warning("--------------------------------------")
	usage()


# TODO : move tin in actions ...
list_actions = actions.get_list_of_action();

action_to_do = new_argument_list[0].get_arg()
new_argument_list = new_argument_list[1:]
if action_to_do not in list_actions:
	debug.warning("--------------------------------------")
	debug.warning("Wrong action type : '" + str(action_to_do) + "' availlable list: " + str(list_actions) )
	debug.warning("--------------------------------------")
	usage()

# todo : Remove this
if     action_to_do != "init" \
   and os.path.exists(env.get_island_path()) == False:
	debug.error("Can not execute a island cmd if we have not initialize a config: '" + str("." + env.get_system_base_name()) + "' in upper 6 parent path")
	exit(-1)


ret = actions.execute(action_to_do, my_args.get_last_parsed()+1)

exit (ret)
# stop all started threads;
#multiprocess.un_init()


