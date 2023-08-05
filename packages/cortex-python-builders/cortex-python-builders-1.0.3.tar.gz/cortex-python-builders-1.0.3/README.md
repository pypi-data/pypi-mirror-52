# Programmatic Building of Cortex Resources

The Cortex Python Builders module provides tools to programmatically build Cortex resources (e.g. Skill, Actions, Datasets, etc.) using Python.
Refer to the Cortex documentation for details on how to use the library: 

- Developer guide: https://docs.cortex.insights.ai/docs/developer-guide/overview/
- Cortex Python references: https://docs.cortex.insights.ai/docs/developer-guide/reference-guides


## Installation

To install: 
```
  > pip install cortex-python-builders
```

or from source code:
```
  > git clone git@github.com:CognitiveScale/cortex-python-builders.git
  > cd cortex-python-builders
  > pip install -e .
```

## Development 

### Setup

When developing, it's a best practice to work in a virtual environment. Create and activate a virtual environment:
```
  > virtualenv --python=python3.6 _venv
  > source _venv/bin/activate
```

Install developer dependencies:

```
  > git clone git@github.com:CognitiveScale/cortex-python-builders.git
  > cd cortex-python-builders
  > make dev.install
```

There's a convenience `Makefile` that has commands to common tasks, such as build, test, etc. Use it!

### Testing

#### Unit Tests

Follow above setup instructions (making sure to be in the virtual environment and having the necessary dependencies)

- `make test` to run test suite

To run an individual file or class method, use pytest. Example tests shown below:

- file: `pytest test/unit/ames_test.py` 
- class method: `pytest test/unit/ames_test.py::TestLocal::test_analysis`

#### Publishing an alpha build

Suppose you want to release new functionality so it can be installed without releasing a new official version. We need to use an alpha version in PyPi.

- we need to create and publish an alpha release:
- get credentials to the `cortex-python-builders` pypi CognitiveScale account (via lastpass)
- run `make dev.push`. The alpha pre-release number (the N in X.Y.ZaN) with be determined automatically.

### Contribution 

After contributing to the library, and before you submit changes as a PR, please do the following

1. Run unit tests via `make test`
2. Manual verification (i.e. try the new changes out in Cortex) to make sure everything is going well. Not required, but highly encouraged.
3. Bump up `setup.py` version and update the `CHANGELOG.md` 

### Documentation

The package documentation is built with Sphinx. To build the documentation:

```
> make docs
```
The documentation will be rendered in HTML format under the `docs/_build/html` directory.

Activate your virtual environment:
```
> source _venv/bin/activate
```

Setup your environment, if you have not done so:
```
> make dev.install 
```

### Pre-release to staging

1. Create and push an alpha release:
    ```
    > make dev.push TAG=1
    ```
    This will build an alpha-tagged package.
2. Merge `develop` to `staging` branch:
    ```
    > make stage
    ```
3. In GitHub, create a pull request from `staging` to `master`.
