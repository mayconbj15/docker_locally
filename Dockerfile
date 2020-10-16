FROM mcr.microsoft.com/dotnet/core/aspnet:3.1.8-bionic

LABEL maintainer="Maycon Jesus <maycon.jesus@bancointer.com.br>"
LABEL maintainer="Maycon Jesus <mayconbj15@gmail.com.br>"

# Instala certificados
RUN echo "Copia Certificados"
COPY certs/*.* /usr/local/share/ca-certificates/
RUN ls /usr/local/share/ca-certificates/

RUN echo "Instala Certificados"
RUN apt-get update \
    && apt-get upgrade \    
    && apt-get install -y wget \
    ca-certificates \
    && update-ca-certificates 2>/dev/null || true \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt

RUN echo "Copia do ambiente de build"
COPY ./publish /opt/
COPY run.sh .

EXPOSE 8080

ENTRYPOINT ["sh", "run.sh"]
#ENTRYPOINT ["/bin/sh"] #Retire this comment to debug inside container, and add -it flag to docker run command