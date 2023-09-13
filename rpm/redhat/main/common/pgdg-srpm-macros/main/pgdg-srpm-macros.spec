%global debug_package %{nil}

%if 0%{?fedora} || 0%{?rhel} >= 7
%global macros_dir %{_rpmconfigdir}/macros.d
%else
%global macros_dir %{_sysconfdir}/rpm
%endif

%if 0%{?fedora} >= 36 || 0%{?rhel} >= 8
BuildArch:	noarch
%endif

Name:		pgdg-srpm-macros
Version:	1.0.34
Release:	1PGDG%{?dist}
Summary:	SRPM macros for building PostgreSQL PGDG Packages

License:	PostgreSQL
URL:		https://yum.PostgreSQL.org
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
%license COPYRIGHT
%doc AUTHORS
%{macros_dir}/macros.pgdg-postgresql

%changelog
* Wed Sep 13 2023 Devrim Gündüz <devrim@gunduz.org> - 1.0.34-1PGDG
- Update libgeotiffmajorversion to 17, add Proj 9.3, and update GDAL
  to 3.7.2

* Mon Aug 21 2023 Devrim Gündüz <devrim@gunduz.org> - 1.0.33-2PGDG
- Remove RHEL 6 bits

* Thu Aug 10 2023 Devrim Gündüz <devrim@gunduz.org> - 1.0.33-1PGDG
- Add GDAL 3.7 and GeOS 3.12.0
- Update PROJ to 9.2.1
- Add PGDG branding.

* Mon Mar 27 2023 Devrim Gündüz <devrim@gunduz.org> - 1.0.32-1
- Add libgeotiff16instdir macro, remove obsoleted llvm macro,
  update copyright year.

* Thu Mar 23 2023 Devrim Gündüz <devrim@gunduz.org> - 1.0.31-1
- Update GeOS 311 to 3.11.2

* Wed Mar 15 2023 Devrim Gündüz <devrim@gunduz.org> - 1.0.30-1
- Add Proj 9.2.0
- Update GDAL36 to 3.6.3

* Mon Dec 5 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0.29-1
- Remove AT support from RHEL 7 - ppc64le
- Update Proj to 9.1.1

* Wed Nov 23 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0.28-1
- Update GeOS to 3.11.1

* Mon Nov 14 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0.27-1
- Add GDAL 3.6.0 and reorder some items

* Fri Sep 16 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0.26-1
- Add Proj 9.1.0 and update GDAL to 3.5.2

* Fri Aug 19 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0.25-1
- Add GDAL 3.5

* Tue Jul 12 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0.24-1
- Add GeOS 3.11, update GeOS 3.10, GDAL 3.4 and PROJ 9.0.

* Wed Mar 2 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0.23-1
- Add Proj 9.0

* Fri Jan 7 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0.22-1
- Update PROJ to 8.2.1 and GDAL to 3.4.1

* Thu Dec 16 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0.21-1
- Add PROJ 8.2 support

* Tue Oct 26 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0.20-1
- Add GDAL 3.4.0, update GeOS 3.9 to 3.9.2

* Tue Oct 26 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0.19-1
- Add GeOS 3.10

* Wed Sep 1 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0.18-1
- Update GDAL and Proj versions.

* Wed Sep 1 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0.17-1
- Add libgeotiff17 macros

* Thu Aug 26 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0.16-1
- Add Proj 8.1 and GDAL 3.2 macros.

* Thu Jun 17 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0.15-1
- Add version specific macros for gdal

* Tue May 18 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0.14-1
- Update PROJ to 8.0.1 and GDAL to 3.2.3.

* Mon Mar 8 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0.13-1
- Update PROJ to 8.0.0, GDAL to 3.2.2 and GeOS to 3.9.1

* Fri Jan 8 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0.12-1
- Introduce pgdg_set_llvm_variables macro, to specify which
  distro/arch combinations have llvm support.

* Wed Jan 6 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0.11-1
- Update GDAL to 3.2.1 and PROJ to 7.2.1

* Sun Dec 20 2020 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.10-1
- Update GeOS to 3.9.0

* Fri Nov 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.9-1
- Add custom macros for (supported) PROJ versions. Without this,
  all PROJ packages would install under the same directory, whatever
  the latest version is.

* Thu Nov 5 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.8-1
- Remove libspatialitemajorversion macro definition. Apparently
  conditional does not work in the macro file.
- Update Proj to 7.2.0, GDAL to 3.2.0

* Fri Oct 30 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.7-1
- Add missing libspatialitemajorversion macro.

* Thu Oct 8 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.6-1
- Add IBM Advance Toolchain 12, 13 and 14 support

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
