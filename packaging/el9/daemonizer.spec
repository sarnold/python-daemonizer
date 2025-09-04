# Tests are disabled in RHEL 9 because really old tox
# Specify --with tests to enable them.
%bcond_with tests

%global srcname daemonizer

Name:           python-%{srcname}
Version:        VER_GOES_HERE
Release:        1%{?dist}
Summary:        Python daemonizer for Unix, Linux and OS X

License:        CC-BY-SA-3.0
URL:            https://github.com/sarnold/python-daemonizer
Source0:        %{url}/releases/download/%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python%{python3_pkgversion}dist(tomli)
BuildRequires:  python%{python3_pkgversion}dist(wheel)
BuildRequires:  python%{python3_pkgversion}dist(setuptools)
BuildRequires:  python%{python3_pkgversion}dist(setuptools-scm[toml])
%if %{with tests}
BuildRequires:  python%{python3_pkgversion}dist(pytest)
%endif

%description
A Python class to daemonize your Python script so it can continue
running in the background. It works on Unix, Linux and OS X, creates a
PID file and has standard commands (start, stop, restart) plus a
foreground mode.

%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}

%description -n python%{python3_pkgversion}-%{srcname}
A Python class to daemonize your Python script so it can continue
running in the background. It works on Unix, Linux and OS X, creates a
PID file and has standard commands (start, stop, restart) plus a
foreground mode.

%prep
%autosetup -p1 -n %{srcname}-%{version}

# using pyproject macros
%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install

# Use -l to assert a %%license file is found (PEP 639).
# note the last argument is the top-level module directory name
%pyproject_save_files -l daemonizer

%check
%pyproject_check_import
%if %{with tests}
%pytest -vv test/
%endif

%files -n python%{python3_pkgversion}-daemonizer -f %{pyproject_files}
%doc README.rst CHANGELOG.rst
%license LICENSES REUSE.toml

%changelog
* Wed Sep 04 2025 Stephen Arnold <nerdboy@gentoo.org> - 1.1.5
- Update packaging and build env, stop generating version file
* Wed Sep 03 2025 Stephen Arnold <nerdboy@gentoo.org> - 1.1.4
- Pick up previous release, test packaging
* Sat Jul 12 2025 Stephen Arnold <nerdboy@gentoo.org> - 1.1.3
- Bump package release number for spec change
* Sat Jul 12 2025 Stephen Arnold <nerdboy@gentoo.org> - 1.1.3
- Initial package
