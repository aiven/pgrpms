%global __ospython %{_bindir}/python2

%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

%global sname	wsgiref

Summary:	WSGI (PEP 333) Reference Library
Name:		python-%{sname}
Version:	0.1.2
Release:	17%{?dist}
License:	Python
Group:		Development/Languages
URL:		https://pypi.python.org/pypi/%{sname}
Source0:	http://pypi.python.org/packages/source/w/%{sname}/%{sname}-%{version}.zip
BuildRequires:	python-setuptools
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This is a standalone release of the wsgiref library, that
provides validation support for WSGI 1.0.1 (PEP 3333) for
Python versions < 3.2, and includes the new
wsgiref.util.test() utility function.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install --skip-build --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc README.txt
%dir %{python_sitelib}/%{sname}/
%{python_sitelib}/%{sname}/*
%{python_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info/*

%changelog
* Sun Sep 11 2016 Devrim Gündüz <devrim@gunduz.org> - 0.1.2-17
- Use proper macros.

* Sat Sep 10 2016 Devrim Gündüz <devrim@gunduz.org> - 0.1.2-16
- Add Python3 support, and also bump up the release number to
  override Fedora/EPEL repos.

* Mon May 30 2016 Devrim Gündüz <devrim@gunduz.org> - 0.1.2-1
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.
