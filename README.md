## Scripts para executar docker localmente :whale:

### Pré-requisitos
- Python3
- Docker instalado na sua máquina
- Pasta **``certs``** que contém os certificados SSL (opcional para quem não irá fazer requisições HTTPS que necessitam de certificação)
- [Dockerfile](https://github.com/mayconbj15/docker-scripts/blob/master/Dockerfile) (Dockerfile que irá montar sua imagem docker)
- O script [dotnet-docker.py](https://github.com/mayconbj15/docker-scripts/blob/master/dotnet-docker.py)
- Adicionar a pasta e o arquivo em uma pasta base (recomenda-se o caminho **``$HOME/docker-locally/``**)

### Como executar
#### Da pasta base
    python3 dotnet-docker.py -pn {project_name} -wf {workspace_folder}

As flags **``-pn``** e **``-wf``** são obrigatórias

#### Da pasta do seu projeto usando VSCode

- Adicione o json abaixo no **``tasks.json``** na pasta **``.vscode``**

  ```json
    {
    "label": "docker-run",
        "command": "python3 $HOME/docker-locally/dotnet-docker.py -wf ${workspaceFolder} -pn {projectName}",
        "type": "shell",
        "group": {
            "kind": "test",
            "isDefault": true
            }
    }
    ```
- Execute a task pelo atráves do VSCode **``Ctrl + Shift + P ``** --> **``Run Tasks``** --> **``docker-run``** 

### Argumentos do script 

#### Argumentos obrigatórios
- ``-pn PROJECT_NAME, --project-name PROJECT_NAME The name of project``

- ``-wf WORKSPACE_FOLDER, --workspace-folder WORKSPACE_FOLDER The workspace path to the folder of the project``

#### Argumentos opcionais
- ``-h, --help show this help message and exit``
  
- ``-a {y,n}, --aws {y,n} If you want to get credentials in aws``

- ``-c {y,n}, --clean {y,n} Clean the dependencies of dotnet project``
  
- ``-d {y,n}, --detach {y,n} Run container in background and print container ID``

- ``-di {y,n}, --debug-inside {y,n} Publish a container's port(s) to the host``

- ``-e ENV, --env ENV     The env that container wiil run. This env is your role of aws``

- ``-in IMAGE_NAME, --image-name IMAGE_NAME The name of the image that docker will build``

- ``-p PORT, --port PORT  Publish a container's port(s) to the host``
  
- ``-r REMOVE, --remove REMOVE Remove the container after the execution``
