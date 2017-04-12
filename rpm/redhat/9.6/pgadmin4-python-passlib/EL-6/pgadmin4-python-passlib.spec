%global sname passlib
%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/

%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Name:		pgadmin4-python-%{sname}
Version:	1.6.2
Release:	3%{?dist}
Summary:	Comprehensive password hashing framework supporting over 20 schemes

License:	BSD and Beerware and Copyright only
URL:		http://%{sname}.googlecode.com
Source0:	https://pypi.python.org/packages/source/p/%{sname}/%{sname}-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python2-devel
BuildRequires:	python-setuptools
# docs generation requires python-cloud-sptheme, which isn't packaged yet.
# so we won't generate the docs yet.
#BuildRequires:	python-sphinx >= 1.0
#BuildRequires:	python-cloud-sptheme

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
%{__ospython2} setup.py build

%install
%{__rm} -rf %{buildroot}

%{__ospython2} setup.py install -O1 --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python_sitelib}/%{sname} %{buildroot}%{python_sitelib}/%{sname}-%{version}-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}

%files
%doc LICENSE README
%{pgadmin4py2instdir}/*%{sname}*.egg-info
%{pgadmin4py2instdir}/%{sname}

%changelog
* Wed Apr 12 2017 Devrim Gündüz <devrim@gunduz.org> - 1.6.2-3
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Thu Mar 16 2017 Devrim Gündüz <devrim@gunduz.org> - 1.6.2-2
- Initial packaging for PostgreSQL YUM repository, to satisfy
  dependency of pgadmin4. Spec file is from EPEL 7.
