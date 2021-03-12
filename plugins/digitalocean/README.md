DigitalOcean API
=====

Droplet creation is described in the main ./README.md file.

To get info about all DigitalOcean droplets:

    TOKEN=my-api-token
    docker run --rm \
      --env TOKEN="$TOKEN" \
      dcycle/api_client_helper:1 digitalocean listdroplets

To see only the active Droplet ids, names, and public IP addresss:

    TOKEN=my-api-token
    docker run --rm \
      --env TOKEN="$TOKEN" \
      dcycle/api_client_helper:1 digitalocean listdroplets \
      --jsonpath="$.droplets[?(@.status=active)].id,name,networks" \
      | python -m json.tool

To get info about a DigitalOcean droplet with its ID:

    ID=1234567
    TOKEN=my-api-token
    docker run --rm \
      --env TOKEN="$TOKEN" \
      --env ID="$ID" \
      dcycle/api_client_helper:1 digitalocean dropletinfo \
      | python -m json.tool

To delete a DigitalOcean droplet with its ID:

    ID=1234567
    TOKEN=my-api-token
    docker run --rm \
      --env TOKEN="$TOKEN" \
      --env ID="$ID" \
      dcycle/api_client_helper:1 digitalocean deletedroplet
