%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.3
%global sname pg_shard

Summary:	Easy sharding for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.2.2
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
%{__rm} -rf %{buildroot}
make %{?_smp_mflags} install DESTDIR=%{buildroot}
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} %{buildroot}%{pginstdir}/doc/extension/README.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/bin/copy_to_distributed_table
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Wed Mar 2 2016 - Devrim Gündüz <devrim@gunduz.org> 1.2.2-1
- Update to 1.2.2.

* Tue Jan 26 2016 - Devrim Gündüz <devrim@gunduz.org> 1.1.0-2
- Minor cosmetic updates for unified spec file.

* Fri Mar 20 2015 - Devrim GUNDUZ <devrim@gunduz.org> 1.1.0-1
- Update to 1.1.0

* Thu Mar 12 2015 - Devrim GUNDUZ <devrim@gunduz.org> 1.0.2-1
- Initial RPM packaging for PostgreSQL RPM Repository
