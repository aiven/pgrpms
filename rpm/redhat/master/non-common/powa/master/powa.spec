%if 0%{?rhel} && 0%{?rhel} <= 6
%global systemd_enabled 0
%else
%global systemd_enabled 1
%endif

%global sname powa
%global swebname powa-web
# Powa version
%global powamajorversion 4
%global powamidversion 0
%global powaminorversion 1
# powa-web version
%global powawebversion 4.0.0

%global	powawebdir  %{_datadir}/%{name}

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

Summary:	PostgreSQL Workload Analyzer
Name:		%{sname}_%{pgmajorversion}
Version:	%{powamajorversion}.%{powamidversion}.%{powaminorversion}
Release:	1%{?dist}
License:	BSD
Source0:	https://github.com/powa-team/powa-archivist/archive/REL_%{powamajorversion}_%{powamidversion}_%{powaminorversion}.tar.gz
Source1:	https://github.com/powa-team/powa-web/archive/%{powawebversion}.tar.gz
Source2:	powa-%{pgpackageversion}.service
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		http://dalibo.github.io/powa/
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-contrib
# Actually these are optional, but let's add them for a better PoWA instance.
Requires:	pg_qualstats%{pgmajorversion}, pg_stat_kcache%{pgmajorversion}
Requires:	hypopg_%{pgmajorversion}

%if %{systemd_enabled}
Requires:		systemd
Requires(post):		systemd-sysv
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
%endif

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
PoWA is PostgreSQL Workload Analyzer that gathers performance stats and
provides real-time charts and graphs to help monitor and tune your PostgreSQL
servers.
It is similar to Oracle AWR or SQL Server MDW.

%package web
Summary:	The user interface of powa
BuildRequires:	python3-setuptools
Requires:	python3-tornado >= 2.0, python3-psycopg2, python3-sqlalchemy

%description web
This is the user interface of POWA.

%prep
%setup -q -n %{sname}-archivist-REL_%{powamajorversion}_%{powamidversion}_%{powaminorversion}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
%{__make} %{?_smp_mflags}

# Build powa-web
tar zxf %{SOURCE1}
pushd %{swebname}-%{powawebversion}
%{__ospython} setup.py build
popd

%install
%{__rm} -rf %{buildroot}
%{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
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

%if %{systemd_enabled}
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{swebname}-%{pgpackageversion}.service
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{pginstdir}/doc/extension/%{sname}
%if %{systemd_enabled}
%doc %{pginstdir}/doc/extension/%{sname}/INSTALL.md
%doc %{pginstdir}/doc/extension/%{sname}/PL_funcs.md
%doc %{pginstdir}/doc/extension/%{sname}/README.md
%license %{pginstdir}/doc/extension/%{sname}/LICENSE.md
%else
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/%{sname}/*.md
%endif
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
%if %{systemd_enabled}
%{_unitdir}/%{swebname}-%{pgpackageversion}.service
%endif

%changelog
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
