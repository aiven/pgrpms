%global __python %{_bindir}/python3
%global sname powa
%global swebname powa-web
# Powa archivist version
%global powamajorversion 4
%global powamidversion 1
%global powaminorversion 4
# powa-web version
%global powawebversion 4.1.3

%global	powawebdir  %{_datadir}/%{name}

%global __ospython %{_bindir}/python3
%if 0%{?fedora} >= 35
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")


Summary:	PostgreSQL Workload Analyzer
Name:		%{sname}_%{pgmajorversion}
Version:	%{powamajorversion}.%{powamidversion}.%{powaminorversion}
Release:	2%{?dist}
License:	BSD
Source0:	https://github.com/powa-team/powa-archivist/archive/REL_%{powamajorversion}_%{powamidversion}_%{powaminorversion}.tar.gz
Source1:	https://github.com/powa-team/powa-web/archive/refs/tags/%{powawebversion}.tar.gz
Source2:	powa-%{pgpackageversion}.service
URL:		https://powa.readthedocs.io/
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-contrib
# Actually these are optional, but let's add them for a better PoWA instance.
Requires:	pg_qualstats_%{pgmajorversion}, pg_stat_kcache_%{pgmajorversion}
Requires:	hypopg_%{pgmajorversion}

# We require this to be present for %%{_prefix}/lib/tmpfiles.d
Requires:		systemd
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
Requires(post):		systemd-sysvinit
%endif
%else
Requires(post):		systemd-sysv
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
%endif

%description
PoWA is PostgreSQL Workload Analyzer that gathers performance stats and
provides real-time charts and graphs to help monitor and tune your PostgreSQL
servers.
It is similar to Oracle AWR or SQL Server MDW.

%package web
Summary:	The user interface of powa
BuildRequires:	python3-setuptools
Requires:	python3-psycopg2
%if 0%{?rhel} == 7
Requires:	python36-tornado >= 2.0 python36-sqlalchemy
%else
Requires:	python3-tornado >= 2.0 python3-sqlalchemy
%endif

%description web
This is the user interface of POWA.

%prep
%setup -q -n %{sname}-archivist-REL_%{powamajorversion}_%{powamidversion}_%{powaminorversion}

%build
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

# Build powa-web
tar zxf %{SOURCE1}
pushd %{swebname}-%{powawebversion}
%{__ospython} setup.py build
popd

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
# Move powa docs into their own subdirectory:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension/%{sname}
%{__install} INSTALL.md LICENSE.md PL_funcs.md README.md %{buildroot}%{pginstdir}/doc/extension/%{sname}

# Install powa-web
pushd %{swebname}-%{powawebversion}
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}
# Install sample conf file
%{__mkdir} -p %{buildroot}%{_sysconfdir}
%{__install} powa-web.conf-dist %{buildroot}%{_sysconfdir}
popd

%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{swebname}-%{pgpackageversion}.service

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{pginstdir}/doc/extension/%{sname}
%doc %{pginstdir}/doc/extension/%{sname}/INSTALL.md
%doc %{pginstdir}/doc/extension/%{sname}/PL_funcs.md
%doc %{pginstdir}/doc/extension/%{sname}/README.md
%license %{pginstdir}/doc/extension/%{sname}/LICENSE.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
  %endif
 %endif
%endif

%files web
%defattr(-,root,root,-)
%{_bindir}/%{swebname}
%dir %{python_sitelib}/%{sname}
%{python_sitelib}/%{sname}/*
%{python_sitelib}/powa_web-%{powawebversion}-py%{pyver}.egg-info/*
%{_sysconfdir}/powa-web.conf-dist
%{_unitdir}/%{swebname}-%{pgpackageversion}.service

%changelog
* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 4.1.4-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu May 19 2022 Devrim Gündüz <devrim@gunduz.org> - 4.1.4-1
- Update to 4.1.4

* Mon Feb 14 2022 Devrim Gündüz <devrim@gunduz.org> - 4.1.3-1
- Update to 4.1.3

* Tue Nov 2 2021 Devrim Gündüz <devrim@gunduz.org> - 4.1.2-5
- Add Fedora 35 support

* Tue Jun 29 2021 Devrim Gündüz <devrim@gunduz.org> - 4.1.2-4
- Add SLES support

* Mon Jun 28 2021 Devrim Gündüz <devrim@gunduz.org> - 4.1.2-3
- Update powa-web to 4.1.2

* Sat Jun 5 2021 Devrim Gündüz <devrim@gunduz.org> - 4.1.2-2
- Remove pgxs patches, and export PATH instead.
- Remove RHEL 6 stuff.

* Tue Dec 22 2020 Devrim Gündüz <devrim@gunduz.org> - 4.1.2-1
- Update to 4.1.2

* Sat Dec 12 2020 Devrim Gündüz <devrim@gunduz.org> - 4.1.0-1
- Update to 4.1.0

* Fri May 29 2020 Devrim Gündüz <devrim@gunduz.org> - 4.0.1-2
- Fix dependency issue on RHEL 7. Per
  https://github.com/powa-team/powa/issues/129

* Tue May 12 2020 Devrim Gündüz <devrim@gunduz.org> - 4.0.1-1
- Update to 4.0.1

* Mon Apr 20 2020 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-1
- Update to 4.0.0

* Sat Jan 18 2020 Devrim Gündüz <devrim@gunduz.org> - 3.2.0-3
- Attempt to fix RHEL 8 builds. Move to Python3.

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Fri Nov 9 2018 Devrim Gündüz <devrim@gunduz.org> - 3.2.0-2
- Update powa-web to 3.2.0

* Tue Oct 16 2018 Devrim Gündüz <devrim@gunduz.org> - 3.2.0-1
- Update to 3.2.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 3.1.1-2.1
- Rebuild against PostgreSQL 11.0

* Fri Mar 16 2018 - Devrim Gündüz <devrim@gunduz.org> 3.1.2-1
- Add debuginfo package, per #3207

* Wed Sep 20 2017 - Devrim Gündüz <devrim@gunduz.org> 3.1.1-1
- Update to 3.1.1
- Update powa-web to 3.1.4
  Fixes #2718.

* Wed Jul 19 2017 - Devrim Gündüz <devrim@gunduz.org> 3.1.0-4
- Update powa-web to 3.1.3
- Add systemd support
- Install sample config file.

* Fri Jan 27 2017 - Devrim Gündüz <devrim@gunduz.org> 3.1.0-3
- Update powa-web to 3.1.1

* Wed Jan 25 2017 - Devrim Gündüz <devrim@gunduz.org> 3.1.0-2
- Fix dependencies, per patch from Thomas Reiss. Per #2072.
- Add dependency for hypopg, per #2073.

* Fri Oct 28 2016 - Devrim Gündüz <devrim@gunduz.org> 3.1.0-1
- Update both components to 3.1.0

* Wed Feb 10 2016 - Devrim Gündüz <devrim@gunduz.org> 3.0.1-1
- Update to 3.0.1

* Wed Jan 27 2016 - Devrim Gündüz <devrim@gunduz.org> 3.0.0-1
- Update to 3.0.0
- Improve spec file, to fix multiple issues.

* Mon Jan 19 2015 - Devrim Gündüz <devrim@gunduz.org> 1.2.1-1
- Update to 1.2.1
- Fix a stupid oversight in spec file: This package contains
  3 digit version number.

* Tue Oct 28 2014 - Devrim Gündüz <devrim@gunduz.org> 1.2-1
- Update to 1.2

* Wed Aug 27 2014 - Devrim Gündüz <devrim@gunduz.org> 1.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
