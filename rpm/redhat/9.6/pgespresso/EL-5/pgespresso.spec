%global pgmajorversion 96
%global pginstdir /usr/pgsql-9.6
%global sname pgespresso

Summary:	Optional Extension for Barman
Name:		%{sname}%{pgmajorversion}
Version:	1.2
Release:	1%{?dist}
License:	PostgreSQL
Group:		Applications/Databases
Source0:	https://github.com/2ndquadrant-it/%{name}/archive/%{version}.tar.gz
Patch0:		Makefile-pgxs.patch
URL:		https://github.com/2ndquadrant-it/%{name}
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description

pgespresso is an extension that adds functions and views to be used by Barman,
the disaster recovery tool written by 2ndQuadrant and released as open source
(http://www.pgbarman.org/). Requires at least Barman 1.3.1 and PostgreSQL 9.2.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

make USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
install -d %{buildroot}%{pginstdir}/share/extension
install -m 755 README.asciidoc  %{buildroot}%{pginstdir}/share/extension/README-%{sname}.asciidoc

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/share/extension/README-%{sname}.asciidoc
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYING
%else
%license COPYING
%endif
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Tue Aug 9 2016 - Devrim GUNDUZ <devrim@gunduz.org> 1.2-1
- Update to 1.2

* Sun May 22 2016 - Devrim GUNDUZ <devrim@gunduz.org> 1.1-1
- Update to 1.1

* Tue Apr 29 2014 - Devrim GUNDUZ <devrim@gunduz.org> 1.0.0-2
- Remove barman dependency

* Mon Apr 14 2014 - Devrim GUNDUZ <devrim@gunduz.org> 1.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
