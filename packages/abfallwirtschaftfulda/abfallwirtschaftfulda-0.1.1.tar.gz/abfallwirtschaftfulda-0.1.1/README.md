# Python: Abfallwirtschaft Fulda

[![GitLab Release][releases-shield]][releases]
![Project Stage][project-stage-shield]
[![License][license-shield]](LICENSE.md)

[![Build Status][build-shield]][build]
![Project Maintenance][maintenance-shield]
[![GitLab Activity][commits-shield]][commits]

[![Buy me a coffee][buymeacoffee-shield]][buymeacoffee]

[![Support my work on Patreon][patreon-shield]][patreon]

Asynchronous Python client for the Abfallwirtschaft Fulda API.

## About

This package allows you to request waste pickup days from Abfallwirtschaft Fulda
programmatically. It is mainly created to allow third-party programs to use
or respond to this data.

An excellent example of this might be Home Assistant, which allows you to write
automations, e.g., play a Google Home announcement in the morning when it is
trash pickup day.

## Installation

```bash
pip install abfallwirtschaftfulda
```

## Usage

```python
import asyncio

from abfallwirtschaftfulda import AbfallwirtschaftFulda, WASTE_TYPE_NON_RECYCLABLE


async def main(loop):
    """Show example on stats from Abfallwirtschaft Fulda."""
    async with AbfallwirtschaftFulda(district_id=7, town_id=40, loop=loop) as tw:
        await tw.update()
        pickup = await tw.next_pickup(WASTE_TYPE_NON_RECYCLABLE)
        print("Next pickup for Non-recyclable:", pickup)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
```

## Changelog & Releases

This repository keeps a change log using [GitLab's releases][releases]
functionality. The format of the log is based on
[Keep a Changelog][keepchangelog].

Releases are based on [Semantic Versioning][semver], and use the format
of ``MAJOR.MINOR.PATCH``. In a nutshell, the version will be incremented
based on the following:

- ``MAJOR``: Incompatible or major changes.
- ``MINOR``: Backwards-compatible new features and enhancements.
- ``PATCH``: Backwards-compatible bugfixes and package updates.

## Contributing

This is an active open-source project. We are always open to people who want to
use the code or contribute to it.

We've set up a separate document for our
[contribution guidelines](CONTRIBUTING.md).

Thank you for being involved! :heart_eyes:

## Setting up development environment

In case you'd like to contribute, a `Makefile` has been included to ensure a
quick start.

```bash
make venv
source ./venv/bin/activate
make dev
```

Now you can start developing, run `make` without arguments to get an overview
of all make goals that are available (including description):

```bash
$ make
Asynchronous Python client for Abfallwirtschaft Fulda.

Usage:
  make help                            Shows this message.
  make dev                             Set up a development environment.
  make lint                            Run all linters.
  make lint-black                      Run linting using black & blacken-docs.
  make lint-flake8                     Run linting using flake8 (pycodestyle/pydocstyle).
  make lint-pylint                     Run linting using PyLint.
  make lint-mypy                       Run linting using MyPy.
  make test                            Run tests quickly with the default Python.
  make coverage                        Check code coverage quickly with the default Python.
  make install                         Install the package to the active Python's site-packages.
  make clean                           Removes build, test, coverage and Python artifacts.
  make clean-all                       Removes all venv, build, test, coverage and Python artifacts.
  make clean-build                     Removes build artifacts.
  make clean-pyc                       Removes Python file artifacts.
  make clean-test                      Removes test and coverage artifacts.
  make clean-venv                      Removes Python virtual environment artifacts.
  make dist                            Builds source and wheel package.
  make release                         Release build on PyP
  make tox                             Run tests on every Python version with tox.
  make venv                            Create Python venv environment.
```

## License

MIT License

Copyright (c) 2019 Stephan Beier

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[build-shield]: https://dev.azure.com/stbkde/python-abfallwirtschaftfulda/_apis/build/status/stbkde.python-abfallwirtschaftfulda?branchName=master
[build]: https://dev.azure.com/stbkde/python-abfallwirtschaftfulda/_build/latest?definitionId=2&branchName=master
[buymeacoffee-shield]: https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-2.svg
[buymeacoffee]: https://www.buymeacoffee.com/stbkde
[commits-shield]: https://img.shields.io/gitlab/commit-activity/y/stbkde/python-abfallwirtschaftfulda.svg
[commits]: https://gitlab.com/stbkde/python-abfallwirtschaftfulda/commits/master
[contributors]: https://gitlab.com/stbkde/python-abfallwirtschaftfulda/graphs/contributors
[stbkde]: https://gitlab.com/stbkde
[keepchangelog]: http://keepachangelog.com/en/1.0.0/
[license-shield]: https://img.shields.io/gitlab/license/stbkde/python-abfallwirtschaftfulda.svg
[maintenance-shield]: https://img.shields.io/maintenance/yes/2019.svg
[patreon]: https://www.patreon.com/stbkde
[project-stage-shield]: https://img.shields.io/badge/project%20stage-experimental-yellow.svg
[releases-shield]: https://img.shields.io/gitlab/release/stbkde/python-abfallwirtschaftfulda.svg
[releases]: https://gitlab.com/stbkde/python-abfallwirtschaftfulda/releases
[semver]: http://semver.org/spec/v2.0.0.html
