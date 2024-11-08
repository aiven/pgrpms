%global sname pg_statviz

%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

Summary:	CLI tool for time series analysis and visualization of PostgreSQL internal statistics.
Name:		%{sname}
Version:	0.7
Release:	1PGDG%{dist}
License:	GPLv2+
Source0:	https://github.com/vyruss/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/vyruss/%{sname}

Requires:	python3-plac python3-numpy python3-psycopg3 >= 3.2.1
Requires:	python3-six python3-matplotlib python3-kiwisolver
Requires:	python3-packaging python3-argh

%if 0%{?fedora} >= 38 || 0%{?rhel} >= 8
Requires:	python3-cycler python3-dateutils python3-pillow
Requires:	python3-fonttools
%endif
%if 0%{?suse_version} >= 1315
Requires:	python3-Cycler python3-python-dateutil python3-Pillow
Requires:	python3-FontTools
%endif

BuildArch:	noarch

%description
pg_statviz is a minimalist extension and utility pair for time series analysis
and visualization of PostgreSQL internal statistics.

Created for snapshotting PostgreSQL's cumulative and dynamic statistics and
performing time series analysis on them. The accompanying utility can produce
visualizations for selected time ranges on the stored stats snapshots,
enabling the user to track PostgreSQL performance over time and potentially
perform tuning or troubleshooting.

Best served with pg_statviz extensions package, which includes the extension files.

%prep
%setup -q -n %{sname}-%{version}

%build

%install
# Manual installation is needed:
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{python3_sitelib}
%{__mv} src/run_%{sname} %{buildroot}%{_bindir}/%{sname}
%{__mv} src/%{sname} %{buildroot}%{python3_sitelib}

%files
%defattr(644,root,root,755)
%license LICENSE
%attr(0755,root,root) %{_bindir}/%{sname}
%{python3_sitelib}/%{sname}

%changelog
* Mon Jul 22 2024 Devrim Gündüz <devrim@gunduz.org> - 0.7-1PGDG
- Update to 0.7 per changes described at:
  https://github.com/vyruss/pg_statviz/releases/tag/v0.7

* Tue Feb 20 2024 Devrim Gündüz <devrim@gunduz.org> - 0.6-2PGDG
- Organise dependencies to support SLES 15.

* Thu Sep 7 2023 Devrim Gündüz <devrim@gunduz.org> - 0.6-1PGDG
- Update to 0.6

* Thu Aug 24 2023 Devrim Gündüz <devrim@gunduz.org> - 0.5-1PGDG
- Update to 0.5

* Mon Aug 21 2023 Devrim Gündüz <devrim@gunduz.org> - 0.4-1PGDG
- Update to 0.4

* Thu Aug 17 2023 Devrim Gündüz <devrim@gunduz.org> - 0.3-1PGDG
- Update to 0.3

* Thu Apr 20 2023 Devrim Gündüz <devrim@gunduz.org> - 0.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository
