Changelog
=========


1.1.0 (2025-06-26)
------------------

Changes
~~~~~~~
- Update workflows, add container workflow to test rpms. [Stephen L
  Arnold]

  * add a tox dev environment, remove .spec from gitignore
- Still more cleanup in docs config and index. [Stephen L Arnold]
- Migrate package metadata to pyproject.toml, update project files.
  [Stephen L Arnold]

  * update readme, pre-commit, and tox files
  * remove MANIFEST.in and setup.cfg

Fixes
~~~~~
- Cleanup test imports and lint, update tox config. [Stephen L Arnold]


1.0.0 (2025-03-24)
------------------

New
~~~
- Generate a changelog and add to doc index. [Stephen L Arnold]
- Add tox cmd to generate changelog. [Stephen L Arnold]

Changes
~~~~~~~
- Add reuse badge and update changelog. [Stephen L Arnold]
- Add REUSE config and make LICENSE a symlink to the text. [Stephen L
  Arnold]
- Update tox cmds and python versions, adjust project config. [Stephen L
  Arnold]

  * update readme and add .gitchangelog.rc file

Fixes
~~~~~
- Disable link check in sphinx docs build workflow. [Stephen L Arnold]

  * old changelog bits have too many crufty URLs


0.4.1 (2024-12-24)
------------------

Changes
~~~~~~~
- Early spring cleanup, update workflows and use setuptools_scm.
  [Stephen L Arnold]

Fixes
~~~~~
- Cleanup daemon args logging vs console output. [Stephen L Arnold]


0.4.0 (2023-09-20)
------------------

Changes
~~~~~~~
- Update docs, more packaging and coverage cleanup. [Stephen L Arnold]
- Upgrade all action versions to current. [Stephen L Arnold]
- Use upstream examples link instead of GH (not)permalink. [Stephen L
  Arnold]
- Cleanup/bump versions in pre-commit config. [Stephen L Arnold]

Other
~~~~~
- General cleanup, add py311 and update coverage workflow. [Stephen L
  Arnold]


0.3.5 (2022-07-10)
------------------

Fixes
~~~~~
- MANIFEST.in needs graft test to include all test files in sdist.
  [Stephen L Arnold]


0.3.4 (2022-07-09)
------------------

Changes
~~~~~~~
- Add pointer to example daemon script, fix missing ref. [Stephen L
  Arnold]
- Add platform badge to readme. [Stephen L Arnold]
- Adjust test delay for macos, cleanup optional deps, packaging cfg.
  [Stephen L Arnold]

Fixes
~~~~~
- Doc sources in sdist require the README.rst file. [Stephen L Arnold]


0.3.3 (2022-07-08)
------------------

Fixes
~~~~~
- Make sdist more complete, including test and doc srcs. [Stephen L
  Arnold]

  * keep exclude in setup.cfg, requires MANIFEST.in to graft srcs


0.3.2 (2022-07-04)
------------------

Changes
~~~~~~~
- General readme cleanup, update args and example. [Stephen L Arnold]
- Add alternate-branches test, exclude NotImplemented funcs. [Stephen L
  Arnold]

  * must be subclassed by the consuming script

Fixes
~~~~~
- Restore missing closing paren. [Stephen L Arnold]
- Remove duplicate log msg and getLogger call. [Stephen L Arnold]

  * add record_factory so we can set custom name in log record


0.3.1 (2022-06-30)
------------------

Changes
~~~~~~~
- Move test script to test directory, update tox file. [Stephen L
  Arnold]

Fixes
~~~~~
- Make sure artifact upload finds the right wheels. [Stephen L Arnold]


0.3.0 (2022-06-29)
------------------

New
~~~
- Add docs build, convert readme to rst, cleanup some docstrings.
  [Stephen L Arnold]
- Add base python package workflows, update tox file. [Stephen L Arnold]

  * pylint seems to need a little extra foo
  * no windows workflows for simple python daemons
- Modern packaging, new tools, more deps and lint cleanup. [Stephen L
  Arnold]

  * fix gevent.signal not a callable, apply isort cleanup
  * add git versioning, cleanup string warnings

Changes
~~~~~~~
- Add coverage workflow and pkg name helper script. [Stephen L Arnold]

  * add still-more-status to readme
- Add tool configs, apply pre-commit cleanup. [Stephen L Arnold]
- Remove old py2 timezone helper, reformat logger src. [Stephen L
  Arnold]

Fixes
~~~~~
- Enable syntax highlighting in the readme on github. [Stephen L Arnold]
- Use static badge since github does not grok the license. [Stephen L
  Arnold]
- Still more readme cleanup. [Stephen L Arnold]
- Add egg_info pre-command for import checks to tox file. [Stephen L
  Arnold]
- Fix tests and cleanup some archaic lint. [Stephen L Arnold]

Other
~~~~~
- Doc: really fix license badge... [Stephen L Arnold]
- Add pylint section to tox.ini and cleanup some lint, fix osx. [Stephen
  L Arnold]
- Add coverage_python_version plugin to sort out test coverage. [Stephen
  L Arnold]


0.2.3 (2020-03-13)
------------------
- Add py27 timezone file back and update tests (see test_daemon.py
  comment) [Stephen Arnold]
- Setup.py: version bump and update classifiers. [Stephen Arnold]
- Keep py27 in CI for a while longer. [Stephen Arnold]
- Daemon/__init__.py: add status arg, returns self.is_running() [Stephen
  Arnold]
- .travis.yml: fix silly travis cfg... [Stephen Arnold]
- Test_daemon.py: fix tests for all test runners, restore tox cfg.
  [Stephen Arnold]
- Cleanup .travis.yml, remove tox.ini, correct test assert. [Stephen
  Arnold]


0.2.2 (2020-03-01)
------------------
- Dev-python/daemon: add pre-stop cleanup handler and remove py27
  support. [Stephen Arnold]
- Tox.ini: bump allowed line length by one character. [Stephen Arnold]
- Update logging format and switch README urls to freepn. [Stephen
  Arnold]


0.2.1 (2019-12-17)
------------------
- Setup.py: version bump. [Stephen Arnold]
- Revert move of test script, keep test settings file. [Stephen Arnold]


0.2.0 (2019-12-17)
------------------
- Setup.py: bump version for github release (pick up new helper modules)
  [Stephen Arnold]
- Settings.py: move test artifacts, only use settings for local testing.
  [Stephen Arnold]
- Add initial settings.py file for config options. [Stephen Arnold]
- Daemon/__init__.py: fix silly migration typo. [Stephen Arnold]
- Add timestamps and initial logging output for verbose=0, update
  .gitignore. [Stephen Arnold]
- .travis.yml: add os/x back to the testing matrix. [Stephen Arnold]
- .travis.yml: remove coveralls and add irc notify. [Stephen Arnold]
- Update py versions in setup.py and travis cfg, add tox.ini for
  test/cov. [Stephen Arnold]
- Revert "README.markdown: point travis in the right direction..."
  [Stephen Arnold]

  This reverts commit b00dd3c768bf596862c5d4974b21197f0d585983.
- README.markdown: point travis in the right direction... [Stephen
  Arnold]
- Setup.py: add packages name for correct import. [Stephen Arnold]
- Mv daemon.py to daemon/__init__.py for packaging. [Stephen Arnold]
- Attempt to fix python 2.6 build. [Carlos Perelló Marín]
- Use flake8 to check python files. [Carlos Perelló Marín]
- Added travis build state. [Carlos Perelló Marín]
- Updated the notification secret. [Carlos Perelló Marín]
- Ignored bitcode files. [Carlos Perelló Marín]
- Added license text. [Carlos Perelló Marín]
- Updated setup.py with some ideas from https://github.com/amdei/python-
  daemon/tree/py_daemon. [Carlos Perelló Marín]
- Initial travis config. [Carlos Perelló Marín]
- Add py3k support, drop 2.5- support, add tests. [jingchao]
- Add python 3 compatibility while preserving python 2.4+ compatibility.
  [Jonathan Barratt]
- Eventlet compatible. [Tony Wang]
- More python 3 compatible fix. [Tony Wang]
- Remove bug line. [Tony Wang]
- Add setup.py. [Tony Wang]
- Python 3 compatible. [Tony Wang]
- Log by verbose. [Tony Wang]
- Improve pid related. [Tony Wang]

  - is_running: use os.kill to check if it's still running
  - delpid: remove pidfile only if it matches self pid
- Using 'is None' instead of '== None' [will mclafferty]
- Rename for_gevent to use_gevent. [Tony Wang]
- Add gevent support. [Tony Wang]
- Moving signal registration outside signal handler. [will mclafferty]

  also fixing pylint/pep8 warnings
- Fix link. [Ben Sima]
- Raise exception if ``run`` has not been overridden. [Daniel Waardal]

  Raises the builtin NotImplementedError
- Provide more useful output for is_running() [David Mytton]

  As suggested in comments https://github.com/serverdensity/python-daemon/commit/a304de8cef9d3483bf5ffc2b743947f98afb2ed8#commitcomment-9024066
- Final pep8 fixes. [Jouke Thiemo Waleson]
- Added an is_running method. [Jouke Thiemo Waleson]
- Moved get_pid to separate method. [Jouke Thiemo Waleson]
- PEP8ified. [Jouke Thiemo Waleson]
- Send a SIGHUP if process won't die. [Reid Ransom]
- Made Daemon extend object so that it can be extended in the usual way.
  [Jessamyn Smith]
- Add ability to pass arguments to start() and run() [Hadley Rich]
- Stderr forwarded to stdout if is None. [Dmitriy Narkevich]
- Added umask argument. [Dmitriy Narkevich]
- Added verbose argument for prints. [Dmitriy Narkevich]
- Added home_dir argument to __init__ function. [Dmitriy Narkevich]
- Added daemon_alive flag and SIGTERM/SIGINT handler. [Dmitriy
  Narkevich]
- Added notes about foreground mode. [David Mytton]
- Make names consistent. [David Mytton]
- Adjusted URL format in readme. [David Mytton]
- Moved readme to markdown. [David Mytton]
