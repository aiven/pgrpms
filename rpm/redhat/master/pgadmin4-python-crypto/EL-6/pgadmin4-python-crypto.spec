%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global __ospython2 %{_bindir}/python2

%global _docdir_fmt %{name}
%global sname Crypto

Summary:	Cryptography library for Python
Name:		pgadmin4-python-crypto
Version:	2.6.1
Release:	14%{?dist}
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
BuildRequires:	python-devel >= 2.4
BuildRequires:	python-tools

%description
PyCrypto is a collection of both secure hash functions (such as MD5 and
SHA), and various encryption algorithms (AES, DES, RSA, ElGamal, etc.).

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
%{__rm} -rf src/libtom
%patch3

# setup.py doesn't run 2to3 on pct-speedtest.py
%{__cp} pct-speedtest.py pct-speedtest3.py
2to3 -wn pct-speedtest3.py

%build
%global optflags %{optflags} -fno-strict-aliasing
%{__ospython2} setup.py build

%install
%{__ospython2} setup.py install --skip-build --root %{buildroot}

# Remove group write permissions on shared objects
find %{buildroot}%{python_sitearch} -name '*.so' -exec chmod -c g-w {} \;

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python_sitearch}/%{sname} %{buildroot}%{python_sitearch}/pycrypto-%{version}-py2.*.egg-info %{buildroot}/%{pgadmin4py2instdir}

%files
%doc README TODO ACKS ChangeLog Doc/ COPYRIGHT LEGAL/
%{pgadmin4py2instdir}/Crypto/
%{pgadmin4py2instdir}/pycrypto-%{version}-py2.*.egg-info

%changelog
* Mon Apr 10 2017 Devrim Gündüz <devrim@gunduz.org> - 2.6.1-14
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Thu Mar 16 2017 Devrim Gündüz <devrim@gunduz.org> - 2.6.1-13
- Initial packaging for PostgreSQL YUM repository, to satisfy
  dependency of pgadmin4. Spec file is based on EPEL 7.
