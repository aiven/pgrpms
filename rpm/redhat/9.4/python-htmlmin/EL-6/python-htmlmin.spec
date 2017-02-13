%global pypi_name htmlmin
%global desc A configurable HTML Minifier with safety features.
%global github_owner mankyd
%global github_name %{pypi_name}
%global commit cc611c3c6eabac97aaa4e4e249be6e8910b12abd
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Name:           python-%{pypi_name}
Version:        0.1.10
Release:        5.gitcc611c3%{?dist}
Summary:        HTML Minifier

License:        BSD
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        https://github.com/%{github_owner}/%{github_name}/archive/%{commit}/%{github_name}-%{commit}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel

%description
%{desc}

%{?python_provide:%python_provide python2-%{pypi_name}}

%package       doc
Summary:       %{summary}
BuildRequires: python-sphinx

%description  doc
%{desc}

Documentation package.

%prep
%setup -q -n %{github_name}-%{commit}
%{__rm} -rf *.egg-info


%build
%{__ospython2} setup.py build

# Build doc
cd docs
make html
make man
# Remove hidden dir in doc not to install it
%{__rm} -rf _build/html/.buildinfo


%install
%{__rm} -rf %{buildroot}
%{__ospython2} setup.py install --skip-build --root %{buildroot}

# Install man
%{__mkdir} -p %{buildroot}%{_mandir}/man1
install -p -m0644 docs/_build/man/htmlmin.1 %{buildroot}%{_mandir}/man1

%files -n python-%{pypi_name}
%license LICENSE
%doc README.rst
%{_bindir}/htmlmin
%{_mandir}/man1/*
%{python2_sitelib}/%{pypi_name}-%{version}-py%{py2ver}.egg-info/
%{python2_sitelib}/%{pypi_name}/

%files doc
%license LICENSE
%doc docs/_build/html

%changelog
* Mon Feb 13 2017 Devrim Gündüz <devrim@gunduz.org> - 0.1.10-5.gitcc611c3
- Initial packaging for PostgreSQL YUM repo, based on Fedora rawhide spec.

