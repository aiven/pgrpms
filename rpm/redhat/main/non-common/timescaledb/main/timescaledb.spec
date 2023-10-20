%global debug_package %{nil}
%global sname	timescaledb

Summary:	PostgreSQL based time-series database
Name:		%{sname}_%{pgmajorversion}
Version:	2.12.2
Release:	1PGDG%{?dist}
License:	Apache
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

%description
TimescaleDB is an open-source database designed to make SQL scalable for
time-series data. It is engineered up from PostgreSQL, providing automatic
partitioning across time and space (partitioning key), as well as full SQL
support.

%prep
%setup -q -n %{sname}-%{version}
%if 0%{?rhel} && 0%{?rhel} == 7
%patch -P 1 -p0
%endif

# Build only the portions that have Apache Licence, and disable telemetry:
export PATH=%{pginstdir}/bin:$PATH
./bootstrap -DAPACHE_ONLY=1 -DSEND_TELEMETRY_DEFAULT=NO \
	-DPROJECT_INSTALL_METHOD=pgdg -DREGRESS_CHECKS=OFF

%build
export PATH=%{pginstdir}/bin:$PATH
%ifarch ppc64 ppc64le
%if 0%{?rhel} && 0%{?rhel} == 7
	CFLAGS="-O3 -mcpu=$PPC_MCPU -mtune=$PPC_MTUNE"
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
%{__rm} -f %{buildroot}/%{pginstdir}/lib/pgxs/src/test/perl/*pm

%files
%defattr(-, root, root)
%doc README.md
%license LICENSE-APACHE
%{pginstdir}/lib/%{sname}*.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

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
- Remove RHEL 6 bits

* Thu Jul 6 2023 Devrim Gündüz <devrim@gunduz.org> - 2.11.1-1PGDG
- Update to 2.11.1, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.11.1
- Add PGDG branding

* Tue May 30 2023 Devrim Gündüz <devrim@gunduz.org> - 2.11.0-1
- Update to 2.11.0, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.11.0

* Mon May 8 2023 Devrim Gündüz <devrim@gunduz.org> - 2.10.3-1
- Update to 2.10.3, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.10.3

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 2.10.2-1.1
- Modernise %patch usage, which has been deprecated in Fedora 38

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

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.8.1-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

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

* Mon Apr 18 2022 Devrim Gündüz <devrim@gunduz.org> - 2.6.1-1
- Update to 2.6.1

* Fri Feb 25 2022 Devrim Gündüz <devrim@gunduz.org> - 2.6.0-1
- Update to 2.6.0

* Mon Feb 14 2022 Devrim Gündüz <devrim@gunduz.org> - 2.5.2-1
- Update to 2.5.2

* Mon Nov 1 2021 Devrim Gündüz <devrim@gunduz.org> - 2.5.1-1
- Update to 2.5.1

* Mon Nov 1 2021 Devrim Gündüz <devrim@gunduz.org> - 2.5.0-1
- Update to 2.5.0
- Remove patch0, and export PATH instead.

* Wed Sep 22 2021 Devrim Gündüz <devrim@gunduz.org> - 2.4.2-1
- Update to 2.4.2

* Thu Aug 26 2021 Devrim Gündüz <devrim@gunduz.org> - 2.4.1-1
- Update to 2.4.1

* Wed May 26 2021 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-1
- Update to 2.3.0

* Thu Apr 15 2021 Devrim Gündüz <devrim@gunduz.org> - 2.2.0-1
- Update to 2.2.0

* Wed Apr 7 2021 Devrim Gündüz <devrim@gunduz.org> - 2.1.1-2
- Add missing BR

* Thu Apr 1 2021 Devrim Gündüz <devrim@gunduz.org> - 2.1.1-1
- Update to 2.1.1

* Mon Mar 1 2021 John Harvey <john.harvey@crunchydata.com> - 2.1.0-1
- Update to 2.1.0

* Mon Feb 15 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-1
- Update to 2.0.1
- Use patch1 only on RHEL 7, otherwise it breaks SLES-15 builds.

* Tue Dec 22 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-1
- Update to 2.0.0

* Wed Sep 23 2020 Devrim Gündüz <devrim@gunduz.org> - 1.7.4-1
- Update to 1.7.4

* Wed Jul 29 2020 Devrim Gündüz <devrim@gunduz.org> - 1.7.2-1
- Update to 1.7.2

* Mon Apr 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.7.0-1
- Update to 1.7.0

* Thu Apr 2 2020 Devrim Gündüz <devrim@gunduz.org> - 1.6.1-1
- Update to 1.6.1

* Sat Jan 18 2020 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-1
- Update to 1.6.0

* Sun Nov 24 2019 Devrim Gündüz <devrim@gunduz.org> - 1.5.1-1
- Update to 1.5.1

* Thu Jul 25 2019 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-1
- Update to 1.4.0

* Thu Jun 27 2019 Devrim Gündüz <devrim@gunduz.org> - 1.3.2-1
- Update to 1.3.2
- Add -DPROJECT_INSTALL_METHOD=pgdg to help upstream get better
  data when users enable telemetry.

* Tue Jun 11 2019 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-1
- Update to 1.3.1
- Disable telemetry by default.
- Remove my patch that disabled telemetry.

* Tue Jun 4 2019 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-2
- Add a patch to disable telemetry by default.

* Mon May 6 2019 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1
- Update to 1.3.0
- Build only the portions that have Apache Licence.

* Tue Feb 5 2019 Devrim Gündüz <devrim@gunduz.org> - 1.1.1-2
- Add dependency to PostgreSQL server package.

* Fri Dec 21 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1.1-1
- Update to 1.1.1

* Thu Dec 6 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0.1-1
- Update to 1.0.1

* Mon Nov 5 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1
- Update to 1.0.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.12.1-1.1
- Rebuild against PostgreSQL 11.0

* Thu Sep 20 2018 Devrim Gündüz <devrim@gunduz.org> 0.12.1-1
- Update to 0.12.1, per #3662

* Wed Aug 15 2018 Devrim Gündüz <devrim@gunduz.org> 0.11.0-1
- Update to 0.11.0, per #3555.

* Sat Aug 11 2018 Devrim Gündüz <devrim@gunduz.org> 0.10.1-2
- Ignore .bc files on PPC arch.

* Fri Jul 13 2018 Devrim Gündüz <devrim@gunduz.org> 0.10.1-1
- Update to 0.10.1, per #3497.

* Mon May 14 2018 Devrim Gündüz <devrim@gunduz.org> 0.9.2-1
- Update to 0.9.2, per #3345

* Tue Mar 27 2018 Devrim Gündüz <devrim@gunduz.org> 0.9.1-1
- Update to 0.9.1, per #3231

* Wed Mar 7 2018 Devrim Gündüz <devrim@gunduz.org> 0.9.0-1
- Update to 0.9.0, per #3178

* Mon Feb 12 2018 Devrim Gündüz <devrim@gunduz.org> 0.8.0-2
- Rebuild against PostgreSQL 10.2, per
  https://github.com/timescale/timescaledb/issues/422

* Tue Feb 6 2018 Devrim Gündüz <devrim@gunduz.org> 0.8.0-1
- Initial packaging for PostgreSQL RPM Repository
