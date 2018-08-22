%global sname	passwordcheck_cracklib
%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Name:		%{sname}%{pgmajorversion}
Version:	1.0.2
Release:	2%{?dist}
Summary:	PostgreSQL passwordcheck extension, built with cracklib.
Group:		Applications/Databases
License:	BSD
URL:		https://github.com/devrimgunduz/%{sname}/
Source0:	https://github.com/devrimgunduz/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	postgresql%{pgmajorversion}

BuildRequires:	cracklib-devel, postgresql%{pgmajorversion}-devel
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
This is the regular PostgreSQL passwordcheck extension, built with cracklib.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{pginstdir}/lib/%{sname}.so
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

%changelog
* Wed Aug 22 2018 - Devrim Gündüz <devrim@gunduz.org> 1.0.2-2
- Add v11 code to spec file

* Tue May 30 2017 - Devrim Gündüz <devrim@gunduz.org> 1.0.2-1
- Initial packaging
