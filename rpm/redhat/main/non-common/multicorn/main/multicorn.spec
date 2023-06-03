%global sname multicorn
%global python_runtimes python3

# Python major version.
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python_sitearch %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	Multicorn Python bindings for Postgres FDW
Name:		%{sname}_%{pgmajorversion}
Version:	1.4.0
Release:	5%{?dist}.2
License:	PostgreSQL
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
Patch0:		%{sname}-python-destdir.patch
URL:		http://pgxn.org/dist/multicorn/
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
BuildRequires:	python3-devel

Provides:	%{sname}%{pgmajorversion} = %{version}-%{release}
Obsoletes:	%{sname}%{pgmajorversion} < 1.4.0-3

# Provide versionless multicorn. This will simplify using
# bigquery_fdw package.
Provides:	%{sname} = %{version}

%description
The Multicorn Foreign Data Wrapper allows you to write foreign data wrappers
in python.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for multicorn
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:  llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:  llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for multicorn
%endif

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p0

%build
export PYTHON_OVERRIDE="python%{pyver}"

PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
export PYTHON_OVERRIDE="python%{pyver}"
PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc README.md
%{pginstdir}/share/extension/%{sname}--%{version}.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/doc/extension/%{sname}.md
%{pginstdir}/lib/%{sname}.so
%dir %{python_sitearch}/%{sname}-%{version}-py%{pyver}.egg-info
%{python_sitearch}/%{sname}-%{version}-py%{pyver}.egg-info/*
%dir %{python_sitearch}/%{sname}/
%{python_sitearch}/%{sname}/*

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.4.0-5.2
- Rebuild against LLVM 15 on SLES 15

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 1.4.0-5.1
- Modernise %patch usage, which has been deprecated in Fedora 38

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-5
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-4
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-3
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Tue May 19 2020 - Devrim Gündüz <devrim@gunduz.org> 1.4.0-2
- Provide versionless multicorn. This will simplify using
  bigquery_fdw package.

* Sat Mar 21 2020 - Devrim Gündüz <devrim@gunduz.org> 1.4.0-1
- Update to 1.4.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.3.5-1.1
- Rebuild against PostgreSQL 11.0

* Fri Jan 12 2018 - Devrim Gündüz <devrim@gunduz.org> 1.3.5-1
- Update to 1.3.5, per #2888 .

* Tue Nov 21 2017 - Devrim Gündüz <devrim@gunduz.org> 1.3.4-1
- Update to 1.3.4, per #2888 .

* Mon Mar 6 2017 - Devrim Gündüz <devrim@gunduz.org> 1.3.3-1
- Update to 1.3.3, per #2224 .

* Thu Mar 3 2016 - Devrim Gündüz <devrim@gunduz.org> 1.3.2-1
- Update to 1.3.2

* Mon Jan 18 2016 - Devrim Gündüz <devrim@gunduz.org> 1.3.1-1
- Update to 1.3.1

* Thu Dec 10 2015 - Devrim Gündüz <devrim@gunduz.org> 1.2.4-1
- Update to 1.2.4

* Wed Jan 21 2015 - Devrim Gündüz <devrim@gunduz.org> 1.2.3-1
- Initial packaging for PostgreSQL RPM Repository
