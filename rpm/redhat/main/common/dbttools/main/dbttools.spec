Summary:	Shared tools for dbt2 tests
Name:		dbttools
Version:	0.3.1
Release:	1%{dist}
License:	GPLv2+
Source0:	https://github.com/osdldbt/dbttools/archive/refs/tags/v0.3.1.tar.gz
URL:		https://github.com/osdldbt/dbttools

BuildArch:	noarch
Requires:	R-core >= 2.9.2

%description
The purpose of this package is to provide tools that are shared between
all kits in the database test projects.

These scripts currently depend on R.

%prep
%setup -q -n %{name}-%{version}

%build

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}/%{_bindir}

%{__cp} bin/dbt-p* %{buildroot}/%{_bindir}
%{__cp} bin/pgsql/* %{buildroot}/%{_bindir}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%license LICENSE
%attr (755,root,root) %{_bindir}/dbt-pgsql*
%attr (755,root,root) %{_bindir}/dbt-plot*
%attr (755,root,root) %{_bindir}/dbt-process-pidstat


%changelog
* Mon Oct 3 2022 Devrim Gündüz <devrim@gunduz.org> - 0.3.1-1
- Initial packaging
