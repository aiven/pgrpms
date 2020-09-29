%global debug_package %{nil}

%if 0%{?fedora} || 0%{?rhel} >= 7
%global macros_dir %{_rpmconfigdir}/macros.d
%else
%global macros_dir %{_sysconfdir}/rpm
%endif

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 8
BuildArch:	noarch
%endif

Name:		pgdg-srpm-macros
Version:	1.0.5
Release:	1%{?dist}
Summary:	SRPM macros for building PostgreSQL PGDG Packages

License:	PostgreSQL
URL:		https://yum.PostgreSQL.org/pgdg-srpm-macros
Source0:	macros.pgdg-postgresql
Source1:	COPYRIGHT
Source2:	AUTHORS

%description
A set of macros for building PostgreSQL PGDG packages. 3rd party packagers can
override these macros and use their own.

%prep
%setup -c -T
%{__cp} %{SOURCE1} %{SOURCE2} .


%build
echo no build stage needed

%install
%{__install} -p -D -m 0644 %{SOURCE0} %{buildroot}/%{macros_dir}/macros.pgdg-postgresql

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYRIGHT AUTHORS
%else
%license COPYRIGHT
%doc AUTHORS
%endif
%{macros_dir}/macros.pgdg-postgresql

%changelog
* Tue Sep 29 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.5-1
- Update libgeotiff to 1.6
- Update GDAL to 3.1.3

* Mon Aug 17 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-1
- Update Proj to 7.1.0
- Add AT 11 support

* Mon May 11 2020 John K. Harvey <john.harvey@crunchydata.com> - 1.0.3-2
- Small fix for plpython3 macro for EL-7

* Sun May 10 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.3-1
- Make plpython3 macro consistent with the PostgreSQL spec file.
  Per John K. Harvey.

* Tue May 5 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.2-1
- Update Proj to 7.0.1

* Thu Apr 16 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.1-1
- Add CXX flags for PPC64LE. Extracted from another patch by Talha.

* Fri May 31 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1
- Initial packaging for PostgreSQL RPM Repository
