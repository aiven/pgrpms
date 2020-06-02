%global debug_package %{nil}
%global pgmajorversion 12
%global pgpackageversion 12
%global sname pgdg-libpq5
%global pgbaseinstdir	/usr/lib64/%{sname}/

# Macros that define the configure parameters:
%{!?kerbdir:%global kerbdir "/usr"}
%{!?disablepgfts:%global disablepgfts 0}

%if 0%{?rhel} || 0%{?suse_version} >= 1315
%{!?enabletaptests:%global enabletaptests 0}
%else
%{!?enabletaptests:%global enabletaptests 1}
%endif

%{!?icu:%global icu 1}
%{!?kerberos:%global kerberos 1}
%{!?ldap:%global ldap 1}
%{!?nls:%global nls 1}
%{!?pam:%global pam 1}

%{!?pltcl:%global pltcl 1}
%{!?plperl:%global plperl 1}
%{!?ssl:%global ssl 1}
%{!?test:%global test 1}
%{!?xml:%global xml 1}

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?systemd_enabled:%global systemd_enabled 0}
%{!?sdt:%global sdt 0}
%{!?selinux:%global selinux 0}
# LLVM version in RHEL 6 is not sufficient to build LLVM
%{!?llvm:%global llvm 0}
%else
%{!?systemd_enabled:%global systemd_enabled 1}
%ifarch ppc64 ppc64le s390 s390x armv7hl
%{!?llvm:%global llvm 0}
%{!?sdt:%global sdt 0}
%else
%{!?llvm:%global llvm 1}
 %{!?sdt:%global sdt 1}
%endif
%{!?selinux:%global selinux 1}
%endif

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	The shared libraries required for some PGDG packages
Name:		pgdg-libpq5
Version:	%{pgmajorversion}.3
Release:	1PGDG%{?dist}
License:	PostgreSQL
Url:		https://www.postgresql.org/

Source0:	https://download.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2
Source9:	%{name}-libs.conf

Patch1:		%{name}-rpm-pgsql.patch
Patch5:		%{name}-var-run-socket.patch

BuildRequires:	perl glibc-devel bison flex >= 2.5.31
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	readline-devel zlib-devel >= 1.0.4

# This dependency is needed for Source 16:
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:	perl-generators
%endif

Requires:	/sbin/ldconfig

%if %icu
BuildRequires:	libicu-devel
Requires:	libicu
%endif

%if %llvm
%if 0%{?rhel} && 0%{?rhel} == 7
# Packages come from EPEL and SCL:
BuildRequires:	llvm5.0-devel >= 5.0 llvm-toolset-7-clang >= 4.0.1
%endif
%if 0%{?rhel} && 0%{?rhel} >= 8
# Packages come from Appstream:
BuildRequires:	llvm-devel >= 8.0.1 clang-devel >= 8.0.1
%endif
%if 0%{?fedora}
BuildRequires:	llvm-devel >= 5.0 clang-devel >= 5.0
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm10-devel clang10-devel
%endif
%endif

%if %kerberos
BuildRequires:	krb5-devel
BuildRequires:	e2fsprogs-devel
%endif

%if %ldap
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	openldap2-devel
%endif
%else
BuildRequires:	openldap-devel
%endif
%endif

%if %nls
BuildRequires:	gettext >= 0.10.35
%endif

%if %pam
BuildRequires:	pam-devel
%endif

%if %plperl
%if 0%{?rhel} && 0%{?rhel} >= 7
BuildRequires:	perl-ExtUtils-Embed
%endif
%if 0%{?fedora} >= 22
BuildRequires:	perl-ExtUtils-Embed
%endif
%endif

%if %pltcl
BuildRequires:	tcl-devel
%endif

%if %sdt
BuildRequires:	systemtap-sdt-devel
%endif

%if %selinux
# All supported distros have libselinux-devel package:
BuildRequires:	libselinux-devel >= 2.0.93
# SLES: SLES 15 does not have selinux-policy package. Use
# it only on SLES 12:
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	selinux-policy >= 3.9.13
%endif
# RHEL/Fedora has selinux-policy:
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	selinux-policy >= 3.9.13
%endif
%endif

%if %ssl
# We depend un the SSL libraries provided by Advance Toolchain on PPC,
# so use openssl-devel only on other platforms:
%ifnarch ppc64 ppc64le
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	libopenssl-devel
%else
BuildRequires:	openssl-devel
%endif
%endif
%endif

%if %xml
BuildRequires:	libxml2-devel libxslt-devel
%endif

%if 0%{?rhel} && 0%{?rhel} <= 6
Requires:	openssl
%else
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
Requires:	libopenssl1_0_0
%else
Requires:	openssl-libs >= 1.0.2k
%endif
%endif

Provides:	postgresql-libs >= 9.2, libpq5 >= 10.0

%description
The %{sname} package provides the essential shared libraries for any
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif


%prep
%setup -q -n postgresql-%{version}
%patch1 -p0
%patch5 -p0

%build
CFLAGS="${CFLAGS:-%optflags}"
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%else
	# Strip out -ffast-math from CFLAGS....
	CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`
	%if 0%{?rhel}
	LDFLAGS="-Wl,--as-needed"; export LDFLAGS
	%endif
%endif

export CFLAGS

%if %icu
# Export ICU flags on RHEL 6:
%if 0%{?rhel} && 0%{?rhel} <= 6
	ICU_CFLAGS='-I%{_includedir}'; export ICU_CFLAGS
	ICU_LIBS='-L%{_libdir} -licui18n -licuuc -licudata'; export ICU_LIBS
%endif
%endif

export PYTHON=/usr/bin/python3

%if %llvm
%if 0%{?rhel} && 0%{?rhel} == 7
	export CLANG=/opt/rh/llvm-toolset-7/root/usr/bin/clang LLVM_CONFIG=%{_libdir}/llvm5.0/bin/llvm-config
%endif
%if 0%{?rhel} && 0%{?rhel} == 8
	export CLANG=%{_bindir}/clang LLVM_CONFIG=%{_bindir}/llvm-config-64
%endif
%endif

# These configure options must match main build
./configure --enable-rpath \
	--prefix=%{pgbaseinstdir} \
	--includedir=%{pgbaseinstdir}/include \
	--mandir=%{pgbaseinstdir}/share/man \
	--datadir=%{pgbaseinstdir}/share \
	--libdir=%{pgbaseinstdir}/lib \
%if %enabletaptests
	--enable-tap-tests \
%endif
%if %icu
	--with-icu \
%endif
%if %plperl
	--with-perl \
%endif
%if %pltcl
	--with-tcl \
	--with-tclconfig=%{_libdir} \
%endif
%if %ssl
	--with-openssl \
%endif
%if %pam
	--with-pam \
%endif
%if %kerberos
	--with-gssapi \
	--with-includes=%{kerbdir}/include \
	--with-libraries=%{kerbdir}/%{_lib} \
%endif
%if %nls
	--enable-nls \
%endif
%if %sdt
	--enable-dtrace \
%endif
%if %disablepgfts
	--disable-thread-safety \
%endif
%if %xml
	--with-libxml \
	--with-libxslt \
%endif
%if %ldap
	--with-ldap \
%endif
%if %selinux
	--with-selinux \
%endif
%if %{systemd_enabled}
	--with-systemd \
%endif
%ifarch ppc64 ppc64le
	--with-includes=%{atpath}/include \
	--with-libraries=%{atpath}/lib64 \
%endif
	--with-system-tzdata=%{_datadir}/zoneinfo \
	--sysconfdir=%{_sysconfdir}/sysconfig/pgsql \
	--docdir=%{pgbaseinstdir}/doc \
	--htmldir=%{pgbaseinstdir}/doc/html

MAKELEVEL=0 %{__make} %{?_smp_mflags} all

%install
%{__rm} -rf %{buildroot}

pushd src/interfaces/libpq
%{__make} DESTDIR=%{buildroot} install
popd

# Install linker config file
%{__install} -d -m 755 %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%{__install} -m 700 %{SOURCE9} %{buildroot}%{_sysconfdir}/ld.so.conf.d/

# Remove some files
%{__rm} -f %{buildroot}%{pgbaseinstdir}/share/pgsql/pg_service.conf.sample
%{__rm} -rf %{buildroot}%{pgbaseinstdir}/include
%{__rm} -f %{buildroot}%{pgbaseinstdir}/lib/pkgconfig/libpq.pc
%{__rm} -f %{buildroot}%{pgbaseinstdir}/lib/libpq.a

# initialize file lists
%{__cp} /dev/null libs.lst

%find_lang libpq5-%{pgmajorversion}
cat libpq5-%{pgmajorversion}.lang > pg_libpq5.lst

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

# FILES section.

%files -f pg_libpq5.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/libpq.so*
%%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{sname}-libs.conf

%changelog
* Tue Jun 2 2020 Devrim Gündüz <devrim@gunduz.org> - 12.3-1PGDG
- Update to 12.3
- Also provide libpq5

* Fri Apr 17 2020 Devrim Gündüz <devrim@gunduz.org> - 12.2-1PGDG
- Initial packaging for PostgreSQL RPM repository
