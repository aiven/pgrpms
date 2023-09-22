%global debug_package %{nil}
%global sname postgresql_faker

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	Fake Data Generator for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	0.5.3
Release:	4PGDG%{?dist}
License:	PostgreSQL
Source0:	https://gitlab.com/dalibo/%{sname}/-/archive/%{version}/%{sname}-%{version}.tar.bz2
URL:		https://gitlab.com/dalibo/%{sname}

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server
Requires:	postgresql%{pgmajorversion}-plpython3
%if 0%{?fedora} || 0%{?rhel} >= 7
Requires:	python3-faker
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1499
Requires:	python3-Faker
%endif
%endif

%description
postgresql_faker is a PostgreSQL extension based on the awesome Python Faker
Library. This is useful to generate random-but-meaningful datasets for
functional testing, anonymization, training data, etc...

This extension is simply a wrapper written in pl/python procedural language.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for postgresql_faker
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
This packages provides JIT support for postgresql_faker
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
# Just a workaround until next version is out.
# https://gitlab.com/dalibo/postgresql_faker/-/issues/13
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension/
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%license LICENSE.md
%defattr(644,root,root,755)
%{pginstdir}/lib/faker.so
%{pginstdir}/share/extension/faker/faker*.sql
%{pginstdir}/share/extension/faker.control
%doc %{pginstdir}/doc/extension/README-%{sname}.md

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/faker*.bc
    %{pginstdir}/lib/bitcode/faker/*.bc
%endif

%changelog
* Fri Sep 22 2023 Devrim Gündüz <devrim@gunduz.org> - 0.5.3-4PGDG
- Fix LLVM dependency on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 0.5.3-3PGDG
- Add PGDG branding
- Cleanup rpmlint warnings

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 0.5.3-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Mar 10 2022 Devrim Gündüz <devrim@gunduz.org> - 0.5.3-1
- Update to 0.5.3

* Wed Mar 9 2022 Devrim Gündüz <devrim@gunduz.org> - 0.5.2-1
- Update to 0.5.2

* Fri Mar 4 2022 Devrim Gündüz <devrim@gunduz.org> - 0.5.1-1
- Update to 0.5.1

* Wed May 19 2021 Devrim Gündüz <devrim@gunduz.org> - 0.4.0-1
- Update to 0.4.0

* Mon Apr 26 2021 Devrim Gündüz <devrim@gunduz.org> - 0.3.0-1
- Initial packaging for PostgreSQL RPM Repository
