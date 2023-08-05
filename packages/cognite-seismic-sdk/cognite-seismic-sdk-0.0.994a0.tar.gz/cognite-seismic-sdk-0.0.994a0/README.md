<a href="https://cognite.com/">
    <img src="https://cognite.com/css/Images/CogniteLogo.svg" alt="Cognite logo" title="Cognite" align="right" height="80" />
</a>


# Cognite Seismic Python SDK
An early Python SDK for the Seismic data store API.

## Prerequisites
In order to start using the Python SDK, you need
- Python3 (>= 3.6) and `pip`
- An API key. Never include the API key directly in the code or upload the key to github. Instead, set the API key as an environment variable. See the usage example for how to authenticate with the API key.

This is how you set the API key as an environment variable on Mac OS and Linux:
```bash
$ export COGNITE_API_KEY=<your API key>
```

On Windows, you can follows [these instructions](https://www.computerhope.com/issues/ch000549.htm) to set the API key as an environment variable.

## Installation
To install this package:

```bash
$ pip install grpcio numpy protobuf
$ pip install cognite-seismic-sdk
```

## Dev installation

* Run `pipenv install --dev` to install a virtual environment and dependencies.
* Install the package using `pip install -e .`. This way, changes to the source code will affect the package.

## Examples
See the file [`examples.py`](./examples.py).