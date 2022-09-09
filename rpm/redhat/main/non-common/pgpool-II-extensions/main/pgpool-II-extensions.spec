%global debug_package %{nil}
%global sname pgpool-II

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	PostgreSQL extensions for pgpool-II
Name:		%{sname}-pg%{pgmajorversion}-extensions
Version:	4.3.3
Release:	1%{?dist}
License:	BSD
URL:		http://pgpool.net
Source0:	http://www.pgpool.net/mediawiki/images/%{sname}-%{version}.tar.gz
Requires:	postgresql%{pgmajorversion}-server %{sname}-pcp

BuildRequires:	postgresql%{pgmajorversion}-devel pam-devel
BuildRequires:	libmemcached-devel openssl-devel pgdg-srpm-macros >= 1.0.21

Requires:	libmemcached
Requires:	%{sname}

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
PostgreSQL extensions, libraries and sql files for pgpool-II.

%prep
%setup -q -n %{sname}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

# We need this flag on SLES so that pgpool can find libmemched.
# Otherwise, we get "libmemcached.so: undefined reference to `pthread_once'" error.
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
	export LDFLAGS='-lpthread'
%endif
%endif
%ifarch ppc64 ppc64le
%configure --build=ppc64le \
%else
./configure \
%endif
	--prefix /usr \
	--libdir %{_libdir} \
	--disable-static \
	--sysconfdir=%{_sysconfdir}/%{name}/ \
	--with-ldap \
	--with-memcached=%{_includedir}/libmemcached \
	--with-openssl \
	--with-pam \
	--with-pgsql=%{pginstdir}

# https://fedoraproject.org/wiki/Packaging:Guidelines#Removing_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

export PATH=%{pginstdir}/bin/:$PATH
USE_PGXS=1 %{__make} %{?_smp_mflags}
USE_PGXS=1 %{__make} %{?_smp_mflags} -C src/sql/pgpool_adm
USE_PGXS=1 %{__make} %{?_smp_mflags} -C src/sql/pgpool-recovery
USE_PGXS=1 %{__make} %{?_smp_mflags} -C src/sql/pgpool-regclass

%install
export PATH=%{pginstdir}/bin/:$PATH
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install -C src/sql/pgpool_adm
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install -C src/sql/pgpool-recovery
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install -C src/sql/pgpool-regclass

# nuke libtool archive and static lib
%{__rm} -f %{buildroot}%{_libdir}/libpcp.{a,la}
# Remove bitcode files
%{__rm} -rf %{buildroot}%{pginstdir}/lib/bitcode/

%files
%doc README AUTHORS
%license COPYING
%{pginstdir}/lib/pgpool_adm.so
%{pginstdir}/lib/pgpool-recovery.so
%{pginstdir}/share/extension/pgpool_adm*.sql
%{pginstdir}/share/extension/pgpool_adm.control
%{pginstdir}/share/extension/pgpool-regclass.sql
%{pginstdir}/share/extension/pgpool_regclass--1.0.sql
%{pginstdir}/share/extension/pgpool_regclass.control
%{pginstdir}/share/extension/pgpool-recovery.sql
%{pginstdir}/share/extension/pgpool_recovery*.sql
%{pginstdir}/share/extension/pgpool_recovery.control
%{pginstdir}/lib/pgpool-regclass.so

%changelog
* Fri Aug 19 2022 Devrim Gündüz <devrim@gunduz.org> - 4.3.3-1
- Update to 4.3.3
- Build with --with-ldap, per #7687 .

* Thu May 19 2022 Devrim Gündüz <devrim@gunduz.org> - 4.3.2-1
- Update to 4.3.2

* Mon Feb 21 2022 Devrim Gündüz <devrim@gunduz.org> - 4.3.1-1
- Update to 4.3.1

* Tue Dec 28 2021 Devrim Gündüz <devrim@gunduz.org> - 4.3.0-1
- Initial packaging for 4.3 series.
