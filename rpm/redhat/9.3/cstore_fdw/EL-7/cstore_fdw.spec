%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.3
%global sname cstore_fdw

Summary:	Columnar store extension for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.5.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/citusdata/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-makefile.patch
URL:		http://citusdata.github.io/cstore_fdw/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	protobuf-c-devel

%description
cstore_fdw is column-oriented store available for PostgreSQL. Using it will
let you:
    Leverage typical analytics benefits of columnar stores
    Deploy on stock PostgreSQL or scale-out PostgreSQL (CitusDB)

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make

%install
%{__rm} -rf %{buildroot}
make %{?_smp_mflags} install DESTDIR=%{buildroot}
# Let's also install documentation:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-cstore_fdw.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%doc LICENSE
%else
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%endif
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Wed Sep 7 2016 - Devrim Gündüz <devrim@gunduz.org> 1.5.0-1
- Update to 1.5.0
- Add LICENSE among installed files.

* Thu Jun 2 2016 - Devrim Gündüz <devrim@gunduz.org> 1.4.1-1
- Update to 1.4.1

* Mon Jan 18 2016 - Devrim Gündüz <devrim@gunduz.org> 1.4-1
- Update to 1.4
- Parallel build seems to be broken, so disable it for now.

* Mon Sep 07 2015 - Devrim Gündüz <devrim@gunduz.org> 1.3-1
- Update to 1.3

* Thu Mar 12 2015 - Devrim Gündüz <devrim@gunduz.org> 1.2-1
- Update to 1.2

* Fri Aug 29 2014 - Devrim Gündüz <devrim@gunduz.org> 1.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
