# Pyapp - Deploy Python applications

**Note** The name needs to change. The "pyapp" name is already taken on
PyPI. For now this will do as a placeholder, but I need to find something
else.

Everyone writes a tool to install Python applications locally. There
are the established tools for making a standalone executable, like
[py2exe](https://pypi.org/project/py2exe/),
[cx_Freeze](https://pypi.org/project/cx_Freeze/), and
[pyInstaller](https://pypi.org/project/pyinstaller/). There are also
tools to manage virtual environments which contain applications,
like
[pipsi](https://pypi.org/project/pipsi/), and
[venvs](https://github.com/Julian/venvs). And furthermore, there is
the standard library
[zipapp](https://docs.python.org/3.7/library/zipapp.html)
module, for creating zipped applications.

Pyapp is yet another tool for doing stuff like this. There's not much
new going on, so if you're happy with one of the other solutions, pyapp
probably isn't for you. It grew out of my frustration with never *quite*
finding a tool that did what I wanted - so in the end, I decided to write
the tool I was looking for.

## Basic summary

Pyapp creates "standalone" Python applications. I put "standalone" in
quotes, because in its normal mode of operation, it doesn't bundle the
Python runtime, so the user needs a version of Python installed. (It
can optionally bundle an embedded Python distribution, though, so fully
standalone applications are possible, just not the default).

The basic modes of operation that I plan on including are

* pipsi-like virtual environment management, with launcher executables
  in a separate directory.
* Zip applications, with or without a prepended exe launcher.
* Shared library in a zipfile, with multiple launchers referencing it.

Configuration will be handled by an explicit definition file. The
intention is that rebuilding a complete application set can be handled
by running a single command.

I intend to self-host pyapp, in the sense that there will be a build
configuration in the sources that creates a standalone pyapp (which
can be downloaded and used to manage your own apps).

## Supported Environments

Pyapp is developed on Windows, and uses Python 3.7 (or later) by default.
At some point, I may consider making it general enough to work on other
platforms, and indeed some modes of operation may work "by accident" on
non-Windows systems (Python generally makes it easier to write portable
code than not to). But until Windows support (the use case I care about
for my own requirements) is solid, I'm not going to worry about other
platforms.

I may support older versions of Python 3. It won't be a priority, though,
as there are some annoying quirks of the embedded distribution and the
C API in previous versions that I don't want to have to worry about
working around. Plus, I work slowly enough that by the time anyone else
cares about using this, Python 3.7 will probably qualify as "old" :-)

I won't ever support Python 2. I haven't used Python 2 for years now, and
I'm not interested in limiting the features I use just to support an
obsolete version of Python. Sorry.
