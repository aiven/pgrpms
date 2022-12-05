%global sname pg_top

Summary:	'top' for PostgreSQL process
Name:		%{sname}_%{pgmajorversion}
Version:	3.7.0
Release:	9%{?dist}
License:	BSD
Source0:	https://github.com/markwkm/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/markwkm/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel ncurses-devel
BuildRequires:	systemtap-sdt-devel
BuildRequires:	autoconf pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server
Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

Obsoletes:	%{sname}%{pgmajorversion} < 3.7.0-6

%description
pg_top is 'top' for PostgreSQL processes. See running queries,
query plans, issued locks, and table and index statistics.

%prep
%setup -q -n %{sname}-%{version}

%build
sh autogen.sh
PG_CONFIG=%{pginstdir}/bin/pg_config ./configure \
%ifarch ppc64 ppc64le
	--build=power \
%endif
	--prefix=%{pginstdir}
%{__make} %{?_smp_mflags} CFLAGS="%{optflags}"

%install
%{__rm} -rf %{buildroot}
%{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%post
%{_sbindir}/update-alternatives --install /usr/bin/pg_top pg_top %{pginstdir}/bin/%{sname} %{pgmajorversion}0
%{_sbindir}/update-alternatives --install /usr/share/man/man1/pg_top.1 pg_topman %{pginstdir}/share/man/man1/pg_top.1 %{pgmajorversion}0

# Drop alternatives entries for common binaries and man files
%postun
if [ "$1" -eq 0 ]
then
      	# Only remove these links if the package is completely removed from the system (vs.just being upgraded)
	%{_sbindir}/update-alternatives --remove pg_top %{pginstdir}/bin/%{sname}
	%{_sbindir}/update-alternatives --remove pg_topman  %{pginstdir}/share/man/man1/pg_top.1
fi

%files
%defattr(-,root,root,-)
%doc FAQ README
%license LICENSE
%{pginstdir}/bin/pg_top
%{pginstdir}/share/man/man1/pg_top.1

%changelog
* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 3.7.0-9
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Sep 29 2022 Devrim Gündüz <devrim@gunduz.org> - 3.7.0-8
- Remove RHEL 6 support, and remove obsoletes

* Thu Feb 4 2021 John Harvey <john.harvey@crunchydata.com> 3.7.0-7
- Fix Obsoletes

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 3.7.0-6
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 3.7.0-5.2
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 3.7.0-5.1
- Rebuild against PostgreSQL 11.0

* Fri Aug 26 2016 - Devrim Gündüz <devrim@gunduz.org> 3.7.0-5
- Fix alternatives link, per report from  Dmitriy Sarafannikov.
  Fixes #1604.

* Tue Jan 26 2016 - Devrim Gündüz <devrim@gunduz.org> 3.7.0-4
- Cosmetic updates, and simplify %%doc section.

* Thu Mar 26 2015 - Devrim Gündüz <devrim@gunduz.org> 3.7.0-3
- Fix alternatives path and version.

* Thu Mar 26 2015 - Devrim Gündüz <devrim@gunduz.org> 3.7.0-2
- Update URLs: Project moved to github.
- pg_top now requires autoconf for build.

* Tue Sep 17 2013 - Devrim Gündüz <devrim@gunduz.org> 3.7.0-1
- Update to 3.7.0
- Remove patch2, now in upstream.
- Remove patch1, new GCC's do not like it.

* Mon Jan 17 2011 - Devrim Gündüz <devrim@gunduz.org> 3.6.2-3
- Port a few fixes from EPEL:
 * Fix display of cumulative statistics (BZ#525763)
 * include %%{optflags} during compilation.
 * include DOC files, including license file
 * fix %%defattr

* Thu Nov 11 2010 - Devrim Gündüz <devrim@gunduz.org> 3.6.2-2
- Apply changes for PostgreSQL 9.0 RPM layout

* Thu May 15 2008 - Devrim Gündüz <devrim@gunduz.org> 3.6.2-1
- Update to 3.6.2

* Sat Apr 12 2008 - Devrim Gündüz <devrim@gunduz.org> 3.6.2-0.1.beta3
- Rename to pg_top
- Update to 3.6.2 beta3

* Mon Mar 10 2008 - Devrim Gündüz <devrim@gunduz.org> 3.6.1-1
- Update to 3.6.1

* Sun Jan 20 2008 - Devrim Gündüz <devrim@gunduz.org> 3.6.1-1.beta3
- Update to 3.6.1-beta3

* Thu Dec 13 2007 - Devrim Gündüz <devrim@gunduz.org> 3.6.1-1.beta2
- Initial RPM packaging for Fedora
