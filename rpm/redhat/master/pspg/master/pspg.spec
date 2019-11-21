Summary:	a unix pager optimized for psql
Name:		pspg
Version:	2.5.5
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
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc README.md LICENSE
%else
%license LICENSE
%doc README.md
%endif
%{_bindir}/*

%changelog
* Thu Nov 21 2019 2019 Devrim Gündüz <devrim@gunduz.org> - 2.5.5-1
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
