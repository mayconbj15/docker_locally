## Scripts para executar docker localmente :whale:

### Pré-requisitos
- Python3
- Pasta **``certs``** que contém os certificados SSL
- Dockerfile (Dockerfile que irá montar sua imagem docker)
- O script **``dotnet-docker.py``**
- Adicionar a pasta e o arquivo em uma pasta base (recomenda-se o caminho **``$HOME/docker/``**)

### Como executar
#### Da pasta base
    python3 dotnet-docker.py -pn {project_name} -wf {workspace_folder}

As flags **``-pn``** e **``-wf``** são obrigatórias

#### Da pasta pasta do seu projeto usando VSCode

- Adicione o json abaixo no **``tasks.json``** na pasta **``.vscode``**

  ```json
    {
    "label": "docker-run",
        "command": "python3 $HOME/docker/dotnet-docker.py -wf ${workspaceFolder} -pn Inter.Crm.TrackSale.Integrator.AtualizaCampanhas.Job",
        "type": "shell",
        "group": {
            "kind": "test",
            "isDefault": true
            }
    }
    ```
- Execute a task pelo atráves do VSCode **``Ctrl + Shift + P ``** --> **``Run Tasks``** --> **``docker-run``** 
