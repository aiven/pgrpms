%global debug_package %{nil}
%global sname	timescaledb

Summary:	PostgreSQL based time-series database
Name:		%{sname}-tsl_%{pgmajorversion}
Version:	2.12.2
Release:	1PGDG%{?dist}
License:	Timescale
Source0:	https://github.com/timescale/%{sname}/archive/%{version}.tar.gz
%if 0%{?rhel} && 0%{?rhel} == 7
Patch1:		%{sname}-cmake3-rhel7.patch
%endif
URL:		https://github.com/timescale/timescaledb
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
BuildRequires:	openssl-devel
%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:	cmake3
%else
BuildRequires:	cmake >= 3.4
%endif

Requires:	postgresql%{pgmajorversion}-server

Conflicts:	%{sname}_%{pgmajorversion}

%description
TimescaleDB is an open-source database designed to make SQL scalable for
time-series data. It is engineered up from PostgreSQL, providing automatic
partitioning across time and space (partitioning key), as well as full SQL
support.

%package devel
Summary:	Development portions of timescaledb-tsl
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This packages includes development portions of timescaledb-tsl.

%prep
%setup -q -n %{sname}-%{version}
%if 0%{?rhel} && 0%{?rhel} == 7
%patch -P 1 -p0
%endif

# Disable telemetry, so that we can distribute it via PGDG repos:
export PATH=%{pginstdir}/bin:$PATH
./bootstrap -DSEND_TELEMETRY_DEFAULT=NO \
	-DREGRESS_CHECKS=OFF

%build
export PATH=%{pginstdir}/bin:$PATH
CFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
CXXFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
export CFLAGS
export CXXFLAGS

cd build; %{__make}

%install
export PATH=%{pginstdir}/bin:$PATH
cd build; %{__make} DESTDIR=%{buildroot} install

%files
%defattr(-, root, root)
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{sname}*.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%files devel
%{pginstdir}/lib/pgxs/src/test/perl/AccessNode.pm
%{pginstdir}/lib/pgxs/src/test/perl/DataNode.pm
%{pginstdir}/lib/pgxs/src/test/perl/TimescaleNode.pm

%changelog
* Fri Oct 20 2023 Devrim Gündüz <devrim@gunduz.org> - 2.12.2-1PGDG
- Update to 2.12.2, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.12.2

* Wed Oct 4 2023 Devrim Gündüz <devrim@gunduz.org> - 2.12.0-1PGDG
- Update to 2.12.0, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.12.0

* Mon Aug 21 2023 Devrim Gündüz <devrim@gunduz.org> - 2.11.2-1PGDG
- Update to 2.11.2, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.11.2

* Thu Jul 6 2023 Devrim Gündüz <devrim@gunduz.org> - 2.11.1-1PGDG
- Update to 2.11.1, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.11.1
- Add PGDG branding

* Tue May 30 2023 Devrim Gündüz <devrim@gunduz.org> - 2.11.0-1
- Update to 2.11.0, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.11.0
- Remove RHEL 7 AT specific portions.

* Mon May 8 2023 Devrim Gündüz <devrim@gunduz.org> - 2.10.3-1
- Update to 2.10.3, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.10.3

* Fri Apr 21 2023 Devrim Gündüz <devrim@gunduz.org> - 2.10.2-1
- Update to 2.10.2, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.10.2

* Mon Feb 27 2023 Devrim Gündüz <devrim@gunduz.org> - 2.10.0-1
- Update to 2.10.0, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.10.0

* Wed Feb 15 2023 Devrim Gündüz <devrim@gunduz.org> - 2.9.3-1
- Update to 2.9.3, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.9.3

* Mon Jan 30 2023 Devrim Gündüz <devrim@gunduz.org> - 2.9.2-1
- Update to 2.9.2, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.9.2

* Wed Jan 4 2023 Devrim Gündüz <devrim@gunduz.org> - 2.9.1-1
- Update to 2.9.1, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.9.1

* Mon Oct 10 2022 Devrim Gündüz <devrim@gunduz.org> - 2.8.1-1
- Update to 2.8.1, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.8.1

* Thu Sep 8 2022 Devrim Gündüz <devrim@gunduz.org> - 2.8.0-1
- Update to 2.8.0, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.8.0

* Wed Jul 27 2022 Devrim Gündüz <devrim@gunduz.org> - 2.7.2-1
- Update to 2.7.2, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.7.2

* Mon May 30 2022 Devrim Gündüz <devrim@gunduz.org> - 2.7.0-1
- Update to 2.7.0
- Add -devel subpackage

* Mon Apr 18 2022 Devrim Gündüz <devrim@gunduz.org> - 2.6.1-1
- Update to 2.6.1

* Fri Feb 25 2022 Devrim Gündüz <devrim@gunduz.org> - 2.6.0-1
- Update to 2.6.0

* Mon Feb 14 2022 Devrim Gündüz <devrim@gunduz.org> - 2.5.2-1
- Update to 2.5.2

* Thu Dec 16 2021 Devrim Gündüz <devrim@gunduz.org> - 2.5.1-1
- Update to 2.5.1

* Mon Nov 1 2021 Devrim Gündüz <devrim@gunduz.org> - 2.5.0-1
- Update to 2.5.0
- Remove patch0, and export PATH instead.

* Wed Sep 22 2021 Devrim Gündüz <devrim@gunduz.org> - 2.4.2-1
- Update to 2.4.2

* Thu Aug 26 2021 Devrim Gündüz <devrim@gunduz.org> - 2.4.1-1
- Update to 2.4.1

* Wed May 26 2021 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-1
- Initial packaging of TimescaleDB with Timescale license.
