%global sname pglogical
%global tag 2_3_1

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	Logical Replication extension for PostgreSQ
Name:		%{sname}_%{pgmajorversion}
Version:	2.3.1
Release:	1%{dist}
License:	PostgreSQL
URL:		https://github.com/2ndQuadrant/%{sname}
Source0:	https://github.com/2ndQuadrant/%{sname}/archive/REL%{tag}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
pglogical is a logical replication system implemented entirely as a PostgreSQL
extension. Fully integrated, it requires no triggers or external programs.
This alternative to physical replication is a highly efficient method of
replicating data using a publish/subscribe model for selective replication.

he pglogical 2 extension provides logical streaming replication for
PostgreSQL, using a publish/subscribe model.

%prep
%setup -q -n %{sname}-REL%{tag}

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif

PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
PATH=%{pginstdir}/bin:$PATH %make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYRIGHT
%else
%license COPYRIGHT
%endif
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/bin/%{sname}_create_subscriber
%{pginstdir}/lib/%{sname}_output.so
%{pginstdir}/share/extension/%{sname}_origin--1.0.0.sql
%{pginstdir}/share/extension/%{sname}_origin.control

%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}_output/*.bc
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/compat%{pgmajorversion}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc*
  %endif
 %endif
%endif

%changelog
* Sun May 3 2020 Devrim Gündüz <devrim@gunduz.org> 2.3.1-1
- Initial RPM packaging for PostgreSQL RPM Repository,
