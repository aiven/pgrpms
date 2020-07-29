%global sname	timescaledb

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	PostgreSQL based time-series database
Name:		%{sname}_%{pgmajorversion}
Version:	1.7.2
Release:	1%{?dist}
License:	Apache
Source0:	https://github.com/timescale/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-pgconfig.patch
Patch1:		%{sname}-cmake3-rhel7.patch
URL:		https://github.com/timescale/timescaledb
BuildRequires:	postgresql%{pgmajorversion}-devel
%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:	cmake3
%else
BuildRequires:	cmake >= 3.4
%endif

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
TimescaleDB is an open-source database designed to make SQL scalable for
time-series data. It is engineered up from PostgreSQL, providing automatic
partitioning across time and space (partitioning key), as well as full SQL
support.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0
%patch1 -p0

# Build only the portions that have Apache Licence, and disable telemetry:
./bootstrap -DAPACHE_ONLY=1 -DSEND_TELEMETRY_DEFAULT=NO \
	-DPROJECT_INSTALL_METHOD=pgdg -DREGRESS_CHECKS=OFF

%build
%ifarch ppc64 ppc64le
	CFLAGS="-O3 -mcpu=$PPC_MCPU -mtune=$PPC_MTUNE"
	CC=%{atpath}/bin/gcc; export CC
%else
	CFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
	CXXFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
	export CFLAGS
	export CXXFLAGS
%endif

cd build; %{__make}

%install
cd build; %{__make} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc README.md LICENSE-APACHE
%else
%doc README.md
%license LICENSE-APACHE
%endif
%{pginstdir}/lib/%{sname}*.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
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
