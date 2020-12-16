%define realname	argparse
%define realver		1.4.0

# Common info
Name:          python-%{realname}
Version:       %{realver}
Release:       2.65%{?dist}
License:       Python-2.0
Group:         Development/Languages/Python
URL:           https://github.com/ThomasWaldmann/argparse/
Summary:       Python command-line parsing library

# Install-time parameters
Provides:      python2-%{realname} = %{version}-%{release}
Obsoletes:     python2-%{realname} < %{version}-%{release}
Requires:      python(abi) = %{py_ver}

# Build-time parameters
%if ! 0%{?sles_version}
BuildArch:     noarch
%endif
BuildRequires: python-setuptools
BuildRequires: %python3_pkg-setuptools
BuildRoot:     %{_tmppath}/%{name}-root
Source:        https://pypi.python.org/packages/source/a/%{realname}/%{realname}-%{realver}%{?extraver}.%{srcext}

%description
The argparse module makes it easy to write user friendly command line interfaces.

The program defines what arguments it requires, and argparse will figure out how
to parse those out of sys.argv. The argparse module also automatically generates
help and usage messages and issues errors when users give the program invalid
arguments.

As of Python >= 2.7 and >= 3.2, the argparse module is maintained within the
Python standard library. For users who still need to support Python < 2.7
or < 3.2, it is also provided as a separate package, which tries to stay
compatible with the module in the standard library, but also supports older
Python versions.

%package -n %{python3_pkg}-%{realname}
Group:         Development/Languages/Python
Summary:       Python command-line parsing library

Requires:      python(abi) = %{py3_ver}
Provides:      python3-%{realname} = %{version}-%{release}

%description -n %{python3_pkg}-%{realname}
The argparse module makes it easy to write user friendly command line interfaces.

The program defines what arguments it requires, and argparse will figure out how
to parse those out of sys.argv. The argparse module also automatically generates
help and usage messages and issues errors when users give the program invalid
arguments.

As of Python >= 2.7 and >= 3.2, the argparse module is maintained within the
Python standard library. For users who still need to support Python < 2.7
or < 3.2, it is also provided as a separate package, which tries to stay
compatible with the module in the standard library, but also supports older
Python versions.

# Preparation step (unpackung and patching if necessary)
%prep
%setup -q -c -n python2
%setup -q -c -n python3 -D

%build
cd %{_builddir}/python2/%{realname}-%{version}%{?extraver}
python setup.py build
cd %{_builddir}/python3/%{realname}-%{version}%{?extraver}
%python3 setup.py build

%install
cd %{_builddir}/python2/%{realname}-%{version}%{?extraver}
python setup.py install --prefix=%{_prefix} --root=%{buildroot} -O2
cd %{_builddir}/python3/%{realname}-%{version}%{?extraver}
%python3 setup.py install --prefix=%{_prefix} --root=%{buildroot} -O2

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc %{realname}-%{version}%{?extraver}/LICENSE.txt
%doc %{realname}-%{version}%{?extraver}/NEWS.txt
%doc %{realname}-%{version}%{?extraver}/README.txt
%doc %{realname}-%{version}%{?extraver}/doc/source/Python-License.txt
%doc %{realname}-%{version}%{?extraver}/doc/source/*.rst
%{python_sitelib}/%{realname}.py*
%{python_sitelib}/%{realname}-%{version}-py%{py_ver}.egg-info/

%files -n %{python3_pkg}-%{realname}
%doc %{realname}-%{version}%{?extraver}/LICENSE.txt
%doc %{realname}-%{version}%{?extraver}/NEWS.txt
%doc %{realname}-%{version}%{?extraver}/README.txt
%doc %{realname}-%{version}%{?extraver}/doc/source/Python-License.txt
%doc %{realname}-%{version}%{?extraver}/doc/source/*.rst
%{python3_sitelib}/%{realname}.py*
%{python3_sitelib}/%{realname}-%{version}-py%{py3_ver}.egg-info/
%{python3_sitelib}/__pycache__/%{realname}.cpython-%{py3_gen}.*

%changelog
* Tue May 14 2019 Alexander Evseev <aevseev@gmail.com>
- Build Python 3.x package
* Tue Apr 26 2016 aevseev@gmail.com
- New upstream version - 1.4.0
