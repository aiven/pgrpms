%global sname psycopg2
%global pname python-%{sname}

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

%{!?with_docs:%global with_docs 0}

%global with_python3 1

%if  0%{?rhel} && 0%{?rhel} <= 8 || 0%{?fedora} < 31
%global with_python2 1
%endif
%if  0%{?rhel} && 0%{?rhel} >= 9 || 0%{?fedora} >= 31 || 0%{?suse_version} >= 1315
%global with_python2 0
%endif

%global	python3_runtimes python3
%{expand: %%global py3ver %(python3 -c 'import sys;print(sys.version[0:3])')}

%if 0%{?with_python2}
 %global python2_runtimes python2
%endif

%if 0%{?with_python2}
 %{expand: %%global pyver %(python2 -c 'import sys;print(sys.version[0:3])')}
 # The python2_sitearch is already defined on RHEL 8 and Fedora, so set this on RHEL 6 and 7:
 %if  0%{?rhel} && 0%{?rhel} <= 7
  # Python major version.
  %{!?python2_sitearch: %global python2_sitearch %(python2 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
 %endif
%endif

Summary:	A PostgreSQL database adapter for Python 3
Name:		python3-%{sname}
Version:	2.8.6
Release:	1%{?dist}
# The exceptions allow linking to OpenSSL and PostgreSQL's libpq
License:	LGPLv3+ with exceptions
Url:		http://initd.org/psycopg/
Source0:	http://initd.org/psycopg/tarballs/PSYCOPG-2-8/psycopg2-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
BuildRequires:	python3-devel

%if 0%{?with_python2}
BuildRequires:	python2-devel
%endif

Requires:	libpq5 >= 10.0

Conflicts:	python-%{sname}-zope < %{version}

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
Psycopg is the most popular PostgreSQL adapter for the Python
programming language. At its core it fully implements the Python DB
API 2.0 specifications. Several extensions allow access to many of the
features offered by PostgreSQL.

%package -n python3-%{sname}-tests
Summary:	A testsuite for Python 3
Requires:	python3-%sname = %version-%release

%description -n python3-%{sname}-tests
This sub-package delivers set of tests for the adapter.

%if 0%{?with_python2}
%package -n python2-%{sname}
Summary:	A PostgreSQL database adapter for Python 2
Provides:	python-%{sname} = %{version}-%{release}
Requires:	postgresql-libs

%description -n python2-%{sname}
Psycopg is the most popular PostgreSQL adapter for the Python
programming language. At its core it fully implements the Python DB
API 2.0 specifications. Several extensions allow access to many of the
features offered by PostgreSQL.

This is a build of the psycopg PostgreSQL database adapter for Python 2.

%package -n python2-%{sname}-tests
Summary:	A testsuite for Python 2
Requires:	%{name} = %{version}-%{release}
Provides:	python-%{sname}-tests = %{version}-%{release}
Obsoletes:	python-%{sname}-tests <= 2.0.0

%description -n python2-%{sname}-tests
This sub-package delivers set of tests for the adapter.
%endif

%if %with_docs
%package doc
Summary:	Documentation for psycopg python PostgreSQL database adapter
Requires:	%{name} = %{version}-%{release}
Obsoletes:	python-%{sname}-doc >= 2.0.0
Provides:	python-%{sname}-doc = %{version}-%{release}

%description doc
Documentation and example files for the psycopg python PostgreSQL
database adapter.
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

export PATH=%{pginstdir}/bin:$PATH
# Change /usr/bin/python to /usr/bin/python2 in the scripts:
for i in `find . -iname "*.py"`; do sed -i "s/\/usr\/bin\/env python/\/usr\/bin\/env python2/g" $i; done

for python in %{python3_runtimes} ; do
  $python setup.py build

done
%if 0%{?with_python2}
for python in %{python2_runtimes} ; do
  $python setup.py build
done
%endif

%if %with_docs
# Fix for wrong-file-end-of-line-encoding problem; upstream also must fix this.
for i in `find doc -iname "*.html"`; do sed -i 's/\r//' $i; done
for i in `find doc -iname "*.css"`; do sed -i 's/\r//' $i; done

# Get rid of a "hidden" file that rpmlint complains about
%{__rm} -f doc/html/.buildinfo
%endif

%install
export PATH=%{pginstdir}/bin:$PATH
for python in %{python3_runtimes} ; do
  $python setup.py install --no-compile --root %{buildroot}
done
%if 0%{?with_python2}
for python in %{python2_runtimes} ; do
  $python setup.py install --no-compile --root %{buildroot}
done
%endif

# Copy tests directory:
%{__mkdir} -p %{buildroot}%{python3_sitearch}/%{sname}/
%{__cp} -rp tests %{buildroot}%{python3_sitearch}/%{sname}/tests
# This test is skipped on 3.7 and has a syntax error so brp-python-bytecompile would choke on it
%{__rm} -f %{buildroot}%{python3_sitearch}/%{sname}/tests/test_async_keyword.py
%if 0%{?with_python2}
%{__mkdir} -p %{buildroot}%{python2_sitearch}/%{sname}/
%{__cp} -rp tests %{buildroot}%{python2_sitearch}/%{sname}/tests
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS LICENSE NEWS README.rst
%dir %{python3_sitearch}/%{sname}
%{python3_sitearch}/%{sname}/*.py
%if ! 0%{?suse_version}
%dir %{python3_sitearch}/%{sname}/__pycache__
%{python3_sitearch}/%{sname}/__pycache__/*.pyc
%endif
%{python3_sitearch}/%{sname}-%{version}-py%{py3ver}.egg-info
%{python3_sitearch}/%{sname}/_psycopg.cpython-3?*.so

%files -n python3-%{sname}-tests
%{python3_sitearch}/%{sname}/tests

%if 0%{?with_python2}
%files -n python2-%{sname}
%defattr(-,root,root)
%doc AUTHORS LICENSE NEWS README.rst
%dir %{python2_sitearch}/%{sname}
%{python2_sitearch}/%{sname}/*.py
 %{python2_sitearch}/%{sname}/_psycopg.so
%if ! 0%{?suse_version}
%{python2_sitearch}/%{sname}/*.pyc
%{python2_sitearch}/%{sname}/*.pyo
%endif
%{python2_sitearch}/%{sname}-%{version}-py%{pyver}.egg-info

%files -n python2-%{sname}-tests
%{python2_sitearch}/%{sname}/tests
%endif

%if %with_docs
%files doc
%defattr(-,root,root)
%doc doc
%endif

%changelog
* Mon Sep 7 2020 Devrim Gündüz <devrim@gunduz.org> - 2.8.6-1
- Update to 2.8.6

* Thu Aug 13 2020 Devrim Gündüz <devrim@gunduz.org> - 2.8.5-4
- Use the path provided by the "common" makefile. This package
  now goes to common directory.

* Wed May 13 2020 Devrim Gündüz <devrim@gunduz.org> - 2.8.5-3
- Depend on "libpq5", which is now provided by the latest
  PostgreSQL 10+ minor update set.

* Mon May 11 2020 Devrim Gündüz <devrim@gunduz.org> - 2.8.5-2
- Let python2-psycopg2 provide python-psycopg2. Per
  https://redmine.postgresql.org/issues/5491

* Mon Apr 6 2020 Devrim Gündüz <devrim@gunduz.org> - 2.8.5-1
- Update to 2.8.5

* Mon Oct 28 2019 Devrim Gündüz <devrim@gunduz.org> - 2.8.3-5
- Fix SLES 12 builds. Patch from Talha Bin Rizwan.

* Mon Oct 28 2019 Devrim Gündüz <devrim@gunduz.org> - 2.8.3-4
- Make PY3 package the default one, so that we can build this
  package easier on Fedora 31+ (and RHEL 9+)
- Remove SLES bits

* Wed Oct 16 2019 Devrim Gündüz <devrim@gunduz.org> - 2.8.3-3
- Add PY3 support to RHEL 7 package
- Get rid of -debug subpackage

* Tue Oct 1 2019 Devrim Gündüz <devrim@gunduz.org> - 2.8.3-2
- Rebuilt
- Require versionless -libs subpackage. Fixes
  https://redmine.postgresql.org/issues/4798
  https://redmine.postgresql.org/issues/4799

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 2.8.3-1.1
- Rebuild for PostgreSQL 12

* Fri Jun 28 2019 Devrim Gündüz <devrim@gunduz.org> - 2.8.3-1
- Update to 2.8.3

* Fri May 24 2019 Devrim Gündüz <devrim@gunduz.org> - 2.8.2-2
- Fix conflict with existing packages, per
  https://redmine.postgresql.org/issues/4287

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.8.2-1
- Update to 2.8.2
- Disable -doc subpackage for now. We need sphinx to build the docs,
  and I will defer it until 2.8.2 is out.
- Change main package name from python-psycopg2 to python2-psycopg2,
  in order to distinguish py2 and py3 packages. Also provide old package
  name in order not to break upgrades. Also invent pname macro, which
  stands for "provides name" (I was lazy to rename patches)
- Switch to python2_sitearch macro.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.7.5-1.1
- Rebuild against PostgreSQL 11.0

* Mon Jun 18 2018 Devrim Gündüz <devrim@gunduz.org> 2.7.5-1
- Update to 2.7.5 per
  http://www.psycopg.org/psycopg/articles/2018/06/17/psycopg-275-released/
- Change python to python2, to supress warning on Fedora 28+.

* Fri Feb 9 2018 Devrim Gündüz <devrim@gunduz.org> 2.7.4-1
- Update to 2.7.4 per
  http://www.psycopg.org/psycopg/articles/2018/02/08/psycopg-274-released/

* Sun Dec 10 2017 Devrim Gündüz <devrim@gunduz.org> 2.7.3.2-1
- Update to 2.7.3.2, per
  http://initd.org/psycopg/articles/2017/10/24/psycopg-2732-released/
- Add -tests subpackages.

* Mon Jul 24 2017 Devrim Gündüz <devrim@gunduz.org> 2.7.3-1
- Update to 2.7.3

* Tue Mar 14 2017 Devrim Gündüz <devrim@gunduz.org> 2.7.1-1
- Update to 2.7.1

* Sun Mar 05 2017 Devrim Gündüz <devrim@gunduz.org> 2.7-1
- Update to 2.7, per #2223.

* Fri Feb 24 2017 Devrim Gündüz <devrim@gunduz.org> 2.7b2-1
- Update to 2.7 beta 2

* Fri Oct 7 2016 Devrim Gündüz <devrim@gunduz.org> 2.6.2-3
- Move one .so file into python3-psycopg2 subpackage, per report
  from Oskari Saarenmaa.
- Fix RHEL 6 builds, with custom conditionals.
- Add BR for Python 2.7 environments.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> 2.6.2-2
- Move python-debug (PY2 version) package into non-py3 builds.
  We need this at least for pgadmin4.

* Thu Jul 7 2016 Devrim Gündüz <devrim@gunduz.org> 2.6.2-1
- Update to 2.6.2, per changes described at:
  http://www.psycopg.org/psycopg/articles/2016/07/07/psycopg-262-released/

* Thu Jan 21 2016 Devrim Gündüz <devrim@gunduz.org> 2.6.1-1
- Update to 2.6.1
- Create unified spec file for all distros.
- Remove Zope subpackage.
- Minor spec file cleanups

* Mon Feb 9 2015 Devrim Gündüz <devrim@gunduz.org> 2.6-1
- Update to 2.6, per changes described at:
  http://www.psycopg.org/psycopg/articles/2015/02/09/psycopg-26-and-255-released/
- Trim changelog
- Merge some changes from Fedora spec file.
