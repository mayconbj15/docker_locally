import argparse
import os
import sys
import json,yaml

import subprocess
from subprocess import PIPE, run

global args

def get_arguments():
    parser = argparse.ArgumentParser(description='Script to run .NETCore project in docker locally')

    parser.add_argument("-a", "--aws", dest = "aws", default = "n", choices=['y', 'n'], help="If you want to get credentials in aws")
    parser.add_argument("-c", "--clean", dest = "dotnet_clean", default = "n", choices=['y', 'n'], help="Clean the dependencies of dotnet project")
    parser.add_argument("-d", "--detach", dest = "detach", default = "n", choices=['y', 'n'], help="Run container in background and print container ID")
    parser.add_argument("-di", "--debug-inside", dest = "debug_inside", default = "n", choices=['y', 'n'], help="Publish a container's port(s) to the host")
    parser.add_argument("-e", "--env", dest = "env", default = "dev", help="The env that container wiil run. This env is your role of aws")    
    parser.add_argument("-in", "--image-name", dest = "image_name", default = "dotnet-image", help="The name of the image that docker will build")
    parser.add_argument("-p", "--port", dest = "port", default = "8080:8080", help="Publish a container's port(s) to the host")
    parser.add_argument("-pn", "--project-name", dest = "project_name", default = "", required=True, help="The name of project")
    parser.add_argument("-wf", "--workspace-folder", dest = "workspace_folder", default = "", required=True, help="The path of the workspace folder of the project")
    
    global args
    args = parser.parse_args()

    print(args)

def readYamlFile(dir_path, base_command):
    with open(dir_path+'/values.yaml') as f:
        j = yaml.load(f, Loader=yaml.FullLoader)

        for x in j["env"]:
            base_command.append('--env')
            base_command.append(str(x['name']) + '=' + str(x['value']))        
        
    return base_command

def docker_build(dir_path):
    build_command = ['docker', 'build', '--tag', args.image_name, dir_path+'/.']
    run_command(build_command)

def docker_run(dir_path):
    base_command = ['docker', 'run', '--env-file', dir_path+'/env_file']
    
    base_command = readYamlFile(dir_path, base_command)
    
    #base_command.append('-it') # usar quando conseguir debugar dentro do container
    if args.detach == 'y':
        print('CONTAINER ID')
        base_command.append('-d')

    base_command.append('-p')
    base_command.append('8080:8080')
    base_command.append(args.image_name) 

    run_command(base_command)

def copy_runsh(base_path, dir_path):
    cp_command = ['cp', base_path + '/run.sh', dir_path]
    run_command(cp_command)

def copy_values(base_path, dir_path):
    cp_command = ['cp', base_path + '/src/main/kubernetes/dev/values.yaml', dir_path]
    run_command(cp_command)

def copy_envs(base_path, dir_path):
    copy_runsh(base_path, dir_path)
    copy_values(base_path, dir_path)
    
def publish(base_path, dir_path):
    pubish_command = ['dotnet', 'publish', base_path, '-o', dir_path+'/publish', '-c', 'release']
    run_command(pubish_command)

def run_command(command, shell=False):
    try:
        result_command = run(command, universal_newlines=True, shell=shell)
        print(result_command)
    except KeyboardInterrupt as err:
        print('\nCOMANDO CANCELADO')
    except:
        print('ERRO AO EXECUTAR COMANDO')

def get_credentials(dir_path):
    command = ['aws-vault exec ' + args.env + ' -- env | grep --color=never ^AWS_ > ' + dir_path+'/env_file']
    run_command(command, shell=True)

def stop_container():
    if args.detach == 'n':
        print('STOPING THE CONTAINER')
        command = ['docker stop $(docker ps -q)']
        run_command(command, shell=True)
    else:
        print('RUNNING CONTAINER IN DETACH MODE\n' + 'Type "docker ps" to see the container info')

def dotnet_clean():
    command = ['dotnet', 'clean', get_proj_file()]
    print(command)

def get_proj_file():
    return args.workspace_folder + '/src/' + args.project_name + '/' + args.project_name + '.csproj'

def dotnet_stages(dir_path):
    if args.dotnet_clean == 'y':
        dotnet_clean()
    
    publish(args.workspace_folder + '/src/' + args.project_name, dir_path)
    copy_envs(args.workspace_folder, dir_path)

def docker_stages(dir_path):
    docker_build(dir_path)
    docker_run(dir_path)
    stop_container()

def main():
    get_arguments()

    if args.aws == 'y':
        get_credentials(dir_path)

    dir_path = os.path.dirname(os.path.realpath(__file__))

    dotnet_stages(dir_path)
    
    docker_stages(dir_path)
    

if __name__ == "__main__":
    main()