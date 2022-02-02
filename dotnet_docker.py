import os
import subprocess
from subprocess import run
import yaml

import parser 
import aws

global args

def get_arguments():
    global args
    args = parser.get_arguments()

#dotnet stages functions
def dotnet_stages(dir_path):
    if args.dotnet_clean == 'y':
        dotnet_clean()
    
    publish(args.workspace_folder + '/src/' + args.project_namespace, dir_path)
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
    return args.workspace_folder + '/src/' + args.project_namespace + '/' + args.project_namespace + '.csproj'

#docker stages functions
def docker_stages(dir_path):
    docker_build(dir_path)
    docker_run(dir_path)
    stop_container()

def get_tag_arg(dotnet_version):
    if "3.1" in dotnet_version:
        return "3.1.21-bionic"

    if "5.0" in dotnet_version:
        return "5.0.12-buster-slim"

    if "6.0" in dotnet_version:
        return "6.0.0-bullseye-slim"

    return "5.0.12-buster-slim"

def docker_build(dir_path):    
    tag_arg = get_tag_arg(args.dotnet_version)
    build_command = ['docker', 'build', '--tag', args.image_name, '--build-arg', f'TAG={tag_arg}', dir_path + '/.']    
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
        return ''

def run_command(command, shell=False):    
    print(f"\n{' '.join(command)}\n")    
    try:
        result_command = run(command, universal_newlines=True, shell=shell, check=True)
        print(result_command)            
    except KeyboardInterrupt as err:
        print('\nCOMANDO CANCELADO')
    except Exception as ex:
        print('ERRO AO EXECUTAR COMANDO:', ex)
        raise

#aws functions
def get_credentials(dir_path):
    command = aws.getCredentialsCommand(dir_path)
    run_command(command, shell=True)

def main():
    get_arguments()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    if not os.path.exists(dir_path + '/env_files'):
        os.mkdir(dir_path + '/env_files')

    if not os.path.exists(dir_path + '/certs'):
        os.mkdir(dir_path + '/certs')

    if args.aws == 'y':
        get_credentials(dir_path + '/env_files/env_file_aws')

    dotnet_stages(dir_path)
    
    docker_stages(dir_path)
    
if __name__ == "__main__":
    main()
