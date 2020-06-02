%global debug_package %{nil}
%global pgmajorversion 12
%global	pgprevversion 11

# Macros that define the configure parameters:
%{!?kerbdir:%global kerbdir "/usr"}

%{!?ssl:%global ssl 1}

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?systemd_enabled:%global systemd_enabled 0}
%{!?selinux:%global selinux 0}
%else
%{!?systemd_enabled:%global systemd_enabled 1}
%{!?selinux:%global selinux 1}
%endif

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	PostgreSQL Client Library
Name:		libpq5
Version:	%{pgmajorversion}.3
Release:	10PGDG%{?dist}
License:	PostgreSQL
Url:		https://www.postgresql.org/

Source0:	https://download.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2

Patch1:		%{name}-rpm-pgsql.patch
Patch5:		%{name}-var-run-socket.patch

BuildRequires:	gcc glibc-devel bison flex >= 2.5.31
BuildRequires:	readline-devel zlib-devel >= 1.0.4

Requires:	/sbin/ldconfig

BuildRequires:	krb5-devel
BuildRequires:	e2fsprogs-devel

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	openldap2-devel
%endif
%else
BuildRequires:	openldap-devel
%endif

BuildRequires:	gettext >= 0.10.35

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

%if 0%{?rhel} && 0%{?rhel} <= 6
Requires:	openssl
%else
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
Requires:	libopenssl1_0_0
%else
Requires:	openssl-libs >= 1.0.2k
%endif
%endif

Conflicts:	libpq
Obsoletes:	libpq
Provides:	postgresql-libs >= 9.2 libpq >= 10.0 libpq.so.5
Provides:	libpq.so.5(RHPG_10)(64bit)
Provides:	libpq.so.5(RHPG_12)(64bit)
Provides:	libpq.so.5(RHPG_9.6)(64bit)

%description
The libpq5 package provides the essential shared libraries for any
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package devel
Summary:	Development files for building PostgreSQL client tools
Requires:	%name%{?_isa} = %version-%release
# Historically we had 'postgresqlXX-devel' package which was used for building
# both PG clients and PG server modules;  let's have this fake provide to cover
# most of the depending packages and the rest (those which want to build server
# modules) need to be fixed to require postgresql-server-devel package.

%description devel
The libpq5 package provides the essential shared library for any PostgreSQL
client program or interface.  You will need to install this package to build any
package or any clients that need to connect to a PostgreSQL server.

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

export PYTHON=/usr/bin/python3

# These configure options must match main build
%configure --disable-rpath \
%if %ssl
	--with-openssl \
%endif
	--with-gssapi \
	--with-includes=%{kerbdir}/include \
	--with-libraries=%{kerbdir}/%{_lib} \
	--enable-nls \
	--with-ldap \
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
	--with-system-tzdata=%{_datadir}/zoneinfo

%global build_subdirs \\\
	src/include \\\
	src/common \\\
	src/port \\\
	src/interfaces/libpq \\\
	src/bin/pg_config

for subdir in %build_subdirs; do
MAKELEVEL=0 %make_build -C "$subdir"
done

%install
%{__rm} -rf %{buildroot}

for subdir in %build_subdirs; do
MAKELEVEL=0	%make_install -C "$subdir"
done

# remove files not to be packaged
find %{buildroot} -name '*.a' -delete
rm -r %{buildroot}%_includedir/pgsql/server

%{__cp} /dev/null libs.lst

find_lang_bins ()
{
    lstfile=$1 ; shift
    cp /dev/null "$lstfile"
    for binary; do
	%find_lang "$binary"-%pgmajorversion
	cat "$binary"-%pgmajorversion.lang >>"$lstfile"
    done
}

find_lang_bins %name.lst	libpq5
find_lang_bins %name-devel.lst	pg_config

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

# FILES section.

%files -f %name.lst
%defattr(-,root,root)
%{_libdir}/libpq.so*
%doc %_datadir/pgsql/pg_service.conf.sample

%files devel -f %name-devel.lst
%_bindir/pg_config
%_includedir/*
%_libdir/libpq.so
%_libdir/pkgconfig/libpq.pc

%changelog
* Tue Jun 2 2020 Devrim Gündüz <devrim@gunduz.org> - 12.3-10PGDG
- Rework on the spec file, using Fedora's spec file.
- Update to 12.3
- Also provide libpq, to override OS package.

* Fri Apr 17 2020 Devrim Gündüz <devrim@gunduz.org> - 12.2-1PGDG
- Initial packaging for PostgreSQL RPM repository
