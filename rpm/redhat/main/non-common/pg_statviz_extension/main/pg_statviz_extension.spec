%global sname pg_statviz
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

Summary:	CLI tool for time series analysis and visualization of PostgreSQL internal statistics.
Name:		%{sname}_extension_%{pgmajorversion}
Version:	0.4
Release:	1PGDG%{dist}
License:	GPLv2+
Source0:	https://github.com/vyruss/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/vyruss/%{sname}

Requires:	python3-plac python3-numpy python3-psycopg2 >= 2.9.5
Requires:	python3-six python3-matplotlib python3-cycler
Requires:	python3-cycler python3-fonttools python3-kiwisolver
Requires:	python3-packaging python3-pillow python3-dateutils
Requires:	python3-argh


BuildArch:	noarch

%description
pg_statviz is a minimalist extension and utility pair for time series analysis
and visualization of PostgreSQL internal statistics.

Created for snapshotting PostgreSQL's cumulative and dynamic statistics and
performing time series analysis on them. The accompanying utility can produce
visualizations for selected time ranges on the stored stats snapshots,
enabling the user to track PostgreSQL performance over time and potentially
perform tuning or troubleshooting.

Best served with pg_statviz extension package, which includes the extension
files.

%prep
%setup -q -n %{sname}-%{version}

%build

%install
# Manual installation is needed:
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__install} -m 755 %{sname}.control  %{buildroot}%{pginstdir}/share/extension/
%{__install} -m 755 %{sname}*sql  %{buildroot}%{pginstdir}/share/extension/

%files
%defattr(644,root,root,755)
%license LICENSE
%{pginstdir}/share/extension/*.control
%{pginstdir}/share/extension/*.sql

%changelog
* Mon Aug 21 2023 Devrim Gündüz <devrim@gunduz.org> - 0.4-1PGDG
- Update to 0.4

* Thu Aug 17 2023 Devrim Gündüz <devrim@gunduz.org> - 0.3-1PGDG
- Update to 0.3

* Thu Apr 20 2023 Devrim Gündüz <devrim@gunduz.org> - 0.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository
