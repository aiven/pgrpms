%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global sname importlib

Name:           pgadmin4-python-%{sname}
Version:        1.0.4
Release:        2%{?dist}
Summary:        Backport of importlib.import_module() from Python 2.7

Group:          Development/Languages
License:        Python
URL:            https://pypi.python.org/pypi/%{sname}
Source0:        https://pypi.io/packages/source/i/%{sname}/%{sname}-%{version}.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
Conflicts:      python(abi) = 2.7

%description
This package contains the code from importlib as found in Python 2.7.
It is provided so that people who wish to use importlib.import_module()
with a version of Python prior to 2.7 or in 3.0 have the function
readily available. The code in no way deviates from what can be found
in the 2.7 trunk.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__ospython2} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython2} setup.py install -O1 --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname}* %{buildroot}/%{pgadmin4py2instdir}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.rst
%{pgadmin4py2instdir}/*%{sname}*.egg-info

%changelog
* Wed Apr 12 2017 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-2
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Thu Mar 16 2017 Devrim Gündüz <devrim@gunduz.org> 1.0.4-1
- Update to 1.0.4, for pgadmin4 dependency in PostgreSQL YUM repository.

* Tue Jun 21 2011 Andrew Colin Kissa <andrew@topdog.za.net> 1.0.2-1
- Initial package
