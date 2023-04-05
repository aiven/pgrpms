%global __ospython %{_bindir}/python3.9
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

%global sname wcwidth

Name:           python39-%{sname}
Version:        0.2.5
Release:        11%{?dist}
Summary:        Measures number of Terminal column cells of wide-character codes

License:        MIT
URL:            https://github.com/jquast/wcwidth
Source0:        %pypi_source
BuildArch:      noarch
BuildRequires:  python39-devel
BuildRequires:  python39-setuptools

%description
This API is mainly for Terminal Emulator implementors, or those writing programs
that expect to interpreted by a terminal emulator and wish to determine the
printable width of a string on a Terminal.

%prep
%setup -q -n %{sname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python39-%{sname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{sname}
%{python3_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info

%changelog
* Wed Apr 5 2023 Devrim Gunduz <devrim@gunduz.org>  - 22.1.0-1
- Initial packaging for the PostgreSQL RPM repository to satisfy
  pg_activity dependency. Package is for RHEL 8 only.

