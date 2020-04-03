%global sname topn

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	PostgreSQL extension that returns the top values in a database
Name:		%{sname}_%{pgmajorversion}
Version:	2.3.0
Release:	1%{dist}
License:	AGPLv3
Source0:	https://github.com/citusdata/postgresql-%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/citusdata/postgresql-%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel libxml2-devel
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
TopN is an open source PostgreSQL extension that returns the top values
in a database according to some criteria. TopN takes elements in a data
set, ranks them according to a given rule, and picks the top elements in
that data set. When doing this, TopN applies an approximation algorithm
to provide fast results using few compute and memory resources.

The TopN extension becomes useful when you want to materialize top
values, incrementally update these top values, and/or merge top values
from different time intervals. If you're familiar with the PostgreSQL
HLL extension, you can think of TopN as its cousin.

%prep
%setup -q -n postgresql-%{sname}-%{version}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif

%{__make} %{?_smp_mflags}

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
  %endif
 %endif
%endif

%changelog
* Wed Nov 6 2019 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-1
- Update to 2.3.0

* Fri Sep 6 2019 Devrim Gündüz <devrim@gunduz.org> - 2.2.2-1
- Update to 2.2.2

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Thu Aug 23 2018 - Devrim Gündüz <devrim@gunduz.org> 2.1.0-1
- Update to 2.1.0

* Sat Aug 11 2018 - Devrim Gündüz <devrim@gunduz.org> 2.0.2-2
- Ignore .bc files on PPC arch.

* Thu Mar 29 2018 - Devrim Gündüz <devrim@gunduz.org> 2.0.2-1
- Update to 2.0.2

* Tue Mar 27 2018 - Devrim Gündüz <devrim@gunduz.org> 2.0.1-1
- Initial RPM packaging for PostgreSQL RPM Repository.
