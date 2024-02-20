%global sname plac
%if 0%{?fedora} >= 35
%{expand: %%global py3ver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global py3ver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif

%global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")


Name:		python3-plac
Version:	1.3.5
Release:	1PGDG%{?dist}
Summary:	The smartest command line arguments parser in the world
License:	BSD-2-Clause
URL:		https://github.com/ialbert/plac
Source0:	https://github.com/ialbert/plac/archive/v%{version}/plac-%{version}.tar.gz
# Man page written for Fedora in groff_man(7) format based on --help output
Source1:	plac_runner.py.1

BuildArch:	noarch

BuildRequires:	python3-devel

%description
plac is a Python package that can generate command line parameters from
function signatures.

plac works on Python 2.6 through all versions of Python 3.

plac has no dependencies beyond modules already present in the Python standard
library.

plac implements most of its functionality in a single file that may be included
in your source code.}

%prep
%setup -q -n plac-%{version}

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --no-compile --root %{buildroot}

# Install man file
%{__install} -t '%{buildroot}%{_mandir}/man1' -m 0644 -p -D '%{SOURCE1}'

# Create __pycache__ directories and their contents in SLES *too*:
%if 0%{?suse_version}
%py3_compile %{buildroot}%{python3_sitelib}
%endif

%files
%doc CHANGES.md README.md RELEASE.md
%{_bindir}/plac_runner.py
%{_mandir}/man1/plac_runner.py.1*
%dir %{python3_sitelib}/%{sname}-%{version}-py%{py3ver}.egg-info
%{python3_sitelib}/%{sname}-%{version}-py%{py3ver}.egg-info/*
%{python3_sitelib}/%{sname}*py
%{python3_sitelib}/__pycache__/%{sname}*pyc

%changelog
* Tue Feb 20 2024 Devrim Gündüz <devrim@gunduz.org> - 1.3.5-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support
  pg_statviz on RHEL 8 and SLES 15.
