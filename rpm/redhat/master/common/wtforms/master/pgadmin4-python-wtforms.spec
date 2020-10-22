%global mod_name WTForms
%global sname wtforms

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif
Name:		pgadmin4-python3-%{sname}
Version:	2.2.1
Release:	2%{?dist}
Summary:	Forms validation and rendering library for python

License:	BSD
URL:		http://wtforms.simplecodes.com/
Source0:	https://github.com/wtforms/wtforms/archive/%{version}.tar.gz

BuildArch:	noarch

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7
BuildRequires:	python3-devel python3-setuptools
%endif

%description
With wtforms, your form field HTML can be generated for you.
This allows you to maintain separation of code and presentation,
and keep those messy parameters out of your python code.

%prep
%setup -q -n wtforms-%{version}
sed -i "s|\r||g" docs/conf.py
sed -i "s|\r||g" docs/Makefile
sed -i "s|\r||g" docs/index.rst
%{__rm} -f docs/html/.buildinfo

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname} %{buildroot}%{python3_sitelib}/%{mod_name}-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}

%files
%license LICENSE.rst
%doc docs/
%{pgadmin4py3instdir}/*%{mod_name}*.egg-info
%{pgadmin4py3instdir}/%{sname}

%changelog
* Sat Feb 29 2020 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-2
- Switch to PY3 on RHEL 7

* Thu Apr 18 2019 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-1
- Update to 2.2.1

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.1-3.1
- Rebuild against PostgreSQL 11.0

* Sun Apr 8 2018 Devrim Gündüz <devrim@gunduz.org> - 2.1-3
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Mon Apr 10 2017 Devrim Gündüz <devrim@gunduz.org> - 2.1-2
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 2.1-1
- Initial packaging for PostgreSQL YUM repository, to satisfy pgadmin4 dependency.
