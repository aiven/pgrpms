Summary:	a unix pager optimized for psql
Name:		pspg
Version:	5.1.3
Release:	1%{?dist}
License:	BSD
URL:		https://github.com/okbob/%{name}
Source:		https://github.com/okbob/%{name}/archive/%{version}.tar.gz
BuildRequires:	ncurses-devel readline-devel
Requires:	ncurses readline

%description
pspg is a unix pager optimized for psql. It can freeze rows, freeze
columns, and lot of color themes are included.

%prep
%setup -q

%build
CFLAGS="%{optflags} -I/usr/include/ncurses/"
%configure
%{__make} %{_smp_mflags} \
	prefix=%{_prefix} \
	all

%install
%{__rm} -rf %{buildroot}
%{__make} %{_smp_mflags} DESTDIR=%{buildroot} \
	prefix=%{_prefix} bindir=%{_bindir} mandir=%{_mandir} \
	install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{_bindir}/*

%changelog
* Mon Jul 26 2021 Devrim Gündüz <devrim@gunduz.org> - 5.1.3-1
- Update to 5.1.3

* Mon Jul 5 2021 Devrim Gündüz <devrim@gunduz.org> - 5.0.5-1
- Update to 5.0.5

* Mon Jun 21 2021 Devrim Gündüz <devrim@gunduz.org> - 5.0.4-1
- Update to 5.0.4

* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> - 5.0.2-1
- Update to 5.0.2
- Remove RHEL 6 stuff.

* Wed Apr 28 2021 Devrim Gündüz <devrim@gunduz.org> - 4.6.3-1
- Update to 4.6.3

* Fri Apr 23 2021 Devrim Gündüz <devrim@gunduz.org> - 4.6.1-1
- Update to 4.6.1

* Mon Apr 19 2021 Devrim Gündüz <devrim@gunduz.org> - 4.6.0-1
- Update to 4.6.0

* Sun Mar 28 2021 Devrim Gündüz <devrim@gunduz.org> - 4.5.0-1
- Update to 4.5.0

* Sun Mar 21 2021 Devrim Gündüz <devrim@gunduz.org> - 4.4.0-1
- Update to 4.4.0

* Thu Mar 11 2021 Devrim Gündüz <devrim@gunduz.org> - 4.3.1-1
- Update to 4.3.1

* Tue Feb 9 2021 Devrim Gündüz <devrim@gunduz.org> - 4.2.1-1
- Update to 4.2.1

* Fri Feb 5 2021 Devrim Gündüz <devrim@gunduz.org> - 4.1.0-1
- Update to 4.1.0

* Tue Oct 20 2020 Devrim Gündüz <devrim@gunduz.org> - 3.1.5-1
- Update to 3.1.5

* Thu Sep 17 2020 Devrim Gündüz <devrim@gunduz.org> - 3.1.4-1
- Update to 3.1.4

* Fri Aug 28 2020 Devrim Gündüz <devrim@gunduz.org> - 3.1.3-1
- Update to 3.1.3

* Wed Jul 29 2020 Devrim Gündüz <devrim@gunduz.org> - 3.1.2-1
- Update to 3.1.2

* Wed May 13 2020 Devrim Gündüz <devrim@gunduz.org> - 3.0.7-1
- Update to 3.0.7

* Fri Mar 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.7.0-1
- Update to 2.7.0

* Fri Jan 31 2020 Devrim Gündüz <devrim@gunduz.org> - 2.6.6-1
- Update to 2.6.6

* Thu Nov 21 2019 Devrim Gündüz <devrim@gunduz.org> - 2.5.5-1
- Update to 2.5.5

* Fri Oct 18 2019 Devrim Gündüz <devrim@gunduz.org> - 2.1.8-1
- Update to 2.1.8

* Tue Oct 15 2019 Devrim Gündüz <devrim@gunduz.org> - 2.1.7-1
- Update to 2.1.7

* Fri Sep 13 2019 Devrim Gündüz <devrim@gunduz.org> - 2.0.3-1
- Update to 2.0.3

* Mon Sep 9 2019 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-1
- Update to 2.0.1

* Sun Sep 1 2019 Devrim Gündüz <devrim@gunduz.org> - 1.7.1-1
- Update to 1.7.1

* Sun Aug 11 2019 Devrim Gündüz <devrim@gunduz.org> - 1.6.8-1
- Update to 1.6.8

* Wed Jul 24 2019 Devrim Gündüz <devrim@gunduz.org> - 1.6.6-1
- Update to 1.6.6

* Tue Apr 16 2019 Devrim Gündüz <devrim@gunduz.org> - 1.6.5-1
- Update to 1.6.5

* Sun Mar 24 2019 Devrim Gündüz <devrim@gunduz.org> - 1.6.4-1
- Update to 1.6.4

* Thu Nov 29 2018 Devrim Gündüz <devrim@gunduz.org> - 1.6.3-1
- Update to 1.6.3

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.6.1-1.1
- Rebuild against PostgreSQL 11.0

* Fri Sep 7 2018 Devrim Gündüz <devrim@gunduz.org> 1.6.1-1
- Update to 1.6.1, per #3626

* Thu Aug 23 2018 Devrim Gündüz <devrim@gunduz.org> 1.3.0-1
- Update to 1.3.0

* Fri Jul 27 2018 Devrim Gündüz <devrim@gunduz.org> 1.2.2-1
- Update to 1.2.2, per #3517

* Tue May 1 2018 Devrim Gündüz <devrim@gunduz.org> 1.1.1-1
- Update to 1.1.1, per #3315 ( RHEL 7 only)

* Sun Apr 29 2018 Devrim Gündüz <devrim@gunduz.org> 1.1.0-1
- Update to 1.1.0, per #3315

* Fri Mar 16 2018 Devrim Gündüz <devrim@gunduz.org> 1.0.0-1
- Update to 1.0.0, per #3210

* Mon Feb 12 2018 Devrim Gündüz <devrim@gunduz.org> 0.9.3-1
- Update to 0.9.3, per #3102.

* Fri Jan 12 2018 Devrim Gündüz <devrim@gunduz.org> 0.9.2-1
- Update to 0.9.2, per #3006 .

* Mon Dec 4 2017 Devrim Gündüz <devrim@gunduz.org> 0.7.5-1
- Update to 0.7.5, per #2932 .

* Sun Nov 26 2017 Devrim Gündüz <devrim@gunduz.org> 0.7.2-1
- Update to 0.7.2, per #2912.

* Fri Nov 17 2017 Devrim Gündüz <devrim@gunduz.org> 0.5-1
- Update to 0.5

* Fri Sep 15 2017 Devrim Gündüz <devrim@gunduz.org> 0.1-1
- Initial packaging for PostgreSQL RPM repository, based on the spec
  file written by Pavel. Fixes #2704
