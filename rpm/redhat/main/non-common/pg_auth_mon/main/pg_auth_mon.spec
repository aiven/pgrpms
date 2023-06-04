%global sname	pg_auth_mon

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	PostgreSQL extension to store authentication attempts
Name:		%{sname}_%{pgmajorversion}
Version:	2.0
Release:	1%{?dist}
License:	MIT
Source0:	https://github.com/RafiaSabih/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/RafiaSabih/%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-libs

%description
The goal of this extension is to ease monitoring of login attempts to your database.
Although each failed login is written to database log file, but it is not straightforward
to identify through that information alone if your database is under some malicious
intents. However, if the information like total failed as well as successful login
attempts, timestamp of last failed and successful login are maintained individually,
then we can easily answer questions like,
 * if the user genuinely mistyped their password or their username is being compromised?
 * if there is any particular time when the malicious user/application is active?

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_auth_mon
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
BuildRequires:  llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for pg_auth_mon
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Sun Jun 4 2023 Devrim Gunduz <devrim@gunduz.org> - 2.0.1
- Update to 2.0

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.0-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Feb 25 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Initial packaging for PostgreSQL RPM Repository
