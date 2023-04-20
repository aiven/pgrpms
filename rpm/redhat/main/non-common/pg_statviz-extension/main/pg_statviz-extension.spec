%global debug_package %{nil}
%global sname	pg_statviz

Summary:	Extension for time series analysis and visualization of PostgreSQL internal statistics.
Name:		%{sname}-pg%{pgmajorversion}-extension
Version:	0.1
Release:	1%{dist}
License:	GPLv2+
Source0:	https://github.com/vyruss/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/vyruss/%{sname}

BuildRequires:	postgresql%{pgmajorversion}-devel

%description
pg_statviz is a minimalist extension and utility pair for time series analysis
and visualization of PostgreSQL internal statistics.

Created for snapshotting PostgreSQL's cumulative and dynamic statistics and
performing time series analysis on them. The accompanying utility can produce
visualizations for selected time ranges on the stored stats snapshots,
enabling the user to track PostgreSQL performance over time and potentially
perform tuning or troubleshooting.

Best served with pg_statviz package, which includes command line tool.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__mv}  %{buildroot}%{pginstdir}/doc/extension/README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

# Remove binary, they are installed with the common package.
%{__rm} -f %{buildroot}/%{_bindir}/*

%clean
%{__rm} -rf %{buildroot}
%files
%defattr(644,root,root,755)
%license LICENSE
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}*.sql

%changelog
* Thu Apr 20 2023 Devrim Gündüz <devrim@gunduz.org> - 0.1-1
- Initial packaging for the PostgreSQL RPM repository
