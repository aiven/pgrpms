Name:		python-passlib
Version:	1.6.2
Release:	2%{?dist}
Summary:	Comprehensive password hashing framework supporting over 20 schemes

License:	BSD and Beerware and Copyright only
URL:		http://passlib.googlecode.com
Source0:	https://pypi.python.org/packages/source/p/passlib/passlib-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python2-devel
BuildRequires:	python-setuptools
# docs generation requires python-cloud-sptheme, which isn't packaged yet.
# so we won't generate the docs yet.
#BuildRequires:	python-sphinx >= 1.0
#BuildRequires:	python-cloud-sptheme

%description
Passlib is a password hashing library for Python 2 & 3, which provides
cross-platform implementations of over 20 password hashing algorithms,
as well as a framework for managing existing password hashes. It's
designed to be useful for a wide range of tasks, from verifying a hash
found in /etc/shadow, to providing full-strength password hashing for
multi-user application.


%prep
%setup -q -n passlib-%{version}


%build
%{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%doc LICENSE README
%{python_sitelib}/*


%changelog
* Thu Mar 16 2017 Devrim Gündüz <devrim@gunduz.org> - 1.6.2-2
- Initial packaging for PostgreSQL YUM repository, to satisfy
  dependency of pgadmin4. Spec file is from EPEL 7.
