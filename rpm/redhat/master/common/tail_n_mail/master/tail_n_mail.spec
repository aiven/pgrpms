Summary:	Check Log Files and Mail Related Parties
Name:		tail_n_mail
Version:	3.3.0
Release:	1%{?dist}
License:	BSD
Source0:	https://github.com/bucardo/%{name}/archive/%{version}.tar.gz
URL:		https://github.com/bucardo/tail_n_mail
BuildArch:	noarch

%description
tail_n_mail (sometimes abbreviated TNM or tnm) is a Perl script for
automatically detecting interesting items that appear in log files
and mailing them out to interested parties. It is primarily aimed
at Postgres log files but can be used for any files. It was developed
at End Point Corporation by Greg Sabino Mullane.

%prep
%setup -q

%build

%install
%{__rm} -rf %{buildroot}

%{__install} -d -m 755 %{buildroot}%{_bindir}
%{__install} -d -m 755 %{buildroot}%{_docdir}/%{name}

%{__install} -m 755 %{name} %{buildroot}%{_bindir}/%{name}
ln -s %{_bindir}/%{name} %{buildroot}/%{_bindir}/%{name}.pl
%{__install} -m 644 README.md %{buildroot}%{_docdir}/%{name}/

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/%{name}*
%attr(644,root,root) %{_docdir}/%{name}/README.md

%changelog
* Wed Mar 10 2021 Devrim Gündüz <devrim@gunduz.org> - 3.3.0-1
- Update to 3.3.0

* Wed Aug 19 2020 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-1
- Update to 3.0.0

* Tue Feb 4 2020 Devrim Gündüz <devrim@gunduz.org> - 2.7.0-1
- Update to 2.7.0

* Thu Aug 22 2019 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-1
- Update to 2.4.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.3.1-2.1
- Rebuild against PostgreSQL 11.0

* Sun Aug 5 2018 - Devrim Gündüz <devrim@gunduz.org> 2.3.1-2
- Fix packaging errors, per #3531.

* Fri Jul 13 2018 - Devrim Gündüz <devrim@gunduz.org> 2.3.1-1
- Update to 2.3.1, per #3490.

* Tue Dec 12 2017 - Devrim Gündüz <devrim@gunduz.org> 1.31.3-1
- Update to 1.31.3

* Wed Dec 11 2013 - Devrim Gündüz <devrim@gunduz.org> 1.26.3-1
- Update to 1.26.3

* Thu Sep 6 2012 - Devrim Gündüz <devrim@gunduz.org> 1.26.1-1
- Update to 1.26.1

* Fri Jul 27 2012 - Devrim Gündüz <devrim@gunduz.org> 1.26.0-1
- Update to 1.26.0

* Mon Oct 03 2011 - Devrim Gündüz <devrim@gunduz.org> 1.20.3-1
- Update to 1.20.3

* Mon Jan 10 2011 - Devrim Gündüz <devrim@gunduz.org> 1.17-4-1
- Update to 1.17.4

* Sat Nov 13 2010 - Devrim Gündüz <devrim@gunduz.org> 1.17-2-1
- Update to 1.17.2

* Fri Sep 17 2010 - Devrim Gündüz <devrim@gunduz.org> 1.16.5-1
- Update to 1.16.5
- Apply a few stylistic fixes.
- Update download URL.

* Sat Sep 11 2010 - Devrim Gündüz <devrim@gunduz.org> 1.16.3-1
- Update to 1.16.3
- Update README.

* Sat May 15 2010 - Devrim Gündüz <devrim@gunduz.org> 1.10.3-1
- Update to 1.10.3

* Tue Apr 27 2010 - Devrim Gündüz <devrim@gunduz.org> 1.9.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
