import argparse
import sys
import os
import time
from multiprocessing import Process

# Temporary. Replace with actual systems directory found on the EC2 Instance.
# Ideally, place this in a config file.
SYSTEMS_DIR = os.path.abspath(os.getcwd())

# ----------------------------------------------
# Utility Functions.
# TODO: Move to utility module

# Forks multiple processes to execute the robin commands concurrently.
def fork_process_per_service(services_list, fork_function):
    processes = []
    
    for service in services_list:
        newProcess = Process(target=fork_function, args={service})
        newProcess.start()
        processes.append(newProcess)

    for process in processes:
        process.join()



# Gets all directories in the SYSTEMS_DIR. Each directory represents a service.
def get_all_services():
    services = []

    # Get all the directories in the script's working directory.
    # Each directory is assumed to be a service.
    for item in os.listdir(SYSTEMS_DIR):
        if os.path.isdir(os.path.join(SYSTEMS_DIR, item)):
            services.append(item)
    
    return services

# ----------------------------------------------



# Executes the necessary robin commands to shutdown a single service.
def shutdown_service(service_name):    
    print "Shutting down running service: {}".format(service_name)

    # TODO: Robin command to shut down service
    # TODO: Print error if couldn't shut down

    # This is for debugging purposes. Delete when replaced.
    seconds = 10
    print "Waiting {} seconds".format(seconds)
    time.sleep(seconds) 



# Checks to see if the provided input corresponds to what is actually there.
def validate_services(input_services_list):
    actual_services_list = get_all_services()
    valid_services = []
    
    for service in input_services_list:
        if service in actual_services_list:
            valid_services.append(service)
        else:
            print "\'{}\' is not a valid service".format(service)
    
    return valid_services



if __name__ == "__main__":
    start_time = time.time()

    # Defining/parsing command-line arguments
    parser = argparse.ArgumentParser(description="Shutdown Deployment Script")
    parser.add_argument("-all", required=False, action="store_true", help="shutdown all running services")
    parser.add_argument("-file", type=str, nargs="?", help="read service names from the file")
    parser.add_argument("-services", type=str, nargs="+", help="list of services available to shutdown")
    args = parser.parse_args()

    if ((args.all) and (args.file == None) and (args.services == None)):        # -all
        fork_process_per_service(get_all_services(), shutdown_service)
    elif ((not args.all) and (args.file != None) and (args.services == None)):  # -file
        try:
            services_list = []
            with open(args.file) as fin:
                for service in fin:
                    services_list.append(service.replace("\n", ""))
            fork_process_per_service(validate_services(services_list), shutdown_service)
        except IOError:
            print "Failed to open file: {}".format(args.file)
            print "Stopping..."
            sys.exit(1)
    elif ((not args.all) and (args.file == None) and (args.services != None)):  # -services
        fork_process_per_service(validate_services(args.services), shutdown_service)
    else:
        parser.print_help()

    print "Exiting (Total Runtime: {0:.2f}ms".format((time.time() - start_time) * 1000)