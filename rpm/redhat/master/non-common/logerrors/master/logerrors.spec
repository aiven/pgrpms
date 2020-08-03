%global sname logerrors

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	Extension for PostgreSQL for collecting statistics about messages in logfile
Name:		%{sname}_%{pgmajorversion}
Version:	1.1
Release:	1%{?dist}
License:	PostgreSQL
Source0:	https://github.com/munakoiso/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/munakoiso/%{sname}
BuildRequires:	postgresql%{pgmajorversion} postgresql%{pgmajorversion}-devel
BuildRequires:	pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
Extension for PostgreSQL for collecting statistics about messages in logfile

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%{__make} %{?_smp_mflags}

%install
%make_install
# Let's also install documentation:
%{__mkdir} -p %{buildroot}%{pginstdir}/share/extension
%{__cp} README.md %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md

%postun -p /sbin/ldconfig
%post -p /sbin/ldconfig

%files
#%license LICENSE
%doc %{pginstdir}/share/extension/README-%{sname}.md
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
* Mon Aug 3 2020 - Devrim Gündüz <devrim@gunduz.org> 1.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
