%global	sname	pg_strom
%global __cuda_path	/usr/local/cuda
%global __systemd_conf	%{_sysconfdir}/systemd/system/postgresql-%%{pgmajorversion}.service.d/%{sname}.conf

Name:		%{sname}_%{pgmajorversion}
Version:	2.3
Release:	2%{?dist}
Summary:	PG-Strom extension module for PostgreSQL
License:	GPL 2.0
URL:		https://github.com/heterodb/pg-strom
Source0:	https://github.com/heterodb/pg-strom/archive/v%{version}.tar.gz
Source1:	systemd-%{sname}.conf
BuildRequires:	postgresql%{pgmajorversion}
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	cuda >= 11
Requires:	nvidia-kmod
Requires:	cuda >= 11
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

%package test
Summary:	PG-Strom related test tools and scripts
Requires:	%{sname}-%{pgmajorversion}

%description test
This package provides test tools and scripts related to PG-Strom

%prep
%setup -q -n pg-strom-%{version}

%build
%{__make} -j 8 CUDA_PATH=%{__cuda_path} PG_CONFIG=%{pginstdir}/bin/pg_config

%install
%{__rm} -rf %{buildroot}
%{__make} CUDA_PATH=%{__cuda_path} PG_CONFIG=%{pginstdir}/bin/pg_config DESTDIR=%{buildroot} install
%{__install} -Dpm 644 %{SOURCE1} %{buildroot}/%{__systemd_conf}

%clean
%{__rm} -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE README.md

%{pginstdir}/lib/%{sname}.so
%{pginstdir}/bin/gpuinfo
%{pginstdir}/bin/pg2arrow
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/%{sname}/*
%config %{__systemd_conf}
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
  %endif
 %endif
%endif

%files test
%{pginstdir}/bin/dbgen-ssbm

%changelog
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.3-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Mon Jun 15 2020 Devrim Gündüz <devrim@gunduz.org> - 2.3-1
- Update to 2.3
- Use Cuda 11

* Thu Dec 19 2019 Devrim Gündüz <devrim@gunduz.org> - 2.2-2
- Initial packaging for the PostgreSQL RPM repository,
  based on KaiGai's spec file
