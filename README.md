API Client Helper
=====

*This project is experimental; and not actively maintained. It may work, but no support will be provided.*

[![CircleCI](https://circleci.com/gh/dcycle/api_client_helper/tree/master.svg?style=svg)](https://circleci.com/gh/dcycle/api_client_helper/tree/master)

Interact with various APIs in Python.

This project currently has plugins for

* [DigitalOcean](https://developers.digitalocean.com/documentation/v2/) to manage Virtual Machines;
* [Acquia](https://docs.acquia.com/cloud-platform/develop/api/) to manage Drupal cloud hosting.

Each plugin is in its ./plugins/* folder, for example ./plugins/acquia or ./plugins/digitalocean, and you can copy-paste those as starters for your own plugins.

Documentation specific to each plugin can be found in each plugin's README.md document, for example `./plugins/digitalocean/README.md`.

This project is meant to ube used as a starterkit for your own API needs.

How to use with Docker
-----

This project defines "providers" such as DigitalOcean, which are in the `./plugins` directory; and, for each provider, actions, as `./plugins/digitalocean/accountinfo/accountinfo.yml`. Please look at the YAML files within the `./plugins` directory and its subdirectories, as a basis for creating extra providers and actions.

Feel free to submit pull requests if you feel your work might be of interest to other teams.

One fo the providers in this project is `dummy`, and one of its actions is `dummy`. This provider and action is used simply to demonstrate how API Client Helper works.

To run the dummy action on the dummy provider, you can run:

    docker run --rm dcycle/api_client_helper:1 dummy dummy

    {"hello": "world", "embedded": {"hello": "unicorns"}}

To view pretty Json, you can run something like this:

    docker run --rm dcycle/api_client_helper:1 dummy dummy | python -m json.tool

    {
        "embedded": {
            "hello": "unicorns"
        },
        "hello": "world"
    }

You can use Jsonpath syntax to get only part of the response, like this:

    docker run --rm dcycle/api_client_helper:1 dummy dummy \
      --jsonpath=$.embedded

    {"hello": "unicorns"}

    docker run --rm dcycle/api_client_helper:1 dummy dummy \
      --jsonpath=$.embedded.hello

    ["unicorns"]

To get the first item in an array:

    docker run --rm dcycle/api_client_helper:1 dummy dummy \
      --jsonpath=$.embedded.hello \
      --jsondecodefirst=1

    unicorns

A real-world example
-----

This script defines interaction with the DigitalOcean API at `./plugins/digitalocean`, meaning that, assuming you have a valid DigitalOcean API token, you can run something like:

    TOKEN=my-api-token
    docker run --rm \
      --env TOKEN="$TOKEN" \
      dcycle/api_client_helper:1 digitalocean accountinfo

    {"account": {"droplet_limit": 25, "floating_ip_limit": 3, "volume_limit": 100, "email": "admin@example.com", "uuid": "abc123", "email_verified": true, "status": "active", "status_message": ""}}

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
      dcycle/api_client_helper:1 digitalocean newdroplet

    {"droplet": {"id": 236335349, "name": "some-new-droplet", "memory": 8192, "vcpus": 4.....

This will create a new droplet with ID 236335349 (in this example), but it will not yet be available for use. That might take up to a minute; we need to poll the dropletinfo API endpoint until it's ready ("active", not "new").

**Here is how to do it manually; read on for an automated way to have the script do it for you.**

Assuming your TOKEN environment variable is still set, you can get information about your droplet by running:

    ID=236335349
    docker run --rm \
      --env TOKEN="$TOKEN" \
      --env ID="$ID" \
      dcycle/api_client_helper:1 digitalocean dropletinfo

This will give you a lot of information; but what we are looking for is the active status, which can be isolated using Jsonpath:

    docker run --rm \
      --env TOKEN="$TOKEN" \
      --env ID="$ID" \
      dcycle/api_client_helper:1 digitalocean dropletinfo \
      --jsonpath=$.droplet.status \
      --jsondecodefirst=1

    active

We will call this a multi-step request:

* First, create a Droplet
* Next, wait for the droplet to be active

To further automate this, see the "Multi-step Requests" section, below.

How to use without Docker
-----

Start by running the same pip3 install commands as in the `Dockerfile`.

Then:

    sudo pip3 install requests pyyaml deepmerge jsonpath-ng
    export TOKEN=my-api-token
    python3 ./api_client_helper.py dummy dummy

Multi-step Requests
-----

Coming back to our "create a Droplet" example, above, several APIs have this behaviour:

* Make a request
* Keep polling the API every second until the request is fulfilled
* Fail after a minute or so

You can define your own multi-step requests. This script provides a dummy example:

    docker run --rm dcycle/api_client_helper:1 dummy multistep

    {"hello": "world", "embedded": {"hello": "unicorns"}}

This example actually calls the dummy action four times and is defined in `./plugins/multistep/mutistep/multistep.yml`.

You can see what's going on by using the debug flag as described in the "Debugging" section, below:

    docker run --rm \
      --env DEBUG=1 \
      dcycle/api_client_helper:1 dummy multistep

    [DEBUG] message
    [DEBUG] ===> STEP 0
    [DEBUG] message
    [DEBUG] Try 0 of 90
    [DEBUG] multistep
    [DEBUG] Success, moving to next step
    [DEBUG] message
    [DEBUG] ===> STEP 1
    [DEBUG] message
    [DEBUG] Try 0 of 90
    [DEBUG] multistep
    [DEBUG] Success, moving to next step
    [DEBUG] message
    [DEBUG] ===> STEP 2
    [DEBUG] message
    [DEBUG] Try 0 of 90
    [DEBUG] multistep
    [DEBUG] Success, moving to next step
    [DEBUG] message
    [DEBUG] ===> STEP 3
    [DEBUG] message
    [DEBUG] Try 0 of 90
    [DEBUG] multistep
    [DEBUG] Success, moving to next step
    [DEBUG] multistep
    [DEBUG] Multistep action succeeded
    {"hello": "world", "embedded": {"hello": "unicorns"}}

We ship with a multistep "create a DigitalOcean Droplet" action, which you can run by:

    TOKEN=my-api-token
    LOCATION=nyc3
    SIZE=8gb
    NAME=some-new-droplet
    IMAGE=docker-18-04
    SSH_FINGERPRINT=a1:b2:c3:d4:a1:b2:c3:d4:a1:b2:c3:d4:a1:b2:c3:d4
    time docker run --rm \
      --env DEBUG="1" \
      --env TOKEN="$TOKEN" \
      --env LOCATION="$LOCATION" \
      --env SIZE="$SIZE" \
      --env NAME="$NAME" \
      --env IMAGE="$IMAGE" \
      --env SSH_FINGERPRINT="$SSH_FINGERPRINT" \
      dcycle/api_client_helper:1 digitalocean newdroplet_and_wait \
      --jsonpath='$.droplet.networks.v4[?(@.type = "public")].ip_address'

    [DEBUG] A bunch of debug messages...
    ["1.2.3.4"]

    real	0m35.167s
    user	0m0.130s
    sys	0m0.062s

Run it witout `--env DEBUG="1"` and with `--jsondecodefirst=1` to get just the IP address.

More DigitalOcean requests can be found in `./plugins/digitalocean/README.md`.

Another multistep example
-----

Let's say you have an API request which returns:

    [
      {
        "id": "123",
        "name": "hello"
      },
      {
        "id": "234",
        "name": "world"
      },
      {
        "id": "456",
        "name": "hello"
      },
    ]

And another request where you can _delete_ any item by ID.

And you would like to delete all items with "hello".

You can find mock actions to list, and to delete (we'll see later on how to combine them in a multistep action):

    docker run --rm dcycle/api_client_helper:1 dummy mock_list

    [[{"id": 123, "name": "hello"}, {"id": 234, "name": "world"}, {"id": 456, "name": "hello"}]]

    docker run --rm \
      --env ID="456" \
      dcycle/api_client_helper:1 dummy mock_delete

    [{"response": "Mock deleted mock ID 456"}]

Take a look now at our mock multistep action to mock-delete _the first_ item with the name "hello", which is defined in `./plugins/dummy/mock_delete_all_by_name`.

    NAME=hello
    docker run --rm \
      --env NAME="$NAME" \
      dcycle/api_client_helper:1 dummy mock_delete_all_by_name

    [{"response": "Mock deleted mock ID 123"}]

The system does not currently allow deleting all items with the name "hello" (for example) with a single multistep action.

Errors
-----

In case of an error you'll get information about the error and a non-zero exit code.

Developers
-----

### Testing Individual Files

This project contains a number of files starting with `test_`, for example `test_my_jsonpath.py`.

To test these files you can run (for example):

    docker run --rm --entrypoint python3 dcycle/api_client_helper:1 test_my_jsonpath.py

Working with Json and Jsonpath
-----

By default the command will output the json result as a string. Let's use the "dummy" provider's "dummy" action to confirm this:

    docker run --rm dcycle/api_client_helper:1 dummy dummy
    {"hello": "world", "embedded": {"hello": "unicorns"}}

You can then format this using whatever method you like, for example:

    docker run --rm dcycle/api_client_helper:1 dummy dummy | python -m json.tool
    {
        "embedded": {
            "hello": "unicorns"
        },
        "hello": "world"
    }

You can also [the JsonPath syntax](https://jsonpath.com) to further dig through your document. The dollar sign is equal to your entire document, so the following are equivalent:

    docker run --rm dcycle/api_client_helper:1 dummy dummy
    {"hello": "world", "embedded": {"hello": "unicorns"}}
    docker run --rm dcycle/api_client_helper:1 dummy dummy --jsonpath=$
    {"hello": "world", "embedded": {"hello": "unicorns"}}

However, if you just want to print the word "unicorns", you can use the jsonpath `$.embedded.hello`:

    docker run --rm dcycle/api_client_helper:1 dummy dummy --jsonpath=$.embedded.hello
    "unicorns"

You can use `--jsondecodefirst=1` to decode the json (in this case remove the quotes from the word "unicorn"):

    docker run --rm dcycle/api_client_helper:1 dummy dummy --jsonpath=$.embedded.hello --jsondecodefirst=1
    unicorns

(If you use `--jsondecodefirst=1` with an object, you will end up with a non-json string which is not of much use.)

More Json and Jsonpath examples
-----

Consider the following output:

    docker run --rm dcycle/api_client_helper:1 dummy jsonpath_example | python -m json.tool
    {
        "hello": [
            {
                "response": "hello",
                "valid": 0
            },
            {
                "response": "world",
                "valid": 1
            },
            {
                "response": "another invalid response",
                "valid": 0
            }
        ]
    }

Let's say I want to get the string "world", I need to _filter_ the response of "hello" by "valid = 1". Here is how to do it to output only the string "world":

    docker run --rm dcycle/api_client_helper:1 \
      dummy jsonpath_example \
      --jsonpath='$.hello[?(@.valid=1)].response' \
      --jsondecodefirst=1

This will output "world".

    docker run --rm dcycle/api_client_helper:1 \
      dummy jsonpath_example \
      --jsonpath='$.hello[?(@.valid=0)].response' \
      --jsondecodefirst=1

Debugging
-----

If you set the DEBUG environment variable to 1, you will see debug info:

    docker run --rm \
      --env DEBUG=1 \
      dcycle/api_client_helper:1 dummy multistep

Local deveolopment
-----

Share the volument using `-v $(pwd):/usr/src/app`:

TOKEN=my-api-token
docker run -v "$(pwd)":/usr/src/app --rm \
  --env TOKEN="$TOKEN" \
  dcycle/api_client_helper:1 digitalocean accountinfo
