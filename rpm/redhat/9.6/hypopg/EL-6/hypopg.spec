%global pgmajorversion 96
%global pginstdir /usr/pgsql-9.6
%global sname	hypopg

Summary:	Hypothetical Indexes support for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	0.0.4
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/dalibo/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-makefile-pgxs.patch
URL:		https://github.com/dalibo/%{sname}/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This software is EXPERIMENTAL and therefore NOT production ready.
Use at your own risk.

HypoPG is a PostgreSQL extension adding support for hypothetical indexes.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
install -d %{buildroot}%{pginstdir}/doc/extension
install -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--%{version}.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Fri Oct 21 2016 - Devrim Gündüz <devrim@gunduz.org> 0.0.4
- Initial RPM packaging for PostgreSQL RPM Repository
