%global debug_package %{nil}
%global sname	timescaledb

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	PostgreSQL based time-series database
Name:		%{sname}-tsl_%{pgmajorversion}
Version:	2.10.2
Release:	1%{?dist}
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

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

Requires:	postgresql%{pgmajorversion}-server

Conflicts:	%{sname}_%{pgmajorversion}

%description
TimescaleDB is an open-source database designed to make SQL scalable for
time-series data. It is engineered up from PostgreSQL, providing automatic
partitioning across time and space (partitioning key), as well as full SQL
support.

%if 0%{?fedora}
%package devel
Summary:	Development portions of timescaledb-tsl
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This packages includes development portions of timescaledb-tsl.
%endif

%prep
%setup -q -n %{sname}-%{version}
%if 0%{?rhel} && 0%{?rhel} == 7
%patch1 -p0
%endif

# Disable telemetry, so that we can distribute it via PGDG repos:
export PATH=%{pginstdir}/bin:$PATH
./bootstrap -DSEND_TELEMETRY_DEFAULT=NO \
	-DREGRESS_CHECKS=OFF

%build
export PATH=%{pginstdir}/bin:$PATH
%ifarch ppc64 ppc64le
%if 0%{?rhel} && 0%{?rhel} == 7
	CFLAGS="-O3 -mcpu=$PPC_MCPU -mtune=$PPC_MTUNE"
	CC=%{atpath}/bin/gcc; export CC
%endif
%else
	CFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
	CXXFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
	export CFLAGS
	export CXXFLAGS
%endif

cd build; %{__make}

%install
export PATH=%{pginstdir}/bin:$PATH
cd build; %{__make} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{sname}*.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if 0%{?fedora}
%files devel
%{pginstdir}/lib/pgxs/src/test/perl/AccessNode.pm
%{pginstdir}/lib/pgxs/src/test/perl/DataNode.pm
%{pginstdir}/lib/pgxs/src/test/perl/TimescaleNode.pm
%endif

%changelog
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
