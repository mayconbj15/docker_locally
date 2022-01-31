import argparse
global args 

def get_arguments():
    parser = argparse.ArgumentParser(description='Script to run .NETCore project in docker locally')

    parser.add_argument("-a", "--aws", dest = "aws", default = "n", choices=['y', 'n'], help="If you want to get credentials in aws")
    parser.add_argument("-c", "--clean", dest = "dotnet_clean", default = "n", choices=['y', 'n'], help="Clean the dependencies of dotnet project")
    parser.add_argument("-d", "--detach", dest = "detach", default = "n", choices=['y', 'n'], help="Run container in background and print container ID")
    parser.add_argument("-di", "--debug-inside", dest = "debug_inside", default = "n", choices=['y', 'n'], help="Publish a container's port(s) to the host")
    parser.add_argument("-e", "--env", dest = "env", default = "uat-service-bus", help="The env that container wiil run. This env is your role of aws")    
    parser.add_argument("-in", "--image-name", dest = "image_name", default = "dotnet-image", help="The name of the image that docker will build")
    parser.add_argument("-p", "--port", dest = "port", default = "8080:8080", help="Publish a container's port(s) to the host")
    parser.add_argument("-pn", "--project-name", dest = "project_name", default = "", required=True, help="The name of project")
    parser.add_argument("-st", "--duration_time", dest = "duration_time", type=int, default=1, help="Duration of the temporary or assume-role session")
    parser.add_argument("-r", "--remove", dest = "remove", default = "n", choices=['y', 'n'], help="Remove the container after the execution")
    parser.add_argument("-wf", "--workspace-folder", dest = "workspace_folder", default = "", required=True, help="The workspace path to the folder of the project")
    parser.add_argument("-dv", "--dotnet-version", dest = "dotnet_version", default = "", help="The dotnet version of dotnet project")

    global args 
    args = parser.parse_args()
    
    return args 

def getArgs():

    return args 