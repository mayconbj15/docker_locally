import argparse
import os
import yaml

import subprocess
from subprocess import run

global args

def get_arguments():
    parser = argparse.ArgumentParser(description='Script to run .NETCore project in docker locally')

    parser.add_argument("-a", "--aws", dest = "aws", default = "n", choices=['y', 'n'], help="If you want to get credentials in aws")
    parser.add_argument("-c", "--clean", dest = "dotnet_clean", default = "n", choices=['y', 'n'], help="Clean the dependencies of dotnet project")
    parser.add_argument("-d", "--detach", dest = "detach", default = "n", choices=['y', 'n'], help="Run container in background and print container ID")
    parser.add_argument("-di", "--debug-inside", dest = "debug_inside", default = "n", choices=['y', 'n'], help="Publish a container's port(s) to the host")
    parser.add_argument("-e", "--env", dest = "env", default = "uat", help="The env that container wiil run. This env is your role of aws")    
    parser.add_argument("-in", "--image-name", dest = "image_name", default = "dotnet-image", help="The name of the image that docker will build")
    parser.add_argument("-p", "--port", dest = "port", default = "8080:8080", help="Publish a container's port(s) to the host")
    parser.add_argument("-pn", "--project-name", dest = "project_name", default = "", required=True, help="The name of project")
    parser.add_argument("-r", "--remove", dest = "remove", default = "n", choices=['y', 'n'], help="Remove the container after the execution")
    parser.add_argument("-wf", "--workspace-folder", dest = "workspace_folder", default = "", required=True, help="The workspace path to the folder of the project")
    
    global args
    args = parser.parse_args()

#dotnet stages functions
def dotnet_stages(dir_path):
    if args.dotnet_clean == 'y':
        dotnet_clean()
    
    publish(args.workspace_folder + '/src/' + args.project_name, dir_path)
    copy_envs(args.workspace_folder, dir_path)

def dotnet_clean():
    command = ['dotnet', 'clean', get_proj_file()]
    print(command)

def publish(base_path, dir_path):
    pubish_command = ['dotnet', 'publish', base_path, '-o', dir_path+'/publish', '-c', 'release']
    run_command(pubish_command)

def copy_envs(base_path, dir_path):
    copy_runsh(base_path, dir_path)
    copy_values(base_path + '/src/main/kubernetes/dev/values.yaml', dir_path + '/env_files/env_file.env')

def copy_runsh(base_path, dir_path):
    path_runsh = base_path + '/run.sh'

    if os.path.exists(base_path) and args.debug_inside == 'n':
        cp_command = ['cp', path_runsh, dir_path]
        run_command(cp_command)
    else: 
        print('run.sh NOT FOUND')

def copy_values(from_path, to_path):
    yaml_file = read_yaml_file(from_path)

    env_file = yaml_to_env(yaml_file)

    try:
        f = open(to_path, 'w')
        f.writelines(env_file)
        f.close()
    except:
        print('Erro ao abrir arquivo ' + to_path)
    
def yaml_to_env(yaml_file):
    env = ''

    for x in yaml_file["env"]:
        env += str(x['name']) + '=' + str(x['value']) + '\n'

    return env

def get_proj_file():
    return args.workspace_folder + '/src/' + args.project_name + '/' + args.project_name + '.csproj'

#docker stages functions
def docker_stages(dir_path):
    docker_build(dir_path)
    docker_run(dir_path)
    stop_container()

def docker_build(dir_path):
    build_command = ['docker', 'build', '--tag', args.image_name, dir_path + '/.']
    run_command(build_command)

def docker_run(dir_path):
    base_command = ['docker', 'run']
    
    if args.detach == 'y':
        print('CONTAINER ID')
        base_command.append('-d')

    base_command.append('-p')
    base_command.append(args.port)

    path_env_file_aws = dir_path + '/env_files/env_file_aws'
    path_env_file = dir_path + '/env_files/env_file.env'

    if os.path.exists(path_env_file_aws):
        base_command.append('--env-file')
        base_command.append(path_env_file_aws)

    if os.path.exists(path_env_file):
        base_command.append('--env-file')
        base_command.append(path_env_file) 
    #base_command.append('-it') # usar quando conseguir debugar dentro do container
    base_command.append(args.image_name) 

    run_command(base_command)

def stop_container():
    if args.detach == 'n':
        print('STOPING THE CONTAINER')
        command_stop = ['docker stop $(docker ps -q -l)']
        run_command(command_stop, shell=True)
        if args.remove == 'y':
            print('REMOVING THE CONTAINER')
            command_remove = ['docker rm $(docker ps -q -l)']
            run_command(command_remove, shell=True)
    else:
        print('RUNNING CONTAINER IN DETACH MODE\n' + 'Type "docker ps" to see the container info')

def read_yaml_file(dir_path):
    try:
        f = open(dir_path)
        y = yaml.load(f, Loader=yaml.FullLoader)
        f.close()
        return y
    except:
        print('Erro ao abrir arquivo ' + dir_path)

def run_command(command, shell=False):
    try:
        result_command = run(command, universal_newlines=True, shell=shell)
        print(result_command)
    except KeyboardInterrupt as err:
        print('\nCOMANDO CANCELADO')
    except:
        print('ERRO AO EXECUTAR COMANDO')

#aws functions
def get_credentials(dir_path):
    command = ['aws-vault exec ' + args.env + ' -- env | grep --color=never ^AWS_ > ' + dir_path]
    run_command(command, shell=True)

def main():
    get_arguments()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    if args.aws == 'y':
        get_credentials(dir_path + '/env_files/env_file_aws')

    dotnet_stages(dir_path)
    
    docker_stages(dir_path)
    
if __name__ == "__main__":
    main()