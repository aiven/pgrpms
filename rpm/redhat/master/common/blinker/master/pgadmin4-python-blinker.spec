%global sname blinker

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

Name:		pgadmin4-python3-%{sname}
Version:	1.4
Release:	4%{?dist}
Summary:	Fast, simple object-to-object and broadcast signaling
License:	MIT
URL:		http://discorporate.us/projects/Blinker/
Source0:	https://pypi.python.org/packages/source/b/%{sname}/%{sname}-%{version}.tar.gz
BuildArch:	noarch

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7
BuildRequires:	python3-devel python3-setuptools
%endif

%description
Blinker provides a fast dispatching system that allows any number
of interested parties to subscribe to events, or "signals".

%prep
%setup -q -n %{sname}-%{version}

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname} %{buildroot}%{python3_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}

%files
%doc docs/ CHANGES LICENSE README.md
%{pgadmin4py3instdir}/*%{sname}*.egg-info
%{pgadmin4py3instdir}/%{sname}

%changelog
* Sat Feb 29 2020 Devrim Gündüz <devrim@gunduz.org> - 1.4-4
- Switch to PY3 on RHEL 7.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.4-3.1
- Rebuild against PostgreSQL 11.0

* Fri Apr 6 2018 Devrim Gündüz <devrim@gunduz.org> - 1.4-3
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Mon Apr 10 2017 Devrim Gündüz <devrim@gunduz.org> - 1.4-2
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Sun Oct 2 2016 Devrim Gündüz <devrim@gunduz.org> - 1.4-1
- Initial packaging for PostgreSQL YUM repository, to satisfy
  pgadmin4 dependencies.
