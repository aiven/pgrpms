%global debug_package %{nil}
%global pgmajorversion 94
%global pginstdir /usr/pgsql-9.4
%global sname powa
%global powamajorversion 1
%global powaminorversion 1

Summary:	PostgreSQL Workload Analyzer
Name:		%{sname}_%{pgmajorversion}
Version:	%{powamajorversion}.%{powaminorversion}
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/dalibo/%{sname}/archive/REL_%{powamajorversion}_%{powaminorversion}.zip
Patch0:		%{sname}-makefile.patch
URL:		http://dalibo.github.io/powa/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
PoWA is PostgreSQL Workload Analyzer that gathers performance stats and
provides real-time charts and graphs to help monitor and tune your PostgreSQL
servers.
It is similar to Oracle AWR or SQL Server MDW.

%prep
%setup -q -n %{sname}-REL_%{powamajorversion}_%{powaminorversion}
%patch0 -p0

%build
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
# Move README file under PostgreSQL installation directory
%{__mkdir} -p -m 700 %{buildroot}/%{pginstdir}/share/extension
%{__mv} %{buildroot}/%{_docdir}/pgsql/extension/README.md %{buildroot}/%{pginstdir}/share/extension/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/share/extension/README.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Wed Aug 27 2014 - Devrim GUNDUZ <devrim@gunduz.org> 1.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
