%global modname attrs

%global __ospython %{_bindir}/python3.9
%if 0%{?fedora} >= 35
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Name:           python-attrs
Version:        22.1.0
Release:        1%{?dist}
Summary:        Python attributes without boilerplate

License:        MIT
URL:            http://www.attrs.org/
BuildArch:      noarch
Source0:        https://github.com/hynek/%{modname}/archive/%{version}/%{modname}-%{version}.tar.gz

BuildRequires:  python39-devel
BuildRequires:  python39-setuptools

%description
attrs is an MIT-licensed Python package with class decorators that
ease the chores of implementing the most common attribute-related
object protocols.

%package -n python3-%{modname}
Summary:        %{summary}

%description -n python%{python3_pkgversion}-%{modname}
attrs is an MIT-licensed Python package with class decorators that
ease the chores of implementing the most common attribute-related
object protocols.

%prep
%setup -q -n %{modname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python%{python3_pkgversion}-%{modname}
%license LICENSE
%doc AUTHORS.rst README.rst
%{python3_sitelib}/*

%changelog
* Sun Sep 18 2022 Devrim Gunduz <devrim@gunduz.org>  - 22.1.0-1
- Initial packaging for the PostgreSQL RPM repository to satisfy
  pg_activity dependency. Package is for RHEL 8 only.
