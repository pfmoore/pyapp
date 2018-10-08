# Use cases that pyapp should support

## Self-hosting

The distribution should contain a config file that builds
pyapp. Specific requirements:

1. Standalone exe that only needs Python installed to run.
2. Standalone exe that doesn't even need Python. (Is there any
   point to having this? Why would you use pyapp if you don't
   have Python?)
3. Config file can be used to rebuild a new pyapp, from github,
   from PyPI, ...? Requires a command line means to override the
   default source location from the config.

## Styles of application

Getting the code will always be via a pip-style list of requirements.
Introspecting code and working out what needs to be included is an
explicit non-goal.

What main routine(s) to expose - various options:

1. Console entry point(s) as applications to expose. Note that a single
   distribution may expose multiple console entry points.
2. Call to a defined API - "myapp.cmd:main".
3. Custom script.

Questions:

* Explicit specification of console entry points to expose? Implicit
  "expose all of them" mode if not explicit spec given? (There are
  often extra utility entry points that you may not want to expose).
* Entry point, but with a different name? (e.g., "pip3.7" -> "pip").

## Applications I'm interested in

Various applications here, that I've used or been interested in, that
I'd like to be able to bundle with pyapp.

* Invoke - can run as zipapp, so single-file zipapp would be good.
* Tox, nox - use virtualenv, so weirdnesses about calling virtualenv
  from venv might be a factor.
* Pipenv - uses virtualenv, might introspect the executing Python
  interpreter as a default (so running via embedded distro may be bad).
* Pew - virtualenv again.

## Installation

* `pip install pyapp` creates a `pyapp` executable. Not the "official"
  installation method, but should work.
* Standalone single-file `pyapp.exe` that works if Python is installed.
* Portable `pyapp.zip` that includes a Python runtime and can be unpacked
  anywhere.

**Note**: Virtualenv build method has potential issues if used with a
version of pyapp that bundles its own runtime, as the virtual environments
that get created will be based on the (embedded) runtime of pyapp.

## Invocation

Define apps in a config file, and build with `pyapp build [app]...`.

Standalone apps (zipapp model) have no further options. Upgrades, etc.,
are handled by rebuilding.

Virtualenv-based apps have further options - upgrade, etc. Maybe also
have a management command to "run a command in the app venv"?

## Limitations of other tools

* We need to be able to build an app from any pip-style requirement (e.g.,
  standalone wheel file, git URL, ...)
* We need to support pip install options (`--find-links`, `--no-index`,
  ...).
