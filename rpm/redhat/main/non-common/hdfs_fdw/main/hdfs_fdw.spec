%global sname hdfs_fdw

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL Foreign Data Wrapper (FDW) for the hdfs
Name:		%{sname}_%{pgmajorversion}
Version:	2.3.2
Release:	2PGDG%{?dist}
License:	BSD
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/EnterpriseDB/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
BuildRequires:	libxml2-devel java-devel

Requires:	postgresql%{pgmajorversion}-server

%description
This PostgreSQL extension implements a Foreign Data Wrapper (FDW) for
the hdfs.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for firebird_fdw
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 13.0 clang-devel >= 13.0
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for firebird_fdw
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
export JDK_INCLUDE="/etc/alternatives/java_sdk_openjdk/include"
export JRE_LIBDIR="/usr/lib/jvm/jre-1.8.0-openjdk/lib/amd64/server"
export JVM_LIB="/usr/lib/jvm/jre-1.8.0-openjdk/lib/amd64/server"
#export JVM_LIB="/etc/alternatives/jre_1.8.0_exports/lib/amd64/server"
pushd libhive
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}
popd

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

pushd libhive
%{__mkdir} -p %{buildroot}%{pginstdir}/lib
%{__make} %{?_smp_mflags} install INSTALL_DIR=%{buildroot}/%{pginstdir}/lib
popd

pushd libhive/jdbc
	%javac MsgBuf.java
	%javac HiveJdbcClient.java
	%jar cf HiveJdbcClient-1.0.jar *.class
	%{__cp} HiveJdbcClient-1.0.jar %{buildroot}%{pginstdir}/lib
popd

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install INSTALL_DIR=%{buildroot} DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__install} -m 755 README.md %{buildroot}%{pginstdir}/share/extension/README-%{sname}
%{__rm} -f %{buildroot}%{_docdir}/pgsql/extension/README.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(755,root,root,755)
%doc %{pginstdir}/share/extension/README-%{sname}
%{pginstdir}/lib/libhive.so
%{pginstdir}/lib/HiveJdbcClient-1.0.jar
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control
%if %llvm
  %{pginstdir}/lib/bitcode/%{sname}*.bc
  %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.3.2-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Fri Jul 12 2024 Devrim Gunduz <devrim@gunduz.org> - 2.3.2-1PGDG
- Update to 2.3.2 per changes described at:
  https://github.com/EnterpriseDB/hdfs_fdw/releases/tag/v2.3.2
- Remove RHEL 7 support

- Add PGDG branding
* Thu Jul 20 2023 Devrim Gunduz <devrim@gunduz.org> - 2.3.1-1PGDG
- Update to 2.3.1
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 2.3.0-1.1
- Rebuild against LLVM 15 on SLES 15

* Thu Dec 22 2022 - Devrim Gündüz <devrim@gunduz.org> - 2.3.0-1
- Update to 2.3.0

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.2.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon May 30 2022 - Devrim Gündüz <devrim@gunduz.org> - 2.2.0-1
- Update to 2.2.0

* Tue Jan 18 2022 - Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1
- Update to 2.1.0

* Tue Sep 21 2021 - Devrim Gündüz <devrim@gunduz.org> - 2.0.9-2
- Fix spec file for RHEL 8 / ppc64le.

* Thu Sep 16 2021 - Devrim Gündüz <devrim@gunduz.org> - 2.0.9-1
- Update to 2.0.9

* Tue Jun 15 2021 - Devrim Gündüz <devrim@gunduz.org> - 2.0.8-1
- Update to 2.0.8

* Thu Jun 3 2021 - Devrim Gündüz <devrim@gunduz.org> 2.0.7-2
- Remove pgxs patches, and export PATH instead.

* Wed Oct 21 2020 - Devrim Gündüz <devrim@gunduz.org> 2.0.7-1
- Update to 2.0.7

* Mon Aug 3 2020 - Devrim Gündüz <devrim@gunduz.org> 2.0.6-1
- Update to 2.0.6

* Tue Oct 1 2019 - Devrim Gündüz <devrim@gunduz.org> 2.0.5-1
- Update to 2.0.5

* Thu Dec 6 2018 - Devrim Gündüz <devrim@gunduz.org> 2.0.4-1
- Update to 2.0.4

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.0.3-1.1
- Rebuild against PostgreSQL 11.0

* Wed Jan 3 2018 - Devrim Gündüz <devrim@gunduz.org> 2.0.3-1
- Update to 2.0.3

* Thu Jun 22 2017 - Devrim Gündüz <devrim@gunduz.org> 2.0.1-1
- Update to 2.0.1

* Tue Jan 17 2017 - Devrim Gündüz <devrim@gunduz.org> 2.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
