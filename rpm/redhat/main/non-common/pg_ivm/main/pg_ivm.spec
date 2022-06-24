%global debug_package %{nil}
%global sname	pg_ivm

Summary:	Incremental View Maintenance (IVM) feature for PostgreSQL.
Name:		%{sname}_%{pgmajorversion}
Version:	1.1
Release:	1%{?dist}
License:	PostgreSQL
URL:		https://github.com/sraoss/%{sname}/
Source0:	https://github.com/sraoss/%{sname}/archive/refs/tags/v%{version}.tar.gz

%description
Incremental View Maintenance (IVM) is a way to make materialized views
up-to-date in which only incremental changes are computed and applied on
views rather than recomputing the contents from scratch as REFRESH
MATERIALIZED VIEW does. IVM can update materialized views more efficiently
than recomputation when only small parts of the view are changed.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} INSTALL_PREFIX=%{buildroot} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%ifarch ppc64 ppc64le
 %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Fri Jun 24 2022 Devrim Gündüz <devrim@gunduz.org> - 1.1-1
- Update to 1.1

* Wed May 11 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Update to 1.0

* Fri May 6 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0-alpha-1
- Initial RPM packaging for the PostgreSQL RPM Repository.
