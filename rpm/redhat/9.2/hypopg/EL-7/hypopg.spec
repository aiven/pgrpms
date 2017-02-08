%global pgmajorversion 92
%global pginstdir /usr/pgsql-9.2
%global sname	hypopg

Summary:	Hypothetical Indexes support for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.0.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/dalibo/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-makefile-pgxs.patch
URL:		https://github.com/dalibo/%{sname}/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
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
* Thu Oct 27 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-1
- Update to 1.0.0

* Fri Oct 21 2016 - Devrim Gündüz <devrim@gunduz.org> 0.0.4-1
- Initial RPM packaging for PostgreSQL RPM Repository
