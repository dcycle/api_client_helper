API Client Helper
=====

Interact with various APIs in Python.

This project currently has plugins for

* [DigitalOcean](https://developers.digitalocean.com/documentation/v2/) to manage Virtual Machines;
* [Acquia](https://docs.acquia.com/cloud-platform/develop/api/) to manage Drupal cloud hosting.

Each plugin is in its ./plugins/* folder, for example ./plugins/acquia or ./plugins/digitalocean, and you can copy-paste those as starters for your own plugins.

How to use with Docker
-----

    TOKEN=my-api-token
    docker run --rm \
      --env TOKEN="$TOKEN" \
      dcycle/api_client_helper:1 digitalocean accountinfo

To create a new DigitalOcean droplet (virtual machine):

    TOKEN=my-api-token
    LOCATION=nyc3
    SIZE=8gb
    NAME=some-new-droplet
    IMAGE=docker-18-04
    SSH_FINGERPRINT=a1:b2:c3:d4:a1:b2:c3:d4:a1:b2:c3:d4:a1:b2:c3:d4
    docker run --rm \
      --env TOKEN="$TOKEN" \
      --env LOCATION="$LOCATION" \
      --env SIZE="$SIZE" \
      --env NAME="$NAME" \
      --env IMAGE="$IMAGE" \
      --env SSH_FINGERPRINT="$SSH_FINGERPRINT" \
      --env DEBUG=1 \
      dcycle/api_client_helper:1 digitalocean newdroplet

To get info about a DigitalOcean droplet with its ID:

    ID=1234567
    TOKEN=my-api-token
    docker run --rm \
      --env TOKEN="$TOKEN" \
      --env ID="$ID" \
      dcycle/api_client_helper:1 digitalocean dropletinfo

To get info about all DigitalOcean droplets:

    TOKEN=my-api-token
    docker run --rm \
      --env TOKEN="$TOKEN" \
      dcycle/api_client_helper:1 digitalocean listdroplets

To delete a DigitalOcean droplet with its ID:

    ID=1234567
    TOKEN=my-api-token
    docker run --rm \
      --env TOKEN="$TOKEN" \
      --env ID="$ID" \
      dcycle/api_client_helper:1 digitalocean deletedroplet

To get your Acquia account info:

    KEY=my-api-key
    SECRET=my-api-secret
    docker run --rm \
      --env KEY="$KEY" \
      --env SECRET="$SECRET" \
      dcycle/api_client_helper:1 acquia accountinfo

To switch the code on an Acquia environment:

  TAG=my-application-tag
  KEY=my-api-key
  SECRET=my-api-secret
  ENVID=my-environment
  BRANCH=tags/"$TAG"
  docker run --rm \
    --env KEY="$KEY" \
    --env SECRET="$SECRET" \
    --env ENVID="$ENVID" \
    --env BRANCH="$BRANCH" \
    dcycle/api_client_helper:1 acquia switch

Debugging
-----

If you set the DEBUG environment variable to 1, you will see debug info:

    TOKEN=my-api-token
    docker run --rm \
      --env TOKEN="$TOKEN" \
      --env DEBUG=1 \
      dcycle/api_client_helper:1 digitalocean accountinfo




    KEY=my-api-key
    SECRET=my-api-secret


    docker run --rm \
      --env KEY="$KEY" \
      --env SECRET="$SECRET" \
      --entrypoint /bin/bash \
      dcycle/api_client_helper:1 -c 'python3 ./acquia_api_test.py'

  KEY=my-api-key
  SECRET=my-api-secret
  ORG_UUID=my-org-uuid
  docker run --rm \
    --env KEY="$KEY" \
    --env SECRET="$SECRET" \
    --env ORG_UUID="$ORG_UUID" \
    --entrypoint /bin/bash \
    dcycle/api_client_helper:1 -c 'python3 ./acquia_api_test.py'




    ENV=my-first-vm
    TOKEN=my-api-token
    TOKEN=my-api-token
    SSH_FINGERPRINT=my-ssh-fingerprint
    REGION=nyc3
    SIZE=8gb
    IMAGE=docker-18-04
    docker run --rm \
      --env NAME="$NAME" \
      --env TOKEN="$TOKEN" \
      --env SSH_FINGERPRINT="$SSH_FINGERPRINT" \
      --env REGION="$LOCATION" \
      --env IMAGE="$IMAGE" \
      --env SIZE="$SIZE" \
      dcycle/api_client_helper:1 digitalocean accountinfo

How to use without Docker
-----

Start by running the same pip3 install commands as in the Dockerfile.

Then:

    export NAME=my-first-vm
    export TOKEN=my-api-token
    export SSH_FINGERPRINT=my-ssh-fingerprint
    python3 ./vm.py --provider digitalocean --action create


Deveolopment
-----

Share the volument using `-v $(pwd):/usr/src/app`:

TOKEN=my-api-token
docker run -v $(pwd):/usr/src/app --rm \
  --env TOKEN="$TOKEN" \
  dcycle/api_client_helper:1 digitalocean accountinfo
