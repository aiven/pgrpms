Summary:	Reliable PostgreSQL Backup & Restore
Name:		pgbackrest
Version:	1.01
Release:	1%{?dist}
License:	MIT
Group:		Applications/Databases
Url:		http://www.pgbackrest.org/
Patch0:		pgbackrest-changeperldir.patch
Source0:	https://github.com/pgbackrest/pgbackrest/archive/release/%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	perl

%description
pgBackRest aims to be a simple, reliable backup and restore system that can
seamlessly scale up to the largest databases and workloads.

Instead of relying on traditional backup tools like tar and rsync, pgBackRest
implements all backup features internally and uses a custom protocol for
communicating with remote systems. Removing reliance on tar and rsync allows
for better solutions to database-specific backup challenges. The custom remote
protocol allows for more flexibility and limits the types of connections that
are required to perform a backup which increases security.

%prep
%setup -q -n %{name}-release-%{version}
%patch0 -p0

%build

%install
install -D -d -m 0755 %{buildroot}%{perl_vendorlib} %{buildroot}%{_bindir}
cp -a lib/*       %{buildroot}%{perl_vendorlib}/
cp -a bin/%{name} %{buildroot}%{_bindir}/%{name}

%files
%defattr(-,root,root)
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%{_bindir}/%{name}
%{perl_vendorlib}/pgBackRest/

%changelog
* Fri May 27 2016 - Devrim Gündüz <devrim@gunduz.org> 1.01-1
- Initial packaging for PostgreSQL RPM Repository

