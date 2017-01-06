%global pgmajorversion 10
%global pginstdir /usr/pgsql-10
%global sname postgresql-unit

Summary:	SI Units for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	1.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/ChristophBerg/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-makefile-pgxs.patch
URL:		https://github.com/ChristophBerg/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
postgresql-unit implements a PostgreSQL datatype for SI units, plus byte.
The base units can be combined to named and unnamed derived units using
operators defined in the PostgreSQL type system. SI prefixes are used for
input and output, and quantities can be converted to arbitrary scale.

Requires PostgreSQL 9.4 or later (uses psprintf()), flex, and bison 3 (the
pre-built grammar files are used if only bison 2 is available).

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
make USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}
# Install README and howto file under PostgreSQL installation directory:
install -d %{buildroot}%{pginstdir}/doc/extension
install -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/unit.so
%{pginstdir}/share/extension/unit*.sql
%{pginstdir}/share/extension/unit.control

%changelog
* Thu Sep 22 2016 - Devrim GUNDUZ <devrim@gunduz.org> 1.0-1
- Initial RPM packaging for PostgreSQL YUM Repository
