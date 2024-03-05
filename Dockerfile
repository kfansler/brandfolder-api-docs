FROM python:3.12-rc-buster

COPY . /openapi
WORKDIR /openapi
RUN chmod 755 scripts/build.sh
RUN apt update --assume-yes
RUN pip3 install openapi-schema-validator==0.1.5
RUN pip3 install openapi-spec-validator==0.3.1 
RUN pip3 install ruamel.yaml
RUN apt install git-core curl build-essential openssl libssl-dev --assume-yes
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt install -y nodejs
RUN npm install swagger-repo 
RUN npm install redoc-cli 
RUN npm install postinstall-js 
RUN npm install speccy
RUN pip3 install jsonschema==3.0.2
RUN pip3 install flask
RUN scripts/build.sh

CMD python3 scripts/serve.py 
