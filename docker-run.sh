#!/bin/bash

#Argumento do caminho do projeto
pathProject=$(pwd)
echo $pathProject

path=$HOME/docker
echo $path

cp run.sh $path
cp $pathProject/src/main/kubernetes/values.yaml $path

#Gerar o publish do projeto na sua pasta
dotnet publish $1 -o $path/publish -c release

#Fazer o build da imagem
docker build --tag dotnet-image $path/.

docker run -p 8080:8080 dotnet-image

