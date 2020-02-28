%global srcname SQLAlchemy
%global sname sqlalchemy

%if 0%{?fedora} > 27 || 0%{?rhel} == 8
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global py3ver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?rhel} == 7
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?with_python3}
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif
Version:	1.3.13
Release:	1%{?dist}
Summary:	Modular and flexible ORM library for python
License:	MIT
URL:		http://www.sqlalchemy.org/
Source0:	https://files.pythonhosted.org/packages/source/S/%{srcname}/%{srcname}-%{version}.tar.gz

%description
SQLAlchemy is an Object Relational Mappper (ORM) that provides a flexible,
high-level interface to SQL databases.  Database and domain concepts are
decoupled, allowing both sides maximum flexibility and power. SQLAlchemy
provides a powerful mapping layer that can work as automatically or as manually
as you choose, determining relationships based on foreign keys or letting you
define the join conditions explicitly, to bridge the gap between database and
domain.

This package includes the python 2 version of the module.

%if 0%{?rhel} == 7
BuildRequires:	python-setuptools pytest python-mock python2-devel
%endif

%if 0%{?fedora} > 25
BuildRequires:	python3-setuptools python3-devel pytest python3-mock
%endif

%if 0%{?rhel} == 8
BuildRequires:	python3-setuptools python3-devel python3-pytest python3-mock
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	python-devel python-mock python-pytest
%endif
%endif

# Filter unnecessary dependencies
%global __provides_exclude_from ^(%{python2_sitearch}|%{python3_sitearch})/.*\\.so$

%prep
%setup -q -n %{srcname}-%{version}

%build
CFLAGS="%{optflags}" %{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}

%{__mkdir} -p %{buildroot}%{python2_sitelib}
%{__ospython} setup.py install --skip-build --root %{buildroot}

# remove unnecessary scripts for building documentation
%{__rm} -rf doc/build

# Move everything under pgadmin4 web/ directory.
%if 0%{?with_python3}
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitearch}/%{sname} %{buildroot}%{python3_sitearch}/*%{srcname}-%{version}*-py%{py3ver}.egg-info %{buildroot}/%{pgadmin4py3instdir}
%else
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitearch}/%{sname} %{buildroot}%{python2_sitearch}/*%{srcname}-%{version}*-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.rst LICENSE PKG-INFO CHANGES doc examples
%if 0%{?with_python3}
%{pgadmin4py3instdir}/*%{srcname}*.egg-info
%{pgadmin4py3instdir}/%{sname}
%else
%{pgadmin4py2instdir}/*%{srcname}*.egg-info
%{pgadmin4py2instdir}/%{sname}
%endif

%changelog
* Fri Feb 28 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.13-1
- Update to 1.3.13

* Thu Apr 18 2019 Devrim Gündüz <devrim@gunduz.org> - 1.2.18-1
- Update to 1.2.18

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.2.5-1.1
- Rebuild against PostgreSQL 11.0

* Tue Apr 10 2018 Devrim Gündüz <devrim@gunduz.org> - 1.2.5-1
- Update to 1.2.5

* Thu Apr 5 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0.14-3
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the dependencies for that.

* Mon Apr 10 2017 Devrim Gündüz <devrim@gunduz.org> - 1.0.14-2
- Move the components under pgadmin web directory, per #2332.

* Mon Apr 10 2017 Devrim Gündüz <devrim@gunduz.org> - 1.0.14-2
- Move the components under pgadmin web directory, per #2332.

* Thu Aug 18 2016 Nils Philippsen <nils@redhat.com> - 1.0.14-1
- version 1.0.14

* Tue May 31 2016 Nils Philippsen <nils@redhat.com> - 1.0.14-1
- fix source URL

* Tue May 17 2016 Nils Philippsen <nils@redhat.com> - 1.0.13-1
- version 1.0.13

* Thu Feb 25 2016 Nils Philippsen <nils@redhat.com> - 1.0.12-1
- version 1.0.12

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 08 2016 Kevin Fenzi <kevin@scrye.com> - 1.0.11-1
- Update to 1.0.11. Fixes bug #1296757

* Sat Dec 12 2015 Kevin Fenzi <kevin@scrye.com> - 1.0.10-1
- Update to 1.0.10. Fixes bug #1290945

* Thu Nov 12 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Oct 21 2015 Nils Philippsen <nils@redhat.com> - 1.0.9-1
- version 1.0.9, upstream feature and bugfix release

* Mon Oct 12 2015 Robert Kuska <rkuska@redhat.com> - 1.0.8-2
- Rebuilt for Python3.5 rebuild

* Fri Jul 24 2015 Nils Philippsen <nils@redhat.com> 1.0.8-1
- version 1.0.8, upstream bugfix release

* Tue Jul 21 2015 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1.0.7-1
- Update to 1.0.7 (#1244991)

* Mon Jun 29 2015 Nils Philippsen <nils@redhat.com> 1.0.6-1
- version 1.0.6, upstream feature and bugfix release

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 07 2015 Kevin Fenzi <kevin@scrye.com> 1.0.4-1
- Update to 1.0.5. Fixes bug #1229067

* Fri May 08 2015 Nils Philippsen <nils@redhat.com> 1.0.4-1
- version 1.0.4, upstream bugfix release

* Sat May 02 2015 Kevin Fenzi <kevin@scrye.com> 1.0.3-1
- Update to 1.0.3. Fixes bug #1217761

* Sat Apr 25 2015 Nils Philippsen <nils@redhat.com> - 1.0.2-1
- version 1.0.2, upstream bugfix release

* Fri Apr 24 2015 Nils Philippsen <nils@redhat.com> - 1.0.1-1
- version 1.0.1, upstream bugfix release

* Fri Apr 17 2015 Nils Philippsen <nils@redhat.com> - 1.0.0-1
- version 1.0.0, upstream feature release

* Fri Apr 10 2015 Nils Philippsen <nils@redhat.com> - 0.9.9-1
- version 0.9.9, upstream feature and bugfix release

* Wed Oct 15 2014 Nils Philippsen <nils@redhat.com> - 0.9.8-1
- version 0.9.8, upstream feature and bugfix release
- avoid using unversioned python macros
- use py.test instead of nose for tests

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 29 2014 Nils Philippsen <nils@redhat.com> - 0.9.7-1
- version 0.9.7, upstream feature and bugfix release

* Mon Jun 30 2014 Nils Philippsen <nils@redhat.com> - 0.9.6-1
- version 0.9.6, upstream feature and bugfix release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 16 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu May 15 2014 Nils Philippsen <nils@redhat.com> - 0.9.4-1
- version 0.9.4, upstream feature and bugfix release

* Thu Feb 20 2014 Nils Philippsen <nils@redhat.com> - 0.9.3-1
- version 0.9.3, upstream feature and bugfix release

* Wed Feb 05 2014 Nils Philippsen <nils@redhat.com> - 0.9.2-1
- version 0.9.2, upstream feature and bugfix release

* Tue Jan 07 2014 Nils Philippsen <nils@redhat.com> - 0.9.1-1
- version 0.9.1, upstream feature and bugfix release
- no need to use 2to3 for python 3.x anymore
- build C extension for python 3.x
- require python2-devel >= 2.6 for building

* Mon Dec 09 2013 Nils Philippsen <nils@redhat.com> - 0.8.4-1
- version 0.8.4, upstream bugfix release

* Tue Oct 29 2013 Nils Philippsen <nils@redhat.com> - 0.8.3-1
- version 0.8.3, upstream bugfix release

* Wed Aug 14 2013 Nils Philippsen <nils@redhat.com> - 0.8.2-1
- version 0.8.2, upstream bugfix release
- drop obsolete sqlalchemy-test-bidirectional-order patch
- fix bogus date in changelog

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 29 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 0.8.1-1
- Upstream bugfix
- Stop calling sa2to3 explicitly on the library.  It seems to break mapper.py's
  import of collections.deque

* Fri Apr 12 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 0.8.0-1
- Final release of 0.8.0
- Fix for a unittest that assumes order in dicts

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-0.2.b1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov  1 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.8.0-0.1.b1
- Update to 0.8.0 beta

* Mon Aug 13 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.7.8-4.20120813hg8535
- Update to a snapshot to fix unittest errors with python-3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 0.7.8-3
- remove rhel logic from with_python3 conditional

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 18 2012 Nils Philippsen <nils@redhat.com> - 0.7.8-1
- Upstream bugfix release

* Tue May 15 2012 Nils Philippsen <nils@redhat.com> - 0.7.7-1
- Upstream bugfix release

* Tue Mar 20 2012 Nils Philippsen <nils@redhat.com> - 0.7.6-1
- Upstream bugfix release

* Mon Jan 30 2012 Nils Philippsen <nils@redhat.com> - 0.7.5-1
- Upstream bugfix release
- package README.rst instead of README as documentation

* Tue Jan 10 2012 Nils Philippsen <nils@redhat.com> - 0.7.3-2
- rebuild for gcc 4.7

* Mon Oct 17 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.7.3-1
- Upstream bugfix release

* Mon Aug 1 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.7.2-1
- Upstream bugfix release

* Mon Jun 06 2011 Nils Philippsen <nils@redhat.com> - 0.7.1-1
- 0.7.1 Upstream release
- no need to fix examples/dynamic_dict/dynamic_dict.py anymore
- use sqla_nose.py to fix %%check

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.6-1
- 0.6.6 Upstream release

* Fri Dec 3 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.5-1
- 0.6.5 Upstream release

* Wed Sep 29 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.4-2
- Filter out the C extensions from provides

* Tue Sep 07 2010 Luke Macken <lmacken@redhat.com> - 0.6.4-1
- 0.6.4 upstream release

* Mon Aug 23 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.3-1
- 0.6.3 upstream release

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com>
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jun 24 2010 Nils Philippsen <nils@redhat.com> - 0.6.1-1
- 0.6.1 upstream release

* Tue Apr 13 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6-0.4.beta3
- Build beta3

* Fri Mar 19 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6-0.3.beta2
- Build beta2 with cextension

* Sun Mar 7 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6-0.2.beta1
- Build python3 package

* Tue Mar 2 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6-0.1.beta1
- 0.6 beta1 upstream release

* Tue Feb 2 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.5.8-3
- One last cleanup

* Tue Feb 2 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.5.8-2
- just some cleanups to older styles of building packages.

* Mon Feb 1 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.5.8-1
- Upstream bugfix release 0.5.8

* Fri Aug 14 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.5.5-2
- Upstream bugfix release 0.5.5

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-2.p2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.5.4-1.p2
- Upstream bugfix release 0.5.4p2.

* Thu Apr 16 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.5.3-1
- Upstream bugfix release.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.5.2-1
- Update to 0.5.2

* Wed Jan 21 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.5.1-1
- Update to 0.5.1.

* Mon Dec 1 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 0.5-0.1.rc4
- Update to 0.5.0rc4 which works with the new pysqlite
- And update test cases to work with the new pysqlite

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.4.7-2
- Rebuild for Python 2.6

* Sun Jul 27 2008 Toshio Kuratomi <toshio@fedoraproject.org> 0.4.7-1
- Update to 0.4.7.

* Sun Jun 1 2008 Toshio Kuratomi <toshio@fedoraproject.org> 0.4.6-1
- Update to 0.4.6.

* Tue Apr 8 2008 Toshio Kuratomi <toshio@fedoraproject.org> 0.4.5-1
- Update to 0.4.5.

* Fri Feb 22 2008 Toshio Kuratomi <toshio@fedoraproject.org> 0.4.3-1
- Update to 0.4.3.

* Tue Dec 11 2007 Toshio Kuratomi <a.badger@gmail.com> 0.4.2-1.p3
- Update to 0.4.2p3.

* Tue Dec 11 2007 Toshio Kuratomi <a.badger@gmail.com> 0.4.1-1
- Update to 0.4.1.

* Wed Oct 17 2007 Toshio Kuratomi <a.badger@gmail.com> 0.4.0-1
- SQLAlchemy-0.4.0 final
- Run the testsuite

* Wed Oct  3 2007 Luke Macken <lmacken@redhat.com> 0.4.0-0.4.beta6
- SQLAlchemy-0.4.0beta6

* Tue Sep 11 2007 Toshio Kuratomi <a.badger@gmail.com> - 0.4.0-0.4.beta5
- Update to 0.4beta5.

* Fri Sep 07 2007 Toshio Kuratomi <a.badger@gmail.com> - 0.4.0-0.4.beta4
- setuptools has been fixed.

* Fri Aug 31 2007 Toshio Kuratomi <a.badger@gmail.com> - 0.4.0-0.3.beta4
- setuptools seems to be broken WRT having an active and inactive version
  of an egg.  Have to make both versions inactive and manually setup a copy
  that can be started via import. (Necessary for the sqlalchemy0.3 compat
  package.)

* Tue Aug 28 2007 Toshio Kuratomi <a.badger@gmail.com> - 0.4.0-0.2.beta4
- Modify setuptools to handle the -devel subpackage split in F-8.

* Mon Aug 27 2007 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.4.0-0.1.beta4
- Update to 0.4 beta4.

* Tue Jul 24 2007 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.3.10-2
- Remove python-abi Requires.  This is automatic since FC4+.

* Tue Jul 24 2007 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.3.10-1
- Update to new upstream version 0.3.10

* Fri Mar 23 2007 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.3.6-1
- Update to new upstream version 0.3.6

* Sat Mar 10 2007 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.3.5-1
- Update to new upstream version 0.3.5
- Simplify the files listing

* Tue Jan 23 2007 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.3.4-2
- Remember to upload the source tarball to the lookaside cache.

* Tue Jan 23 2007 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.3.4-1
- Update to new upstream version 0.3.4

* Mon Jan 01 2007 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.3.3-1
- Update to new upstream version 0.3.3

* Sat Dec 09 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.3.1-2
- Bump and rebuild for python 2.5 on devel.
- BuildRequire: python-devel as a header is missing otherwise.

* Fri Nov 24 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.3.1-1
- Update to new upstream version 0.3.1

* Sat Sep 16 2006 Shahms E. King <shahms@shahms.com> 0.2.7-2
- Rebuild for FC6

* Thu Aug 17 2006 Shahms E. King <shahms@shahms.com> 0.2.7-1
- Update to new upstream version

* Fri Aug 11 2006 Shahms E. King <shahms@shahms.com> 0.2.6-2
- Include, don't ghost .pyo files per new guidelines

* Tue Aug 08 2006 Shahms E. King <shahms@shahms.com> 0.2.6-1
- Update to new upstream version

* Fri Jul 07 2006 Shahms E. King <shahms@shahms.com> 0.2.4-1
- Update to new upstream version

* Mon Jun 26 2006 Shahms E. King <shahms@shahms.com> 0.2.3-1
- Update to new upstream version

* Wed May 31 2006 Shahms E. King <shahms@shahms.com> 0.2.1-1
- Update to new upstream version
