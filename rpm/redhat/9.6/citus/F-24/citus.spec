%global pgmajorversion 96
%global pgpackageversion 9.6
%global pginstdir /usr/pgsql-%{pgpackageversion}
%global sname citus

Summary:	PostgreSQL-based distributed RDBMS
Name:		%{sname}_%{pgmajorversion}
Version:	5.0.0
Release:	2%{dist}
License:	AGPLv3+
Group:		Applications/Databases
Source0:	https://github.com/citusdata/citus/archive/v5.0.0.tar.gz
URL:		https://github.com/citusdata/citus
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

%package devel
Summary:	Citus development header files and libraries
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The citus_%{pgmajorversion}-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact with Citus.

%prep
%setup -q -n %{sname}-%{version}

%build
%configure PG_CONFIG=%{pginstdir}/bin/pg_config
make %{?_smp_mflags}

%install
%make_install

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
%doc README.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/bin/copy_to_distributed_table
%{pginstdir}/bin/csql
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif

%files devel
%{pginstdir}/include/server/citus_config.h
%{pginstdir}/include/server/distributed/*.h

%changelog
* Thu Mar 31 2016 - Devrim Gündüz <devrim@gunduz.org> 5.0.0-2
- Split header files into -devel subpackage.
- Add doc and license files.

* Fri Mar 25 2016 - Devrim Gündüz <devrim@gunduz.org> 5.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository,
  based on the spec file of Jason Petersen @ Citus.
