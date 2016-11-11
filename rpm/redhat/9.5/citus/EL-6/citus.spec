%global pgmajorversion 95
%global pgpackageversion 9.5
%global pginstdir /usr/pgsql-%{pgpackageversion}
%global sname citus

Summary:	PostgreSQL-based distributed RDBMS
Name:		%{sname}_%{pgmajorversion}
Version:	5.2.2
Release:	1%{dist}
License:	AGPLv3
Group:		Applications/Databases
Source0:	https://github.com/citusdata/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/citusdata/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel libxml2-devel
BuildRequires:	libxslt-devel openssl-devel pam-devel readline-devel
Requires:	postgresql%{pgmajorversion}-server
Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Citus horizontally scales PostgreSQL across commodity servers
using sharding and replication. Its query engine parallelizes
incoming SQL queries across these servers to enable real-time
responses on large datasets.

Citus extends the underlying database rather than forking it,
which gives developers and enterprises the power and familiarity
of a traditional relational database. As an extension, Citus
supports new PostgreSQL releases, allowing users to benefit from
new features while maintaining compatibility with existing
PostgreSQL tools. Note that Citus supports many (but not all) SQL
commands.

%prep
%setup -q -n %{sname}-%{version}

%build
%configure PG_CONFIG=%{pginstdir}/bin/pg_config
make %{?_smp_mflags}

%install
%make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%post
%{_sbindir}/update-alternatives --install %{_bindir}/csql \
    %{sname}-csql %{pginstdir}/bin/csql %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/copy_to_distributed_table \
    %{sname}-copy_to_distributed_table %{pginstdir}/bin/copy_to_distributed_table %{pgmajorversion}0

%postun
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove %{sname}-csql \
	%{pginstdir}/bin/csql
    %{_sbindir}/update-alternatives --remove %{sname}-copy_to_distributed_table \
	%{pginstdir}/bin/copy_to_distributed_table
fi

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/include/server/citus_config.h
%{pginstdir}/include/server/distributed/*.h
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/bin/copy_to_distributed_table
%{pginstdir}/bin/csql
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Wed Nov 9 2016 - Devrim Gündüz <devrim@gunduz.org> 5.2.2-1
- Update to 5.2.2

* Sat Sep 17 2016 - Devrim Gündüz <devrim@gunduz.org> 5.2.1-1
- Update to 5.2.1

* Fri Aug 26 2016 - Devrim Gündüz <devrim@gunduz.org> 5.2.0-1
- Update to 5.2.0. Fixes #1566.
- Update license and install docs. Fixes #1385.

* Thu Jul 7 2016 - Devrim Gündüz <devrim@gunduz.org> 5.1.1-1
- Update to 5.1.1

* Tue May 17 2016 - Jason Petersen <jason@citusdata.com> 5.1.0-1
- Update to Citus 5.1.0

* Fri Mar 25 2016 - Devrim Gündüz <devrim@gunduz.org> 5.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository,
  based on the spec file of Jason Petersen @ Citus.
