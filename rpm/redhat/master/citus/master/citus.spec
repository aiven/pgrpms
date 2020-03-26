%global sname citus

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	PostgreSQL-based distributed RDBMS
Name:		%{sname}_%{pgmajorversion}
Version:	9.2.3
Release:	1%{dist}
License:	AGPLv3
URL:		https://github.com/citusdata/%{sname}
Source0:	https://github.com/citusdata/%{sname}/archive/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel libxml2-devel
BuildRequires:	libxslt-devel openssl-devel pam-devel readline-devel
BuildRequires:	libcurl-devel
Requires:	postgresql%{pgmajorversion}-server
Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
Citus horizontally scales PostgreSQL across commodity servers
using sharding and replication. Its query engine parallelizes
incoming SQL queries across these servers to enable real-time
responses on large datasets.

Citus extends the underlying database rather than forking it,
which gives developers and enterprises the power and familiarity
of a traditional relational database. As an extension, Citus
supports new PostgreSQL releases, allowing users to benefit from
new features while maintaining compatibility with existing
PostgreSQL tools. Note that Citus supports many (but not all) SQL
commands.

%package devel
Summary:	Citus development header files and libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package includes development libraries for Citus.

%prep
%setup -q -n %{sname}-%{version}

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif

%configure PG_CONFIG=%{pginstdir}/bin/pg_config
make %{?_smp_mflags}

%install
%make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*/*.bc
  %endif
 %endif
%endif

%files devel
%defattr(-,root,root,-)
%{pginstdir}/include/server/citus_version.h
%{pginstdir}/include/server/distributed/*.h

%changelog
* Thu Mar 26 2020 Devrim Gündüz <devrim@gunduz.org> 9.2.3-1
- Update to 9.2.3

* Tue Mar 10 2020 Devrim Gündüz <devrim@gunduz.org> 9.2.2-1
- Update to 9.2.2

* Mon Feb 17 2020 Devrim Gündüz <devrim@gunduz.org> 9.2.1-1
- Update to 9.2.1

* Tue Feb 11 2020 Devrim Gündüz <devrim@gunduz.org> 9.2.0-1
- Update to 9.2.0

* Wed Jan 1 2020 Devrim Gündüz <devrim@gunduz.org> 9.1.2-1
- Update to 9.1.2

* Mon Dec 9 2019 Devrim Gündüz <devrim@gunduz.org> 9.1.0-1
- Update to 9.1.0

* Sun Nov 3 2019 Devrim Gündüz <devrim@gunduz.org> 9.0.1-1
- Update to 9.0.1

* Wed Oct 16 2019 Devrim Gündüz <devrim@gunduz.org> 9.0.0-1
- Update to 9.0.0

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Sun Aug 11 2019 Devrim Gündüz <devrim@gunduz.org> 8.3.2-1
- Update to 8.3.2

* Mon Aug 5 2019 Devrim Gündüz <devrim@gunduz.org> 8.3.1-1
- Update to 8.3.1

* Fri Jul 12 2019 Devrim Gündüz <devrim@gunduz.org> 8.3.0-1
- Update to 8.3.0

* Thu Jun 13 2019 Devrim Gündüz <devrim@gunduz.org> 8.2.2-1
- Update to 8.2.2

* Thu Apr 11 2019 Devrim Gündüz <devrim@gunduz.org> 8.2.1-1
- Update to 8.2.1

* Mon Apr 1 2019 Devrim Gündüz <devrim@gunduz.org> 8.2.0-1
- Update to 8.2.0

* Wed Feb 13 2019 Devrim Gündüz <devrim@gunduz.org> 8.1.1-2
- Rebuild against PostgreSQL 11.2

* Tue Jan 15 2019 Devrim Gündüz <devrim@gunduz.org> 8.1.1-1
- Update to 8.1.1

* Fri Dec 21 2018 Devrim Gündüz <devrim@gunduz.org> 8.0.1-1
- Update to 8.0.1

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Thu Aug 30 2018 -  Devrim Gündüz <devrim@gunduz.org> 7.5.1-1
- Update to 7.5.1, per #3597

* Thu Jul 26 2018 -  Devrim Gündüz <devrim@gunduz.org> 7.5.0-1
- Update to 7.5.0

* Fri Jun 29 2018 -  Devrim Gündüz <devrim@gunduz.org> 7.4.1-1
- Update to 7.4.1, per #3432

* Thu May 17 2018 -  Devrim Gündüz <devrim@gunduz.org> 7.4.0-1
- Update to 7.4.0, per #3351

* Fri Mar 16 2018 -  Devrim Gündüz <devrim@gunduz.org> 7.3.0-1
- Update to 7.3.0, per #3208

* Tue Feb 6 2018 -  Devrim Gündüz <devrim@gunduz.org> 7.2.1-1
- Update to 7.2.1, per #3088

* Thu Jan 18 2018 -  Devrim Gündüz <devrim@gunduz.org> 7.2.0-1
- Update to 7.2.0, per #3026

* Wed Jan 10 2018 -  Devrim Gündüz <devrim@gunduz.org> 7.1.2-1
- Update to 7.1.2, per #2994

* Sun Dec 10 2017 -  Devrim Gündüz <devrim@gunduz.org> 7.1.1-1
- Update to 7.1.1, per #2938

* Thu Nov 16 2017 -  Devrim Gündüz <devrim@gunduz.org> 7.1.0-1
- Update to 7.1.0

* Sat Oct 21 2017 -  Devrim Gündüz <devrim@gunduz.org> 7.0.3-1
- Update to 7.0.3, per #2817

* Tue Oct 3 2017 -  Devrim Gündüz <devrim@gunduz.org> 7.0.2-1
- Update to 7.0.2, per #2751

* Wed Sep 13 2017 -  Devrim Gündüz <devrim@gunduz.org> 7.0.1-1
- Update to 7.0.1, per #2697.

* Thu Aug 31 2017 -  Devrim Gündüz <devrim@gunduz.org> 7.0.0-1
- Update to 7.0.0

* Sat Jul 15 2017 -  Devrim Gündüz <devrim@gunduz.org> 6.2.3-1
- Update to 6.2.3

* Sun Jun 11 2017 -  Devrim Gündüz <devrim@gunduz.org> 6.2.2-1
- Update to 6.2.2

* Thu May 25 2017 -  Devrim Gündüz <devrim@gunduz.org> 6.2.1-1
- Update to 6.2.1

* Tue Apr 25 2017 -  Devrim Gündüz <devrim@gunduz.org> 6.1.0-1
- Update to 6.1.0

* Thu Dec 1 2016 - Devrim Gündüz <devrim@gunduz.org> 6.0.1-1
- Update to 6.0.1

* Wed Nov 9 2016 - Devrim Gündüz <devrim@gunduz.org> 6.0.0-1
- Update to 6.0.0
- Split development headers into separate subpackage.

* Wed Nov 9 2016 - Devrim Gündüz <devrim@gunduz.org> 5.2.2-1
- Update to 5.2.2

* Sat Sep 17 2016 - Devrim Gündüz <devrim@gunduz.org> 5.2.1-1
- Update to 5.2.1

* Fri Aug 26 2016 - Devrim Gündüz <devrim@gunduz.org> 5.2.0-1
- Update to 5.2.0. Fixes #1566.
- Update license and install docs. Fixes #1385.

* Thu Jul 7 2016 - Devrim Gündüz <devrim@gunduz.org> 5.1.1-1
- Update to 5.1.1

* Tue May 17 2016 - Jason Petersen <jason@citusdata.com> 5.1.0-1
- Update to Citus 5.1.0

* Fri Mar 25 2016 - Devrim Gündüz <devrim@gunduz.org> 5.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository,
  based on the spec file of Jason Petersen @ Citus.
