import os
import subprocess
from subprocess import run
import yaml

import dotnet_docker as dd
import parser 
import aws

global args

def get_arguments():
    global args
    args = parser.get_arguments()

def set_env_debug():    
    dir_path = os.path.dirname(os.path.realpath(__file__)) + '/env_files/'

    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    dir_path += 'env_file.env'
    
    yaml_file = dd.read_yaml_file(args.workspace_folder + '/src/main/kubernetes/dev/values.yaml')
    
    env_file = yaml_to_env(yaml_file)
    
    print('env_file.env')
    print(env_file)

    f = open(dir_path, 'w')
    f.write(env_file)
    f.close()

def set_env_aws():
    dir_path = os.path.dirname(os.path.realpath(__file__)) + '/env_files/'

    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    dir_path += 'env_file_aws'
    
    if args.aws == 'y':
        get_credentials(dir_path)
        print('Credentials created')
    else:
        f = open(dir_path, 'w')
        f.write('')
        f.close()
      
def get_credentials(dir_path):
    command = aws.getCredentialsCommand(dir_path)
    run_command(command, shell=True)

def yaml_to_env(yaml_file):
    env = ''

    if yaml_file:
        for x in yaml_file["env"]:
            env += str(x['name']) + '=' + str(x['value']) + '\n'

    return env

def run_command(command, shell=False):
    try:
        result_command = run(command, universal_newlines=True, shell=shell)
        print(result_command)
    except KeyboardInterrupt as err:
        print('\nCOMANDO CANCELADO')
    except:
        print('ERRO AO EXECUTAR COMANDO')

def main():
    get_arguments()
    
    set_env_aws()
    
    set_env_debug()
    
    print('SCRIPT EXECUTADO')

if __name__ == "__main__":
    main()