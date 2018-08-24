import argparse
import sys
import os

# TODO: config file?

# we could define some base dir and use relative paths
#BASE_DIR='/somewhere'

# Finds all the running services (directories) in the script's root directory
def find_all_running_services():
    # TODO: How to find if service is running?
    
    services = []

    root = os.path.abspath(os.getcwd())
    for item in os.listdir(root):
        if os.path.isdir(os.path.join(root, item)):
            #services.append(os.path.join(os.getcwd(), item)) # For absolute path
            services.append(item)
    
    return services

def shutdown_service(services_to_shutdown_list):
    for service in services_to_shutdown_list:
        # TODO: Fork new process with dummy robin command. See multiprocessing module
        # TODO: Try, except for robin command
        print "Shutting down running service: {}".format(service)

def validate_services(input_services):
    running_services = find_all_running_services()
    valid = []        
    
    for service in input_services:
        if service in running_services:
            valid.append(service)
        else:
            print "\'{}\' is not a running service".format(service)
    
    return valid

# Defining/parsing command-line arguments
parser = argparse.ArgumentParser(description="Shutdown Deployment Script")
parser.add_argument("-all", required=False, action="store_true", help="shutdown all running services")
parser.add_argument("-file", type=str, nargs="?", help="read service names from the file")
parser.add_argument("-services", type=str, nargs="+", help="list of services available to shutdown")
args = parser.parse_args()

# Priority order:
#   1. -all
#   2. -file
#   3. -services
if ((args.all) and (args.file == None) and (args.services == None)):        # -all
    shutdown_service(find_all_running_services())
elif ((not args.all) and (args.file != None) and (args.services == None)):  # -file
    try:
        services_list = []
        with open(args.file) as fin:
            for service in fin:
                services_list.append(service.replace("\n", ""))
        shutdown_service(validate_services(services_list))
    except IOError:
        print "Failed to open file: {}".format(args.file)
        print "Stopping..."
        sys.exit(1)
elif ((not args.all) and (args.file == None) and (args.services != None)):  # -services
    valid_running_services = validate_services(args.services)
    shutdown_service(valid_running_services)
else:
    parser.print_help()
