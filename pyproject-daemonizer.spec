%global srcname daemonizer

Name:           python-%{srcname}
Version:        1.1.0
Release:        1%{?dist}
Summary:        Python daemonizer for Unix, Linux and OS X

License:        CC-BY-SA-3.0
URL:            https://github.com/sarnold/python-daemonizer
Source0:        %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

%global _description %{expand:
A Python class to daemonize your Python script so it can continue
running in the background. It works on Unix, Linux and OS X, creates a
PID file and has standard commands (start, stop, restart) plus a
foreground mode.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}

# this does not work with pyproject_rpm_macros since RH 9.6 is way too old
# to meet the current build requirement versions
BuildRequires: python3-devel
BuildRequires: pyproject-rpm-macros
BuildRequires: python3dist(tomli)
BuildRequires: python3dist(setuptools)
BuildRequires: python3dist(setuptools-scm[toml])

%description -n python3-%{srcname} %_description

%prep
%autosetup -p1 -n %{name}-%{version}

# using pyproject macros
%generate_buildrequires
%pyproject_buildrequires -x test

%build
%pyproject_wheel

%install
%pyproject_install

# Use -l to assert a %%license file is found (PEP 639).
%pyproject_save_files -l daemonizer

%check
%pyproject_check_import
%pytest

%files -n python3-daemonizer -f %{pyproject_files}

%changelog
* Fri Jun 27 2025 Stephen Arnold <nerdboy@gentoo.org> - 1.1.0
- Initial package
