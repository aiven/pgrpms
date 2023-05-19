%global	sname	pg_strom
%global __cuda_path	/usr/local/cuda
%global __systemd_conf	%{_sysconfdir}/systemd/system/postgresql-%%{pgmajorversion}.service.d/%{sname}.conf

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	5.0
Release:	alpha1_1%{?dist}
Summary:	PG-Strom extension module for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/heterodb/pg-strom
Source0:	https://github.com/heterodb/pg-strom/archive/v%{version}_alpha1.tar.gz
Source1:	systemd-%{sname}.conf
BuildRequires:	postgresql%{pgmajorversion}
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	cuda-12-0 >= 12
Requires:	nvidia-kmod
Requires:	cuda-12-0 >= 12
Requires:	postgresql%{pgmajorversion}-server
Requires:	/sbin/ldconfig
# for /sbin/ldconfig
Requires(post):		glibc
Requires(postun):	glibc

Obsoletes:	nvme_strom < 2.0
Obsoletes:	%{sname}-%{pgmajorversion} < 2.3-2

%description
PG-Strom is an extension for PostgreSQL, to accelerate analytic queries
towards large data set using the capability of GPU devices.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for XXX
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm13-devel clang13-devel
Requires:	llvm13
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for XXX
%endif

%prep
%setup -q -n pg-strom-%{version}_alpha1

%build
pushd src
%{__make} -j 8 CUDA_PATH=%{__cuda_path} PG_CONFIG=%{pginstdir}/bin/pg_config
popd

%install
%{__rm} -rf %{buildroot}
pushd src
%{__make} CUDA_PATH=%{__cuda_path} PG_CONFIG=%{pginstdir}/bin/pg_config DESTDIR=%{buildroot} install
%{__install} -Dpm 644 %{SOURCE1} %{buildroot}/%{__systemd_conf}
popd

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE README.md

%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/%{sname}/*
%config %{__systemd_conf}

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Fri May 19 2023 Devrim Gündüz <devrim@gunduz.org> - 5.0_alpha1-1
- Update to 5.0 alpha1
- Split llvmjit subpackage

* Mon Apr 24 2023 Devrim Gündüz <devrim@gunduz.org> - 3.5-1
- Update to 3.5

* Wed Jan 4 2023 Devrim Gündüz <devrim@gunduz.org> - 3.4-1
- Update to 3.4

* Thu Dec 16 2021 Devrim Gündüz <devrim@gunduz.org> - 3.3-2-1
- Update to 3.3-2

* Tue Oct 19 2021 Devrim Gündüz <devrim@gunduz.org> - 3.2-1
- Update to 3.2

* Thu Aug 26 2021 Devrim Gündüz <devrim@gunduz.org> - 3.1-1
- Update to 3.1

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.3-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Mon Jun 15 2020 Devrim Gündüz <devrim@gunduz.org> - 2.3-1
- Update to 2.3
- Use Cuda 11

* Thu Dec 19 2019 Devrim Gündüz <devrim@gunduz.org> - 2.2-2
- Initial packaging for the PostgreSQL RPM repository,
  based on KaiGai's spec file
