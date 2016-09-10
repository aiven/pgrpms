%global pypi_name Flask-Login

%if 0%{?fedora}
%global with_python3 1
%else
# EL doesn't have Python 3
%global with_python3 0
%endif

%if 0%{?rhel} && 0%{?rhel} < 7
# EL 6 doesn't have this macro
%global __python2       %{__python}
%global python2_sitelib %{python_sitelib}
%endif

Name:           python-flask-login
Version:        0.3.2
Release:        1%{?dist}
Summary:        User session management for Flask

License:        MIT
URL:            https://github.com/maxcountryman/flask-login
Source0:        https://pypi.python.org/packages/source/F/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%if %{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif # if with_python3

Requires:       python-flask

%description
Flask-Login provides user session management for Flask. It handles the common
tasks of logging in, logging out, and remembering your users' sessions over
extended periods of time.

%if 0%{?with_python3}
%package -n     python3-flask-login
Summary:        User session management for Flask

Requires:       python3-flask

%description -n python3-flask-login
Flask-Login provides user session management for Flask. It handles the common
tasks of logging in, logging out, and remembering your users' sessions over
extended periods of time.
%endif # with_python3


%prep
%setup -q -n %{pypi_name}-%{version}
rm -rf %{pypi_name}.egg-info


%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

%endif # with_python3


%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3

%{__python2} setup.py install --skip-build --root %{buildroot}



%files
%doc README.md LICENSE
%{python2_sitelib}/*
%if 0%{?with_python3}

%files -n python3-flask-login
%doc README.md
%license LICENSE
%{python3_sitelib}/*
%endif # with_python3


%changelog
* Fri Sep 2 2016 Devrim Gündüz <devrim@gunduz.org> - 1:0.3.2-1
- Update to 0.3.2

* Tue May 31 2016 Devrim Gündüz <devrim@gunduz.org> - 1:0.2.11-3
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency. Spec file taken from Fedora repo.
