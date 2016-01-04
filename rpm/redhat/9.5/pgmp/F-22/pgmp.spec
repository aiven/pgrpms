%global pgmajorversion 95
%global pginstdir /usr/pgsql-9.5
%global sname pgmp

Summary:	PostgreSQL Multiple Precision Arithmetic Extension
Name:		%{sname}%{pgmajorversion}
Version:	1.0.2
Release:	1%{?dist}
License:	LGPL
Group:		Applications/Databases
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
Patch0:		%{sname}-Makefile.patch
URL:		http://pgxn.org/dist/pgmp/
BuildRequires:	postgresql%{pgmajorversion}-devel, gmp-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	gmp

%description
The pgmp extension adds PostgreSQL data types wrapping the high performance
integer and rational data types offered by the GMP library.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

make USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/%{sname}/*.rst
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/%{sname}/%{sname}*.sql

%changelog
* Mon Jan 19 2015 - Devrim GUNDUZ <devrim@gunduz.org> 1.0.2-1
- Initial RPM packaging for PostgreSQL RPM Repository
