%global _docdir_fmt %{name}

# For consistency and completeness
%global python2_pkgversion 2

Summary:	Cryptography library for Python
Name:		python-crypto
Version:	2.6.1
Release:	13%{?dist}
# Mostly Public Domain apart from parts of HMAC.py and setup.py, which are Python
License:	Public Domain and Python
URL:		http://www.pycrypto.org/
Source0:	http://ftp.dlitz.net/pub/dlitz/crypto/pycrypto/pycrypto-%{version}.tar.gz
Patch0:		python-crypto-2.4-optflags.patch
Patch1:		python-crypto-2.4-fix-pubkey-size-divisions.patch
Patch2:		pycrypto-2.6.1-CVE-2013-7459.patch
Patch3:		pycrypto-2.6.1-unbundle-libtomcrypt.patch
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	gcc
BuildRequires:	gmp-devel >= 4.1
BuildRequires:	libtomcrypt-devel >= 1.16
BuildRequires:	python%{python2_pkgversion}-devel >= 2.4
BuildRequires:	python-tools

%description
PyCrypto is a collection of both secure hash functions (such as MD5 and
SHA), and various encryption algorithms (AES, DES, RSA, ElGamal, etc.).

%package -n python%{python2_pkgversion}-crypto
Summary:	Cryptography library for Python 2
Provides:	pycrypto = %{version}-%{release}
%{?python_provide:%python_provide python2-crypto}

%description -n python%{python2_pkgversion}-crypto
PyCrypto is a collection of both secure hash functions (such as MD5 and
SHA), and various encryption algorithms (AES, DES, RSA, ElGamal, etc.).

This is the Python 2 build of the package.

%prep
%setup -n pycrypto-%{version} -q

# Use distribution compiler flags rather than upstream's
%patch0 -p1

# Fix divisions within benchmarking suite:
%patch1 -p1

# AES.new with invalid parameter crashes python
# https://github.com/dlitz/pycrypto/issues/176
# CVE-2013-7459
%patch2 -p1

# Unbundle libtomcrypt (#1087557)
rm -rf src/libtom
%patch3

# setup.py doesn't run 2to3 on pct-speedtest.py
cp pct-speedtest.py pct-speedtest3.py
2to3 -wn pct-speedtest3.py

%build
%global optflags %{optflags} -fno-strict-aliasing
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root %{buildroot}

# Remove group write permissions on shared objects
find %{buildroot}%{python2_sitearch} -name '*.so' -exec chmod -c g-w {} \;

%files -n python%{python2_pkgversion}-crypto
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc README TODO ACKS ChangeLog Doc/ COPYRIGHT LEGAL/
%else
%license COPYRIGHT LEGAL/
%doc README TODO ACKS ChangeLog Doc/
%endif
%{python2_sitearch}/Crypto/
%{python2_sitearch}/pycrypto-%{version}-py2.*.egg-info

%changelog
* Thu Mar 16 2017 Devrim Gündüz <devrim@gunduz.org> - 2.6.1-13
- Initial packaging for PostgreSQL YUM repository, to satisfy
  dependency of pgadmin4. Spec file is based on EPEL 7.
