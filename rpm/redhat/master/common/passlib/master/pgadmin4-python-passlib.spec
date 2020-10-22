%global sname passlib

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

Name:		pgadmin4-python3-%{sname}
Version:	1.7.2
Release:	1%{?dist}
Summary:	Comprehensive password hashing framework supporting over 20 schemes

License:	BSD and Beerware and Copyright only
URL:		http://%{sname}.googlecode.com
Source0:	https://files.pythonhosted.org/packages/source/p/%{sname}/%{sname}-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	python3-devel python3-setuptools

%description
%{sname} is a password hashing library for Python 2 & 3, which provides
cross-platform implementations of over 20 password hashing algorithms,
as well as a framework for managing existing password hashes. It's
designed to be useful for a wide range of tasks, from verifying a hash
found in /etc/shadow, to providing full-strength password hashing for
multi-user application.


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
%license LICENSE
%doc README
%{pgadmin4py3instdir}/*%{sname}*.egg-info
%{pgadmin4py3instdir}/%{sname}

%changelog
* Fri Feb 28 2020 Devrim Gündüz <devrim@gunduz.org> - 1.7.2-1
- Update to 1.7.2
- Switch to PY3 on RHEL 7.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.7.1-1.1
- Rebuild against PostgreSQL 11.0

* Tue Apr 10 2018 Devrim Gündüz <devrim@gunduz.org> - 1.7.1-1
- Update to 1.7.1

* Thu Apr 5 2018 Devrim Gündüz <devrim@gunduz.org> - 1.6.2-4
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the dependencies for that.

* Wed Apr 12 2017 Devrim Gündüz <devrim@gunduz.org> - 1.6.2-3
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Thu Mar 16 2017 Devrim Gündüz <devrim@gunduz.org> - 1.6.2-2
- Initial packaging for PostgreSQL YUM repository, to satisfy
  dependency of pgadmin4. Spec file is from EPEL 7.
