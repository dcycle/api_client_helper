FROM python:3

WORKDIR /usr/src/app

RUN pip3 install requests pyyaml deepmerge jsonpath-ng

COPY . .

ENTRYPOINT [ "python3", "./api_client_helper.py" ]
