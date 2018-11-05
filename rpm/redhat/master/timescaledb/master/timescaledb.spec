%global sname	timescaledb

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	PostgreSQL based time-series database
Name:		%{sname}_%{pgmajorversion}
Version:	1.0.0
Release:	1%{?dist}
License:	Apache
Source0:	https://github.com/timescale/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-pgconfig.patch
Patch1:		%{sname}-cmake3-rhel7.patch
URL:		https://github.com/timescale/timescaledb
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
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

%description
TimescaleDB is an open-source database designed to make SQL scalable for
time-series data. It is engineered up from PostgreSQL, providing automatic
partitioning across time and space (partitioning key), as well as full SQL
support.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0
%patch1 -p0
./bootstrap

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
