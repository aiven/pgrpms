%global sname pg_comparator

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	Efficient table content comparison and synchronization for PostgreSQL and MySQL
Name:		%{sname}_%{pgmajorversion}
Version:	2.2.5
Release:	6PGDG%{?dist}
License:	BSD
Source0:	https://github.com/koordinates/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/koordinates/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server
Requires:	perl(Getopt::Long) perl(Time::HiRes) perl-Pod-Usage

Obsoletes:	%{sname}%{pgmajorversion} < 2.2.5-3

%description
pg_comparator is a tool to compare possibly very big tables in
different locations and report differences, with a network and
time-efficient approach.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_comparator
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
This packages provides JIT support for pg_comparator
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
%{__install} -d %{buildroot}%{pginstdir}/share/contrib/

%post
# Create alternatives entries for binaries
%{_sbindir}/update-alternatives --install /usr/bin/%{sname} pgcomparator %{pginstdir}/bin/%{sname} %{pgmajorversion}0

%preun
# Drop alternatives entries for common binaries and man files
%{_sbindir}/update-alternatives --remove pgcomparator %{pginstdir}/bin/%{sname}

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/contrib/README.%{sname}
%doc %{pginstdir}/doc/contrib/README.pgc_casts
%doc %{pginstdir}/doc/contrib/README.pgc_checksum
%doc %{pginstdir}/doc/contrib/README.xor_aggregate
%license LICENSE
%{pginstdir}/bin/%{sname}
%{pginstdir}/lib/pgc_casts.so
%{pginstdir}/lib/pgc_checksum.so
%{pginstdir}/share/contrib/*.sql
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/pgc_casts.index.bc
   %{pginstdir}/lib/bitcode/pgc_checksum.index.bc
   %{pginstdir}/lib/bitcode/pgc_casts/*.bc
   %{pginstdir}/lib/bitcode/pgc_checksum/*.bc
%endif

%changelog
* Fri Sep 8 2023 Devrim Gunduz <devrim@gunduz.org> - 2.2.5-6PGDG
- Cleanup rpmlint warnings
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 2.2.5-5.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.2.5-5
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Sat Jun 5 2021 Devrim Gündüz <devrim@gunduz.org> 2.2.5-4
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 2.2.5-3
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Wed Aug 22 2018 - Devrim Gündüz <devrim@gunduz.org> 2.2.5-2
- Add v11 support to spec file.

* Sun Jan 24 2016 - Devrim Gündüz <devrim@gunduz.org> 2.2.5-1
- Update to 2.2.5
- Unified spec file for all distros
- Use more macros
- Don't strip .so file
- Whitespace cleanup

* Thu Feb 13 2014 - Devrim Gündüz <devrim@gunduz.org> 2.2.2-1
- Update to 2.2.2

* Sun Jun 30 2013 - Devrim Gündüz <devrim@gunduz.org> 2.2.1-1
- Update to 2.2.1

* Wed Nov 14 2012 - Devrim Gündüz <devrim@gunduz.org> 2.1.2-1
- Update to 2.1.2

* Fri Sep 14 2012 - Devrim Gündüz <devrim@gunduz.org> 2.1.1-1
- Update to 2.1.1
- Use a better URL for tarball

* Fri Oct 8 2010 - Devrim Gündüz <devrim@gunduz.org> 1.6.2-1
- Refactor spec for 9.0 compatibility.

* Tue Apr 20 2010 - Devrim Gündüz <devrim@gunduz.org> 1.6.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
