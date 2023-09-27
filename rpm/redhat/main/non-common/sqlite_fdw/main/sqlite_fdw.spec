%global sname	sqlite_fdw

# Disable tests by default.
%{!?runselftest:%global runselftest 0}

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	SQLite Foreign Data Wrapper for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	2.4.0
Release:	1PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/pgspider/%{sname}
Source0:	https://github.com/pgspider/%{sname}/archive/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
BuildRequires:	postgresql%{pgmajorversion}-server sqlite-devel
Requires:	postgresql%{pgmajorversion}-server
%if 0%{?fedora} >= 27
Requires:	sqlite-libs
%endif
%if 0%{?rhel} <= 7
Requires:	sqlite
%endif

%description
This PostgreSQL extension is a Foreign Data Wrapper for SQLite.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for sqlite_fdw
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
This packages provides JIT support for sqlite_fdw
%endif

%prep
%setup -q -n %{sname}-%{version}

%build

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(-,root,root,-)
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.sql
%{pginstdir}/share/extension/*.control
%{pginstdir}/doc/extension/README-%{sname}.md

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Wed Sep 27 2023 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-1PGDG
- Update to 2.4.0
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 2.3.0-1.1
- Rebuild against LLVM 15 on SLES 15

* Fri Jan 20 2023 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-1
- Update to 2.3.0

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.2.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Sep 27 2022 Devrim Gündüz <devrim@gunduz.org> - 2.2.0-1
- Update to 2.2.0

* Wed Dec 22 2021 Devrim Gündüz <devrim@gunduz.org> - 2.1.1-1
- Update to 2.1.1

* Fri Sep 24 2021 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1
- Update to 2.1.0

* Wed May 26 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-1
- Update to 2.0.0

* Thu Jan 21 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-1
- Update to 1.3.1

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Oct 1 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1
- Update to 1.3.0

* Fri Aug 28 2020 Devrim Gündüz <devrim@gunduz.org> - 1.2.1-1
- Update to 1.2.1

* Tue Oct 1 2019 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1
- Update to 1.2.0

* Wed Oct 31 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1
- Update to 1.1.0

* Tue Oct 23 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1
- Initial packaging for PostgreSQL RPM repositories
