import argparse
import yaml
import os

import dotnet_docker as dd

global args

def get_arguments():
    parser = argparse.ArgumentParser(description='Script to run .NETCore project in docker locally')

    parser.add_argument("-a", "--aws", dest = "aws", default = "n", choices=['y', 'n'], help="If you want to set env_file_aws")
    parser.add_argument("-pn", "--project-name", dest = "project_name", default = "", required=True, help="The name of project")
    parser.add_argument("-wf", "--workspace-folder", dest = "workspace_folder", default = "", required=True, help="The workspace path to the folder of the project")
    
    global args
    args = parser.parse_args()

def set_env_debug():    
    dir_path = os.path.dirname(os.path.realpath(__file__)) + '/env_files/env_file.env'
    
    yaml_file = dd.read_yaml_file(args.workspace_folder + '/src/main/kubernetes/dev/values.yaml')
    
    env_file = yaml_to_env(yaml_file)
    
    print('env_file.env')
    print(env_file)

    f = open(dir_path, 'w')
    f.write(env_file)
    f.close()

def set_env_aws():
    dir_path = os.path.dirname(os.path.realpath(__file__)) + '/env_files/env_file_aws'
    if args.aws == 'y':
        dd.get_credentials(dir_path)
        print('Credentials created')
    else:
        f = open(dir_path, 'w')
        f.write('')
        f.close()

def yaml_to_env(yaml_file):
    env = ''

    for x in yaml_file["env"]:
        env += str(x['name']) + '=' + str(x['value']) + '\n'

    return env

def main():
    get_arguments()
    set_env_debug()
    set_env_aws()

    print('SCRIPT EXECUTADO')

if __name__ == "__main__":
    main()