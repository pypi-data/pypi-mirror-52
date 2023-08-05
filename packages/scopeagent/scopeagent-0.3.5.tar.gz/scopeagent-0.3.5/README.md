# scope-python-agent

Python agent for [Scope](https://scope.dev)


## Install

    pip install scopeagent


## Usage

Please refer to the documentation at [https://docs.scope.dev/docs/python-installation](https://docs.scope.dev/docs/python-installation)


## Development

### Automated Testing

The following environment variables are used for database tests:

* `POSTGRES_DBURL`

To run the tests:

    tox

### Publishing

To publish a new version of `scopeagent` to [pypi](https://pypi.org/):

    make publish

You will need valid [pypi](https://pypi.org/) credentials with access to the `scopeagent` package.
