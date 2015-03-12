%global pgmajorversion 94
%global pginstdir /usr/pgsql-9.4
%global sname pg_shard

Summary:	Easy sharding for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.0.2
Release:	1%{?dist}
License:	LGPLv3
Group:		Applications/Databases
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
Patch0:		%{sname}-makefile.patch
URL:		http://citusdata.com/docs/pg-shard
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Shards and replicates PostgreSQL tables for horizontal scale and high
availability. Seamlessly distributes SQL statements, without requiring
any application changes.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make %{?_smp_mflags} install DESTDIR=%{buildroot}
# Let's also install documentation:
%{__mkdir} -p %{buildroot}%{pginstdir}/share/extension
%{__cp} README.md %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md LICENSE
%doc %{pginstdir}/share/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Thu Mar 12 2015 - Devrim GUNDUZ <devrim@gunduz.org> 1.0.2-1
- Initial RPM packaging for PostgreSQL RPM Repository
