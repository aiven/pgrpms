%global pginstdir	/usr/pgsql-9.0
%global pgmajorversion	90
%global sname	plr
Summary:	Procedural language interface between PostgreSQL and R
Name:		%{sname}%{pgmajorversion}
Version:	8.3.0.11
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://www.joeconway.com/%{sname}/%{sname}-%{version}.tar.gz
Patch0:		Makefile-pgxs.patch
URL:		http://www.joeconway.com/plr/
BuildRequires:	postgresql%{pgmajorversion}-devel R-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Procedural Language Handler for the "R software environment for 
statistical computing and graphics".

%prep
%setup -q -n %{sname}
%patch0 -p1

%build
#make R_HOME=/usr USE_PGXS=1 %{?_smp_mflags} 
make USE_PGXS=1 %{?_smp_mflags} 

%install
rm -rf %{buildroot}
make USE_PGXS=1 DESTDIR=%{buildroot}/ install
install -d %{buildroot}%{_docdir}/%{name}
mv %{buildroot}%{_docdir}/pgsql/contrib/README.plr %{buildroot}%{_docdir}/%{name}/

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig 

%files
%defattr(644,root,root,755)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/contrib/%{sname}.sql
%doc %{_docdir}/%{name}/README.plr

%changelog
* Fri Oct 8 2010 - Devrim GUNDUZ <devrim@gunduz.org> 8.3.0-11-1
- Initial packaging for 9.0, which also suits new PostgreSQL RPM layout.
