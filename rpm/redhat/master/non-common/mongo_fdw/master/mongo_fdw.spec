%global pgmajorversion 13
%global sname mongo_fdw
%global relver 5_2_9

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

%if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
 %ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
 %{!?llvm:%global llvm 0}
 %else
 %{!?llvm:%global llvm 1}
 %endif
 %else
 %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 0}
%endif

Summary:	PostgreSQL foreign data wrapper for MongoDB
Name:		%{sname}_%{pgmajorversion}
Version:	5.2.9
Release:	1%{?dist}
License:	LGPLv3
URL:		https://github.com/EnterpriseDB/%{sname}
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/REL-%{relver}.tar.gz
Source1:	%{sname}-config.h
%ifarch ppc64 ppc64le
Patch0:		mongo_fdw-autogen-ppc64le.patch
%endif

BuildRequires:	postgresql%{pgmajorversion}-devel wget pgdg-srpm-macros

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
Requires:		libsnappy1 libbson-1_0-0 libmongoc-1_0-0
BuildRequires:		snappy-devel libbson-1_0-0-devel libmongoc-1_0-0-devel
BuildRequires:		libopenssl-devel
%endif
%else
# use pgdg-libmongoc and pgdg-libmongoc-devel packages for rhel7
%if 0%{?rhel} == 7
Requires:	snappy
Requires:	pgdg-libmongoc-libs
BuildRequires:	pgdg-libmongoc-devel snappy-devel
BuildRequires:	openssl-devel cyrus-sasl-devel krb5-devel
BuildRequires:	libbson-devel
%else
Requires:	snappy
Requires:	mongo-c-driver-libs
BuildRequires:	mongo-c-driver-devel snappy-devel
BuildRequires:	openssl-devel cyrus-sasl-devel krb5-devel
BuildRequires:	libbson-devel
%endif
%endif

Requires:	postgresql%{pgmajorversion}-server cyrus-sasl-lib
Requires:	libbson

Obsoletes:	%{sname}%{pgmajorversion} < 5.2.7-2

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
This PostgreSQL extension implements a Foreign Data Wrapper (FDW) for
MongoDB.


%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for mongo_fdw
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} == 1315
Requires:	llvm
%endif
%if 0%{?suse_version} >= 1500
Requires:	llvm10
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 5.0
%endif

%description llvmjit
This packages provides JIT support for mongo_fdw
%endif

%prep
%setup -q -n %{sname}-REL-%{relver}
%ifarch ppc64 ppc64le
%patch0 -p0
%endif
%{__cp} %{SOURCE1} ./config.h

sed -i 's|^[[:space:]]checkout_mongo_driver|#checkout_mongo_driver|' autogen.sh
sed -i 's|^[[:space:]]install_mongoc_driver|#install_mongo_driver|' autogen.sh
sed -i 's|^[[:space:]]make install |# make install|' autogen.sh
sed -i 's|^[[:space:]]export PKG_CONFIG_PATH=mongo-c-driver/src/:mongo-c-driver/src/libbson/src|#export PKG_CONFIG_PATH=mongo-c-driver/src/:mongo-c-driver/src/libbson/src|' autogen.sh

# set rpath of edb-mongoc driver libs
# RHEL 7: Use edb-mongoc driver for building, so disable mongo-c-driver compilation
# RHEL 8 and Fedora: Use OS supplied mongo-c-driver
%if 0%{?rhel} && 0%{?rhel} == 7
sed -i '/SHLIB_LINK = /c SHLIB_LINK = $(shell pkg-config --libs libmongoc-1.0) -Wl,-rpath='/usr/pgdg-libmongoc/lib64',--enable-new-dtags' Makefile.meta
%else
sed -i '/SHLIB_LINK = /c SHLIB_LINK = $(shell pkg-config --libs libmongoc-1.0) -Wl,-rpath='/usr/lib64',--enable-new-dtags' Makefile.meta
%endif

%build
%ifarch ppc64 ppc64le
%if 0%{?rhel} && 0%{?rhel} == 7
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -fPIC -I%{atpath}/include"; export CFLAGS
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"; export CXXFLAGS
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
%else
	CFLAGS="$RPM_OPT_FLAGS -fPIC"; export CFLAGS
%endif

sh autogen.sh --with-master

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
sed -i "s:^\(PG_CPPFLAGS.*\):\1 -I/usr/include/libmongoc-1.0 -I/usr/include/libbson-1.0 -I/usr/include/json-c -fPIC:g" Makefile.meta
sed -i "s:\(^#include \"bson.h\"\):#include <bson.h>:g" mongo_fdw.c
sed -i "s:\(^#include \"bson.h\"\):#include <bson.h>:g" mongo_fdw.h
sed -i "s:\(^#include \"bson.h\"\)://\1:g" mongo_wrapper.h
%endif
%endif

PATH=%{pginstdir}/bin:$PATH %{__make} -f Makefile.meta USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

PATH=%{pginstdir}/bin:$PATH %{__make} -f Makefile.meta USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__install} -m 755 README.md %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{_docdir}/pgsql/extension/README.md

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/README-%{sname}.md
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}/json-c/*.bc
%endif

%changelog
* Tue Sep 14 2021 Devrim Gündüz <devrim@gunduz.org> - 5.2.9-1
- Update to 5.2.9
- Add llvmjit subpackage
- Use OS supplied mongo-c-driver on RHEL8+ and Fedora.

* Mon May 3 2021 Devrim Gündüz <devrim@gunduz.org> - 5.2.8-1
- Update to 5.2.8
- Add missing BR and Requires, per Martin Marques.
- Use custom mongo-c-driver package on RHEL 7, per:
  https://redmine.postgresql.org/issues/6424
- Get rid of pg_config patches, export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 5.2.7-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Mon Aug 3 2020 Devrim Gündüz <devrim@gunduz.org> - 5.2.7-1
- Update to 5.2.7

* Fri Sep 27 2019 Devrim Gündüz <devrim@gunduz.org> - 5.2.6-1
- Update to 5.2.6

* Wed May 1 2019 Devrim Gündüz <devrim@gunduz.org> - 5.2.3-1
- Update to 5.2.3

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 5.2.1-1.1
- Rebuild against PostgreSQL 11.0

* Wed Mar 21 2018 - Devrim Gündüz <devrim@gunduz.org> 5.2.1-1
- Update to 5.2.1

* Wed Mar 14 2018 - Devrim Gündüz <devrim@gunduz.org> 5.2.0-1
- Update to 5.2.0

* Tue Jun 6 2017 - Devrim Gündüz <devrim@gunduz.org> 5.0.0-1
- Update to 5.2.0

* Sun Sep 7 2014 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
