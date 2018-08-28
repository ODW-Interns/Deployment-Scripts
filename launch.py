import argparse
import os
import sys

from shutdown import find_all_running_services

def find_all_services_not_running():
    # Find all services that are not running and run these services
    # TODO: Do we have to check if the service is provisioned?
    # TODO: How to find if service is not running?

    # Temporary fix for now until we find out how to find services that are not running
    services = find_all_running_services()
    return services

# Returns a list of services that can be launched from a list of input
def validate_services(input_services_list):
    off_services = find_all_services_not_running()
    valid = []
    
    for service in input_services_list:
        if service in off_services:
            valid.append(service)
        else:
            print "\'{}\' is not a valid service to launch".format(service)
    
    return valid

def launch_services(valid_services):
    # TODO : Add forking functionality to execute robin commands concurrently
    for service in valid_services:
        print "Launching service {}".format(service)


if __name__ == "__main__":
    # Defining/parsing command-line arguments
    parser = argparse.ArgumentParser(description="Launch Deployment Script")
    parser.add_argument("-all", required=False, action="store_true", help="launch all running services")
    parser.add_argument("-file", type=str, nargs="?", help="read service names from the file")
    parser.add_argument("-services", type=str, nargs="+", help="list of services available to launch")
    args = parser.parse_args()

    # Priority order:
    #   1. -all
    #   2. -file
    #   3. -services
    if ((args.all) and (args.file == None) and (args.services == None)):        # -all
        launch_services(find_all_services_not_running())
    elif ((not args.all) and (args.file != None) and (args.services == None)):  # -file
        try:
            services_list = []
            with open(args.file) as fin:
                for service in fin:
                    services_list.append(service.replace("\n", ""))
            lanuch_services(validate_services(services_list))
        except IOError:
            print "Failed to open file: {}".format(args.file)
            print "Stopping..."
            sys.exit(1)
    elif ((not args.all) and (args.file == None) and (args.services != None)):  # -services
        valid_services = validate_services(args.services)
        launch_services(valid_services)
    else:
        parser.print_help()

    print "Exiting"

