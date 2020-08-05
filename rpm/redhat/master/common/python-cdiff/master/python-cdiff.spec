%global sname cdiff

%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

Name:		python3-%{sname}
Version:	1.0
Release:	1%{?dist}
Summary:	View colored, incremental diff in a workspace or from stdin, with side by side and auto pager support

License:	BSD
URL:		https://pypi.org/project/%{sname}/
Source0:	https://files.pythonhosted.org/packages/69/6c/301876940e760a8b46c1caacf08c298f511f517c70eec32e43f38e9cc6f5/%{sname}-%{version}.tar.gz

BuildArch:	noarch

Requires:	less python3
BuildRequires:	python3-devel python3-setuptools

%description
Term based tool to view colored, incremental diff in a
Git/Mercurial/Svn workspace or from stdin, with side by side
and auto pager support. Requires python (>= 2.5.0) and less.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

%files
%license LICENSE
%doc README.rst CHANGES.rst
%{_bindir}/cdiff
%{python3_sitelib}/__pycache__/cdiff*
%{python3_sitelib}/cdiff*

%changelog
* Wed Aug 5 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Initial packaging for PostgreSQL RPM repository, to satisfy patroni dependency.
