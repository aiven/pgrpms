%global sname pg_filedump
%global sversion REL_13_1

Summary:	PostgreSQL File Dump Utility
Name:		%{sname}_%{pgmajorversion}
Version:	13.1
Release:	3%{?dist}
URL:		https://github.com/df7cb/%{sname}
License:	GPLv2+
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Source0:	https://github.com/df7cb/pg_filedump/archive/%{sversion}.tar.gz

%description
Display formatted contents of a PostgreSQL heap/index/control file.

%prep
%setup -q -n %{sname}-%{sversion}

%build
export CFLAGS="$RPM_OPT_FLAGS"

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__mkdir} -p %{buildroot}%{pginstdir}/bin
%{__install} -m 755 pg_filedump %{buildroot}%{pginstdir}/bin

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%{pginstdir}/bin/pg_filedump
%doc README.pg_filedump

%changelog
* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 13.1-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Jun 7 2021 Devrim Gündüz <devrim@gunduz.org> 13.1-2
- Remove pgxs patch, and export PATH instead.

* Mon Jan 4 2021 Devrim Gündüz <devrim@gunduz.org> - 13.1-1
- Update to 13.1

* Wed Oct 28 2020 Devrim Gündüz <devrim@gunduz.org> - 13.0-1
- Initial packaging for PostgreSQL RPM Repository
