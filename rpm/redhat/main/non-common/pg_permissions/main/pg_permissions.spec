%global sname pg_permissions

%global tarballversion REL_1_1

Summary:	PostgreSQL permission reports and checks
Name:		%{sname}_%{pgmajorversion}
Version:	1.1
Release:	3%{?dist}
License:	PostgreSQL
Source0:	https://github.com/cybertec-postgresql/%{sname}/archive/refs/tags/%{tarballversion}.tar.gz
URL:		https://github.com/cybertec-postgresql/pg_permissions/
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server
BuildArch:	noarch

%description
This extension allows you to review object permissions on a PostgreSQL
database.

%prep
%setup -q -n %{sname}-%{tarballversion}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README.%{sname}
%{pginstdir}/share/extension/%{sname}*.*

%changelog
* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.1-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Fri Sep 10 2021 Devrim Gündüz <devrim@gunduz.org> - 1.1-2
- Bump of for rpm Makefile issues on RHEL 7 and RHEL 8.

* Wed Sep 8 2021 Devrim Gündüz <devrim@gunduz.org> - 1.1-1
- Initial packaging for PostgreSQL RPM Repository
