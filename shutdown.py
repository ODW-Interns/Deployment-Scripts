import argparse
import sys
import os
from multiprocessing import Process

import time #temporary

# we could define some base dir and use relative paths
#BASE_DIR='/somewhere'

# Finds all the running services in the script's root directory.
def find_all_running_services():
    # TODO: How to find if service is running?
    services = []

    root = os.path.abspath(os.getcwd())
    for item in os.listdir(root):
        if os.path.isdir(os.path.join(root, item)):
            services.append(item)
    
    return services

# Executes the necessary robin commands to shutdown a service.
def shutdown_robin(service_directory):
    # TODO: Execute and error handle the robin commands here
    
    print "Shutting down running service: {}".format(service_directory)

    # This is for debugging purposes. Delete when replaced.
    seconds = 10
    print "Waiting {} seconds".format(seconds)
    time.sleep(seconds) 

# Forks multiple processes to execute the robin commands concurrently.
def shutdown_services(services_to_shutdown_list):
    processes = []
    
    for service in services_to_shutdown_list:
        newProcess = Process(target=shutdown_robin, args={service})
        newProcess.start()
        processes.append(newProcess)

    for process in processes:
        process.join()

    print "All provided services have been shut down."

# Returns a list of services that can be shut down from a list of input
def validate_services(input_services_list):
    running_services = find_all_running_services()
    valid = []        
    
    for service in input_services_list:
        if service in running_services:
            valid.append(service)
        else:
            print "\'{}\' is not a running service".format(service)
    
    return valid

if __name__ == "__main__":
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

    print "Exiting"