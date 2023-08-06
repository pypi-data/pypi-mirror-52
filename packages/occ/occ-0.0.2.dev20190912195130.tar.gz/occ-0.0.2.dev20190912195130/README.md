# Octavia Chicken Checker

Octavia Chicken Checker looks for abandoned Octavia load balancer artifacts, amphoras, and so forth. Optionally it will clean them up as well.

## Installation

```shell
$ pip install -r requirements.txt

$ pip install setup.py
```

## Running

```shell
$ occ list
```

## Development

This project includes a number of helpers in the `Makefile` to streamline common development tasks.

### Environment Setup

The following demonstrates setting up and working with a development environment:

```shell
### create a virtualenv for development

$ make virtualenv

$ source env/bin/activate


### run occ cli application

$ occ --help


### run pytest / coverage

$ make test
```

### Releasing to PyPi

Before releasing to PyPi, you must configure your login credentials:

**~/.pypirc**:

```ini
[pypi]
username = YOUR_USERNAME
password = YOUR_PASSWORD
```

Then use the included helper function via the `Makefile`:

```shell
$ make dist

$ make dist-upload
```

## Deployments

### Docker

Included is a basic `Dockerfile` for building and distributing `Octavia Chicken Checker`,
and can be built with the included `make` helper:

```
$ make docker

$ docker run -it occ --help
```
