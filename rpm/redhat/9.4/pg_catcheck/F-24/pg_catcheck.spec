%global pgmajorversion 94
%global pginstdir /usr/pgsql-9.4
%global sname pg_catcheck

Summary:	Tool for diagnosing PostgreSQL system catalog corruption
Name:		%{sname}%{pgmajorversion}
Version:	1.0.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://get.enterprisedb.com/src/%{sname}-%{version}.tar.gz
Patch0:		%{sname}-makefile-pgxs.patch
URL:		http://www.enterprisedb.com
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
pg_catcheck is a simple tool for diagnosing system catalog corruption.
If you suspect that your system catalogs are corrupted, this tool may
help you figure out exactly what problems you have and how serious they
are. If you are paranoid, you can run it routinely to search for system
catalog corruption that might otherwise go undetected. However, pg_catcheck
is not a general corruption detector. For that, you should use PostgreSQL's
checksum feature (`initdb -k`).

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

make USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
install -d %{buildroot}%{pginstdir}/doc
install -m 755 README.md %{buildroot}%{pginstdir}/doc/README-%{sname}.md

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(755,root,root,755)
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%{pginstdir}/bin/%{sname}
%{pginstdir}/doc/README-%{sname}.md

%changelog
* Sun Sep 7 2014 - Devrim GUNDUZ <devrim@gunduz.org> 1.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
