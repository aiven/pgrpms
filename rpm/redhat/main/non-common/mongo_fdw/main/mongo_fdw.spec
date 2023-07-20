%global sname mongo_fdw
%global relver 5_5_1

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	PostgreSQL foreign data wrapper for MongoDB
Name:		%{sname}_%{pgmajorversion}
Version:	5.5.1
Release:	1PGDG%{?dist}
License:	LGPLv3
URL:		https://github.com/EnterpriseDB/%{sname}
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/REL-%{relver}.tar.gz
Source1:	%{sname}-config.h

BuildRequires:	postgresql%{pgmajorversion}-devel wget pgdg-srpm-macros

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
Requires:		libsnappy1 libbson-1_0-0 libmongoc-1_0-0
BuildRequires:		snappy-devel libbson-1_0-0-devel libmongoc-1_0-0-devel
BuildRequires:		libopenssl-devel
%endif
%else
# use pgdg-libmongoc and pgdg-libmongoc-devel packages for rhel7. pgdg-libmongoc* contains required version of libbson libs.
# so no need to install libbson-devel or libbson libs packages.
%if 0%{?rhel} == 7
Requires:	snappy
Requires:	pgdg-libmongoc-libs
BuildRequires:	pgdg-libmongoc-devel snappy-devel cmake3
BuildRequires:	openssl-devel cyrus-sasl-devel krb5-devel
%else
Requires:	snappy
Requires:	mongo-c-driver-libs libbson
BuildRequires:	mongo-c-driver-devel snappy-devel
BuildRequires:	openssl-devel cyrus-sasl-devel krb5-devel
BuildRequires:	libbson-devel
%endif
%endif

Requires:	postgresql%{pgmajorversion}-server cyrus-sasl-lib

Obsoletes:	%{sname}%{pgmajorversion} < 5.2.7-2

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
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for mongo_fdw
%endif

%prep
%setup -q -n %{sname}-REL-%{relver}

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
CFLAGS="$RPM_OPT_FLAGS -fPIC"; export CFLAGS

sh autogen.sh --with-master

%if 0%{?rhel} && 0%{?rhel} == 7
export PKG_CONFIG_PATH=/usr/pgdg-libmongoc/lib64/pkgconfig
sed -i "s:^\(PG_CPPFLAGS.*\):\1 -I/usr/pgdg-libmongoc/include/libmongoc-1.0 -I/usr/pgdg-libmongoc/include/libbson-1.0 -I/usr/include/json-c -fPIC:g" Makefile.meta
%endif

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
* Thu Jul 20 2023 Devrim Gündüz <devrim@gunduz.org> - 5.5.1-1PGDG
- Update to 5.5.1
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 5.5.0-1.1
- Rebuild against LLVM 15 on SLES 15

* Thu Dec 22 2022 Devrim Gündüz <devrim@gunduz.org> - 5.5.0-1
- Update to 5.5.0

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 5.4.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon May 30 2022 Devrim Gündüz <devrim@gunduz.org> - 5.4.0-1
- Update to 5.4.0

* Mon Feb 28 2022 Devrim Gündüz <devrim@gunduz.org> - 5.3.0-2
- Fix mongo_fdw installation on RHEL 7, per report and patch
  from Varsha Mehtre.

* Tue Jan 18 2022 Devrim Gündüz <devrim@gunduz.org> - 5.3.0-1
- Update to 5.3.0

* Tue Sep 21 2021 Devrim Gündüz <devrim@gunduz.org> - 5.2.10-2
- Remove patch0, no more needed.

* Thu Sep 16 2021 Devrim Gündüz <devrim@gunduz.org> - 5.2.10-1
- Update to 5.2.10

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
