%global sname pam-pgsql

Summary:	PAM module to authenticate using a PostgreSQL database
Name:		%{sname}_%{pgmajorversion}
Version:	0.7.3.2
Release:	5PGDG%{dist}
Source0:	https://github.com/%{sname}/%{sname}/archive/release-%{version}.tar.gz

License:	GPLv2
URL:		https://github.com/%{sname}/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pam-devel libgcrypt-devel
BuildRequires:	mhash-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}

Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

Patch1:		%{sname}-getservice.patch

Obsoletes:	%{sname}%{pgmajorversion} < 0.7.3.2-2

%description
This module provides support to authenticate against PostgreSQL
tables for PAM-enabled applications.

%prep
%setup -q -n %{sname}-release-%{version}
%patch -P 1 -p1

%build
sh autogen.sh
%configure --with-postgresql=%{pginstdir}/bin/pg_config --prefix=%{pginstdir} --libdir=%{pginstdir}/lib/
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%post
# Create alternatives entries for lib files
%{_sbindir}/update-alternatives --install %{_libdir}/security/pam_pgsql.so %{sname}-so %{pginstdir}/lib/security/pam_pgsql.so %{pgmajorversion}0
libtool --finish %{pginstdir}/lib/security

%preun
# Drop alternatives entries for lib files
%{_sbindir}/update-alternatives --remove %{sname}-so %{pginstdir}/lib/security/pam_pgsql.so

%files
%defattr(-,root,root)
%doc %{pginstdir}/share/doc/pam-pgsql/*
%dir %{pginstdir}/lib/security
%{pginstdir}/lib/security/pam_pgsql.so

%changelog
* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 0.7.3.2-5PGDG
- Cleanup rpmlint warnings
- Add PGDG branding

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 0.7.3.2-4.1
- Modernise %%patch usage, which has been deprecated in Fedora 38

* Sat Apr 22 2023 Devrim Gündüz <devrim@gunduz.org> - 0.7.3.2-4
- Add missing BR, and also remove .la file

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 0.7.3.2-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 0.7.3.2-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

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
