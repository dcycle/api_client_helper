Acquia API
=====

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

docker run --rm     --env KEY="$KEY"     --env SECRET="$SECRET"     --env ENVID="$ENVID" -v $(pwd):/usr/src/app dcycle/api_client_helper:1 acquia envbranch --jsonpath=$.vcs.path

A complex series of calls to achieve results
-----

In certain APIs such as Acquia's Cloud API 2, achieving a given result can require making a series of calls and waiting until something happens remotely in order for a given task to be complete.

For example, Acquia allows one to switch its code from one branch to another on a given environment. Here is how this is achieved:

* Determine what tag or branch you want to change your code to
* See if the branch or tag exists and throw an error if it does not call (1 call)
* Change the branch or tag (1 call)
* Obtain a "notification" URL
* Call the notification URL until the action is "complete" or x seconds has gone by.

We call this a "complex" action because it entails more than one call to the API. In order to demonstrate how this might work, we have created a similar dummy "complex" action which you can call like this. You can simulate a success using `SIMULATE=success`; a failure at step 1 by `SIMULATE=fail1`; and a failure at step 2 by `SIMULATE=fail2`.
