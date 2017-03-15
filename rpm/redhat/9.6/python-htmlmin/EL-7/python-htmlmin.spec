%if 0%{?rhel} && 0%{?rhel} < 6
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%global with_docs 0
%else
%global with_docs 1
%endif

%if 0%{?fedora} > 23
%{!?with_python3:%global with_python3 1}
%global __ospython3 %{_bindir}/python3
%{expand: %%global py3ver %(echo `%{__ospython3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%else
%{!?with_python3:%global with_python3 0}
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%endif

%global pypi_name htmlmin
%global desc A configurable HTML Minifier with safety features.
%global github_owner mankyd
%global github_name %{pypi_name}
%global commit cc611c3c6eabac97aaa4e4e249be6e8910b12abd
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           python-%{pypi_name}
Version:        0.1.10
Release:        6.gitcc611c3%{?dist}
Summary:        HTML Minifier

License:        BSD
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        https://github.com/%{github_owner}/%{github_name}/archive/%{commit}/%{github_name}-%{commit}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel

%description
%{desc}

%{?python_provide:%python_provide python2-%{pypi_name}}

%if 0%{?with_docs}
%package       doc
Summary:       %{summary}
BuildRequires: python-sphinx

%description  doc
%{desc}

Documentation package.
%endif

%prep
%setup -q -n %{github_name}-%{commit}
%{__rm} -rf *.egg-info

%build
%{__ospython2} setup.py build

%if 0%{?with_docs}
# Build doc
cd docs
make html
make man
# Remove hidden dir in doc not to install it
%{__rm} -rf _build/html/.buildinfo
%endif

%install
%{__rm} -rf %{buildroot}
%{__ospython2} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_docs}
# Install man
%{__mkdir} -p %{buildroot}%{_mandir}/man1
install -p -m0644 docs/_build/man/htmlmin.1 %{buildroot}%{_mandir}/man1
%endif

%files -n python-%{pypi_name}
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE README.rst
%else
%license LICENSE
%doc README.rst
%endif
%{_bindir}/htmlmin
%if 0%{?with_docs}
%{_mandir}/man1/*
%endif
%{python2_sitelib}/%{pypi_name}-%{version}-py%{py2ver}.egg-info/
%{python2_sitelib}/%{pypi_name}/

%if 0%{?with_docs}
%files doc
%license LICENSE
%doc docs/_build/html
%endif

%changelog
* Thu Mar 16 2017 Devrim Gündüz <devrim@gunduz.org> - 0.1.10-6.gitcc611c3
- Add a macro for docs, and enable in on RHEL 7 and onwards.

* Mon Feb 13 2017 Devrim Gündüz <devrim@gunduz.org> - 0.1.10-5.gitcc611c3
- Initial packaging for PostgreSQL YUM repo, based on Fedora rawhide spec.

