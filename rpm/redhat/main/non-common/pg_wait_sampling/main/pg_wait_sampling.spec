%global sname	pg_wait_sampling

Summary:	Sampling based statistics of wait events

Name:		%{sname}_%{pgmajorversion}
Version:	1.1.4
Release:	2%{?dist}
License:	PostgreSQL
Source0:	https://github.com/postgrespro/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/postgrespro/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-libs

%description
PostgreSQL 9.6+ provides an information about current wait event of particular
process. However, in order to gather descriptive statistics of server
behavior user have to sample current wait event multiple times.

pg_wait_sampling is an extension for collecting sampling statistics of wait
events.

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

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
  %endif
 %endif
%endif

%changelog
* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.1.4-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Fri Sep 30 2022 Devrim Gündüz <devrim@gunduz.org> - 1.1.4-1
- Update to 1.1.4

* Wed Jan 27 2021 Devrim Gündüz <devrim@gunduz.org> - 1.1.3-1
- Update to 1.1.3
- export PATH for pg_config, to get rid of patches.
- Fix license

* Wed Nov 11 2020 Devrim Gündüz <devrim@gunduz.org> - 1.1.2-1
- Update to 1.1.2

* Sat Apr 4 2020 Devrim Gündüz <devrim@gunduz.org> - 1.1.1-1
- Initial packaging for PostgreSQL RPM Repository
