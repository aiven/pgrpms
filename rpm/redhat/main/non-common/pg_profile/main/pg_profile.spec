%global sname pg_profile

Summary:	Tool to find out most resource intensive activities in your PostgreSQL databases
Name:		%{sname}_%{pgmajorversion}
Version:	4.6
Release:	1PGDG%{?dist}
License:	BSD
Source0:	https://github.com/zubkov-andrei/%{sname}/archive/refs/tags/%{version}.tar.gz
URL:		https://github.com/zubkov-andrei/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-contrib postgresql%{pgmajorversion}-server
Recommends:	pg_stat_kcache_%{pgmajorversion}

BuildArch:	noarch

%description
This extension for PostgreSQL helps you to find out most resource
intensive activities in your PostgreSQL databases.

This extension is based on statistics views of PostgreSQL and contrib
extensions pg_stat_statements and pg_stat_kcache.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/share/extension/%{sname}*sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Fri May 10 2024 Devrim Gündüz <devrim@gunduz.org> - 4.6-1PGDG
- Update to 4.6 per changes described at:
  https://github.com/zubkov-andrei/pg_profile/releases/tag/4.6

* Wed Feb 21 2024 Devrim Gündüz <devrim@gunduz.org> - 4.4-1PGDG
- Update to 4.4 per changes described at:
  https://github.com/zubkov-andrei/pg_profile/releases/tag/4.4

* Mon Feb 12 2024 Devrim Gündüz <devrim@gunduz.org> - 4.3-1PGDG
- Initial RPM packaging for the PostgreSQL RPM Repository
