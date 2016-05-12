%global pgmajorversion 96
%global pginstdir /usr/pgsql-9.6
%global sname pg_top

Summary:	'top' for PostgreSQL process
Name:		%{sname}%{pgmajorversion}
Version:	3.7.0
Release:	4%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/markwkm/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/markwkm/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel, libtermcap-devel, systemtap-sdt-devel
BuildRequires:	autoconf
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Obsoletes:	ptop => 3.5.0

%description
pg_top is 'top' for PostgreSQL processes. See running queries,
query plans, issued locks, and table and index statistics.

%prep
%setup -q -n %{sname}-%{version}

%build
sh autogen.sh
PG_CONFIG=%{pginstdir}/bin/pg_config ./configure --prefix=%{pginstdir}
make %{?_smp_mflags} CFLAGS="%{optflags}"

%install
%{__rm} -rf %{buildroot}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%post
%{_sbindir}/update-alternatives --install /usr/bin/pg_top%{pgmajorversion} pg_top %{_bindir}/bin/pg_top %{pgmajorversion}0
%{_sbindir}/update-alternatives --install /usr/share/man/man1/pg_top.1 pg_topman %{pginstdir}/share/man/man1/pg_top.1 %{pgmajorversion}0

%postun
unlink %{_bindir}/%{sname}

%preun
%{_sbindir}/update-alternatives --remove pg_top %{pginstdir}/bin/%{sname}
%{_sbindir}/update-alternatives --remove pg_topman  %{pginstdir}/share/man/man1/pg_top.1

%files
%defattr(-,root,root,-)
%doc FAQ README
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%{pginstdir}/bin/pg_top
%{pginstdir}/share/man/man1/pg_top.1

%changelog
* Tue Jan 26 2016 - Devrim Gündüz <devrim@gunduz.org> 3.7.0-4
- Cosmetic updates, and simplify %%doc section.

* Thu Mar 26 2015 - Devrim GUNDUZ <devrim@gunduz.org> 3.7.0-3
- Fix alternatives path and version.

* Thu Mar 26 2015 - Devrim GUNDUZ <devrim@gunduz.org> 3.7.0-2
- Update URLs: Project moved to github.
- pg_top now requires autoconf for build.

* Tue Sep 17 2013 - Devrim GUNDUZ <devrim@gunduz.org> 3.7.0-1
- Update to 3.7.0
- Remove patch2, now in upstream.
- Remove patch1, new GCC's do not like it.

* Mon Jan 17 2011 - Devrim GUNDUZ <devrim@gunduz.org> 3.6.2-3
- Port a few fixes from EPEL:
 * Fix display of cumulative statistics (BZ#525763)
 * include %%{optflags} during compilation.
 * include DOC files, including license file
 * fix %%defattr

* Thu Nov 11 2010 - Devrim GUNDUZ <devrim@gunduz.org> 3.6.2-2
- Apply changes for PostgreSQL 9.0 RPM layout

* Thu May 15 2008 - Devrim GUNDUZ <devrim@gunduz.org> 3.6.2-1
- Update to 3.6.2

* Sat Apr 12 2008 - Devrim GUNDUZ <devrim@gunduz.org> 3.6.2-0.1.beta3
- Rename to pg_top
- Update to 3.6.2 beta3

* Mon Mar 10 2008 - Devrim GUNDUZ <devrim@gunduz.org> 3.6.1-1
- Update to 3.6.1

* Sun Jan 20 2008 - Devrim GUNDUZ <devrim@gunduz.org> 3.6.1-1.beta3
- Update to 3.6.1-beta3

* Thu Dec 13 2007 - Devrim GUNDUZ <devrim@gunduz.org> 3.6.1-1.beta2
- Initial RPM packaging for Fedora
