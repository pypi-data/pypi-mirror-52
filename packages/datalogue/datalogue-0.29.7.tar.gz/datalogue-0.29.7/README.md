dtl-python-sdk
--------------

The Datalogue python SDK is an SDK to be able to interact with the platform from
code.

Full documentation is available [here](https://dtl-python-sdk.netlify.com)

## Use in a python project

*Requirements*
*You need to have artifactory [set up](https://github.com/datalogue/grimoire/blob/master/docs/getting-started.md) with pip to be able to use this library*

### Install with Pip
```bash
pip install datalogue
```

### Use in requirements.txt file

```txt
datalogue==0.0.1
```

## Environment Variables for Integration Tests
* `DTL_TEST_USERNAME`: Basically, an email address that is already signed up and has admin rights in its organization
* `DTL_TEST_PASSWORD`: Password for that corresponding user
* `DTL_TEST_URI`: Infrastructure to use for integration tests. It can be either locally deployed platform or remote platform such as internals

## Releases

Release process should be automated, once you merge something into master the process is going to be triggered, this includes:

* Trigger circle-ci jobs.
* Generate a distribution version in artifactory.
* Generate docs to netlify.

# Release candidates
If you need to release a non production ready version you can run:

```bash
make set-version version="1.0.0"
make release
```

## Release process messages
There are 3 types of releases. The release process will check your commits and based on the message it will auto decide which type is appropiated.

    * Majors. Any of the commits since the last release is marked with the title `BREAKING CHANGE`.
    * Minors. Any of the commits since the last release is marked with the title `feat:`.
    * Patches. Any of the commits since the last release is marked with the title `fix:`.

## SSL Verification
We dont have a way to ensure that our clients submit the right certificates, a workaround is to set the enviroment variable `DTL_SSL_VERIFY_CERT` to `false` in order to be able to create a valid session, be aware that this wont stop the warning messages.

## Sentry

`SENTRY_DSN` env variable should be set in the env where we deploy the SDK