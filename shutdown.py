import argparse
import sys
import os

# TODO: config file?

# we could define some base dir and use relative paths
#BASE_DIR='/somewhere'

# Finds all the services (directories) in the script's root directory
def find_all_services():
    services = []

    root = os.path.abspath(os.getcwd())
    for item in os.listdir(root):
        if os.path.isdir(os.path.join(root, item)):
            #services.append(os.path.join(os.getcwd(), item)) # For absolute path
            services.append(item)
    
    return services

def shutdown_service(service_list):
    # TODO: loop through service_list and loop through find_all_services()
        # if serviceName is in both service_list and find_all_services()
            # fork new process
            # fork process to shutdown
    return

def shutdown_service_from_file(fileName):
    with open(fileName) as fin:
        for line in fin:
            #shutdown_service(line)
            pass

def shutdown_all():
    pass

parser = argparse.ArgumentParser(description="Shutdown Deployment Script")
parser.add_argument("-all", required=False, action="store_true", help="shutdown all running services")
parser.add_argument("-file", type=str, nargs="?", help="read service names from the file")
parser.add_argument("-services", type=str, nargs="+", help="list of services available to shutdown")

args = parser.parse_args()
        
if (args.all):
    print "Shutting down all running services..."
    shutdown_all()
elif (args.file != None):
    filename = str(args.file)
    print "Shutting down running services specified in file: " + filename    
    shutdown_service_from_file(filename)
elif (args.services != None):
    print "List of Services: " + str(args.services)
    shutdown_service(args.services)
else:
    parser.print_help()
    pass
