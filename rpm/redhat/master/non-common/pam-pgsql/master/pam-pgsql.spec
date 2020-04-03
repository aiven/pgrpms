%global sname pam-pgsql

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	PAM module to authenticate using a PostgreSQL database
Name:		%{sname}%{pgmajorversion}
Version:	0.7.3.2
Release:	1%{dist}.1
Source0:	https://github.com/%{sname}/%{sname}/archive/release-%{version}.tar.gz

License:	GPLv2
URL:		https://github.com/%{sname}/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel, pam-devel, mhash-devel
Requires:	postgresql%{pgmajorversion}

Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

Patch1:		%{sname}-getservice.patch

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
This module provides support to authenticate against PostgreSQL
tables for PAM-enabled applications.

%prep
%setup -q -n %{sname}-release-%{version}
%patch1 -p1

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
sh autogen.sh
%configure --with-postgresql=%{pginstdir}/bin/pg_config --prefix=%{pginstdir} --libdir=%{pginstdir}/lib/
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf  %{buildroot}
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf  %{buildroot}

%post
# Create alternatives entries for lib files
%{_sbindir}/update-alternatives --install %{_libdir}/security/pam_pgsql.la %{sname}-la %{pginstdir}/lib/security/pam_pgsql.la %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_libdir}/security/pam_pgsql.so %{sname}-so %{pginstdir}/lib/security/pam_pgsql.so %{pgmajorversion}0
libtool --finish %{pginstdir}/lib/security

%preun
# Drop alternatives entries for lib files
%{_sbindir}/update-alternatives --remove %{sname}-so %{pginstdir}/lib/security/pam_pgsql.so
%{_sbindir}/update-alternatives --remove %{sname}-la %{pginstdir}/lib/security/pam_pgsql.la

%files
%defattr(-,root,root)
%doc %{pginstdir}/share/doc/pam-pgsql/*
%dir %{pginstdir}/lib/security
%{pginstdir}/lib/security/pam_pgsql.la
%{pginstdir}/lib/security/pam_pgsql.so

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.7.3.2-1.1
- Rebuild against PostgreSQL 11.0

* Thu Jan 21 2016 Devrim Gunduz <devrim@gunduz.org> - 0.7.3.2-1
- Update to 0.7.3.2
- Rename package to pam-pgsql, so that it matches the upstream name.
  Not adding conflicts: here, because this package has not been built
  for ages anyway.
- Update URL
- Update description
- Fix rpmlint warning about library path, and use %%libdir macro.
- Fix alternatives section

* Sun Sep 23 2012 Devrim Gunduz <devrim@gunduz.org> - 0.7.3.1-1
- Update to 0.7.3.1

* Tue Oct 12 2010 Devrim Gunduz <devrim@gunduz.org> - 0.7.1-1
- Update to 0.7.1-1
- Apply 9.0 specific changes.

* Sat Jun 14 2008 Devrim Gunduz <devrim@gunduz.org> - 0.6.4-1
- Update to 0.6.4-1

* Sun Feb 3 2008 Devrim Gunduz <devrim@gunduz.org> - 0.6.3-1
- Initial packaging for Fedora
