%global sname postcode

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	UK postcode type optimised for indexing
Name:		%{sname}_%{pgmajorversion}
Version:	1.3.0
Release:	1%{?dist}.1
License:	BSD
Source0:	http://api.pgxn.org/dist/postcode/%{version}/postcode-%{version}.zip
Patch0:		%{sname}-1.3.0-c99.patch
Patch1:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://pgxn.org/dist/postcode/
BuildRequires:	postgresql%{pgmajorversion} postgresql%{pgmajorversion}-devel
BuildRequires:	pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
UK postcode encoded in 32 bits and optimised for indexing and partial matches.
Parses and encodes UK postcodes in 32 bits optimised for indexing and partial
matches. Also provides suitable type for delivery point suffixes.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0
%patch1 -p0

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

%{__make} %{?_smp_mflags}

%install
%make_install
# Let's also install documentation:
%{__mkdir} -p %{buildroot}%{pginstdir}/share/extension
%{__cp} README.md %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md
# Install sql/ directory:
%{__mkdir} -p %{buildroot}/%{_datadir}/%{name}/
%{__cp} -rp sql/ %{buildroot}/%{_datadir}/%{name}/

%postun -p /sbin/ldconfig
%post -p /sbin/ldconfig

%files
%license LICENSE
%doc %{pginstdir}/share/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control
%{_datadir}/%{name}

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1.1
- Rebuild against PostgreSQL 11.0

* Tue May 12 2015 - Devrim Gündüz <devrim@gunduz.org> 1.3.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
