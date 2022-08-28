%global sname timestamp9

Summary:	An efficient nanosecond precision timestamp type for Postgres
Name:		%{sname}_%{pgmajorversion}
Version:	1.1.0
Release:	1%{?dist}
License:	MIT
Source0:	https://github.com/fvannee/%{sname}/archive/refs/tags/%{sname}-%{version}.tar.gz
URL:		https://github.com/fvannee/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
BuildRequires:	cmake3
Requires:	postgresql%{pgmajorversion}-server

%description
timestamp9 is an efficient nanosecond precision timestamp type
for PostgreSQL.

%prep
%setup -q -n %{sname}-%{sname}-%{version}

%build
%{__mkdir} build
pushd build
PATH=%{pginstdir}/bin/:$PATH cmake3 ..
popd

%install
%{__rm} -rf %{buildroot}
pushd build
PATH=%{pginstdir}/bin/:$PATH  %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
popd

%files
%defattr(644,root,root,755)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Sun Aug 28 2022 - Devrim Gündüz <devrim@gunduz.org> 1.1.0-1
- Initial RPM packaging for PostgreSQL YUM Repository
