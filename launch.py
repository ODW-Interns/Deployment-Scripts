import argparse
import sys
import os
import time
from shutdown import get_all_services, fork_process_per_service



# Checks to see if the provided input corresponds to what is actually there.
def validate_services(input_services_list):
    actual_services_list = get_all_services()
    valid = []
    
    for service in input_services_list:
        if service in actual_services_list:
            valid.append(service)
        else:
            print "\'{}\' is not a valid service".format(service)
    
    return valid


# Executes the necessary robin commands to launch a single service.
def launch_service(service_name):

    print "Launching service {}".format(service_name)

    # TODO: Robin command to launch a service
    # TODO: Print error if couldn't launch

    # This is for debugging purposes. Delete when replaced.
    seconds = 10
    print "Waiting {} seconds".format(seconds)
    time.sleep(seconds) 



if __name__ == "__main__":
    start_time = time.time()

    # Defining/parsing command-line arguments
    parser = argparse.ArgumentParser(description="Launch Deployment Script")
    parser.add_argument("-all", required=False, action="store_true", help="launch all running services")
    parser.add_argument("-file", type=str, nargs="?", help="read service names from the file")
    parser.add_argument("-services", type=str, nargs="+", help="list of services available to launch")
    args = parser.parse_args()

    if ((args.all) and (args.file == None) and (args.services == None)):        # -all
        fork_process_per_service(get_all_services(), launch_service)
        
    elif ((not args.all) and (args.file != None) and (args.services == None)):  # -file
        try:
            services_list = []
            with open(args.file) as fin:
                for service in fin:
                    services_list.append(service.replace("\n", ""))
            fork_process_per_service(validate_services(services_list), launch_service)
        except IOError:
            print "Failed to open file: {}".format(args.file)
            print "Stopping..."
            sys.exit(1)
    elif ((not args.all) and (args.file == None) and (args.services != None)):  # -services
        fork_process_per_service(validate_services(args.services), launch_service)
    else:
        parser.print_help()

    print "Exiting (Total Runtime: {0:.2f}ms".format((time.time() - start_time) * 1000)