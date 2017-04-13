%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

%global sname html5lib
%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/

Name:		pgadmin4-python-%{sname}
Summary:	A python based HTML parser/tokenizer
Version:	0.999
Release:	6%{?dist}
Epoch:		1
Group:		Development/Libraries
License:	MIT
URL:		https://pypi.python.org/pypi/%{sname}

Source0:	https://pypi.python.org/packages/source/h/%{sname}/%{sname}-%{version}.tar.gz

BuildArch:	noarch
Requires:	python-six
BuildRequires:	python-setuptools python2-devel
BuildRequires:	python-six python-nose

%description
A python based HTML parser/tokenizer based on the WHATWG HTML5
specification for maximum compatibility with major desktop web browsers.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__ospython2} setup.py build

%install

%{__ospython2} setup.py install -O1 --skip-build --root %{buildroot}
# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname} %{buildroot}%{python2_sitelib}/%{sname}-%{version}-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}

%files
%doc CHANGES.rst README.rst LICENSE
%{pgadmin4py2instdir}/*%{sname}*.egg-info
%{pgadmin4py2instdir}/%{sname}

%changelog
* Thu Apr 13 2017 Devrim Gündüz <devrim@gunduz.org> - 1:0.999-6
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Thu Mar 16 2017 Devrim Gündüz <devrim@gunduz.org> - 1:0.999-5
- Initial packaging for PostgreSQL YUM repository, to satisfy
  dependency of pgadmin4. Spec file is based on EPEL 7.
