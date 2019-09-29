%global _docdir_fmt %{name}
%global sname Crypto

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} > 25
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?rhel} == 7
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?with_python3}
Name:		pgadmin4-python3-crypto
%else
Name:		pgadmin4-python-crypto
%endif
Summary:	Cryptography library for Python
Version:	2.6.1
Release:	15%{?dist}.1
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

%if 0%{?fedora} > 25
BuildRequires:  python3-devel python3-tools
%endif

%if 0%{?rhel} == 7
BuildRequires:  python2-devel python-tools
%endif

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
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --skip-build --root %{buildroot}

# Remove group write permissions on shared objects
find %{buildroot} -name '*.so' -exec chmod -c g-w {} \;

# Move everything under pgadmin4 web/ directory.
%if 0%{?with_python3}
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitearch}/%{sname} %{buildroot}%{python3_sitearch}/pycrypto-%{version}-py3.*.egg-info %{buildroot}/%{pgadmin4py3instdir}
%else
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python_sitearch}/%{sname} %{buildroot}%{python_sitearch}/pycrypto-%{version}-py2.*.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

%files
%doc README TODO ACKS ChangeLog Doc/ COPYRIGHT LEGAL/
%if 0%{?with_python3}
%{pgadmin4py3instdir}/Crypto/
%{pgadmin4py3instdir}/pycrypto-%{version}-py3.*.egg-info
%else
%{pgadmin4py2instdir}/Crypto/
%{pgadmin4py2instdir}/pycrypto-%{version}-py2.*.egg-info
%endif

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.6.1-15.1
- Rebuild against PostgreSQL 11.0

* Sat Apr 7 2018 Devrim Gündüz <devrim@gunduz.org> - 2.6.1-15
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Mon Apr 10 2017 Devrim Gündüz <devrim@gunduz.org> - 2.6.1-14
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Thu Mar 16 2017 Devrim Gündüz <devrim@gunduz.org> - 2.6.1-13
- Initial packaging for PostgreSQL YUM repository, to satisfy
  dependency of pgadmin4. Spec file is based on EPEL 7.
