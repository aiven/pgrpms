BuildArch:	noarch
%global sname psycopg3
%global pname python-%{sname}

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

%{!?with_docs:%global with_docs 0}

%if 0%{?fedora} >= 35
%{expand: %%global pyver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global pyver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif
%global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")


Summary:	A PostgreSQL database adapter for Python 3
Name:		python3-%{sname}
Version:	3.0
Release:	3%{?dist}
# The exceptions allow linking to OpenSSL and PostgreSQL's libpq
License:	LGPLv3+ with exceptions
Url:		https://psycopg.org
Source0:	https://github.com/psycopg/psycopg/archive/refs/tags/3.0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
BuildRequires:	python3-devel

Requires:	libpq5 >= 10.0

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

# Enable this package only on Fedora, which has PY 3.9:
%if 0%{?fedora} > 32
%package -n python3-%{sname}-tests
Summary:	A testsuite for Python 3
Requires:	python3-%sname = %version-%release

%description -n python3-%{sname}-tests
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
%setup -q -n psycopg-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

export PATH=%{pginstdir}/bin:$PATH
pushd psycopg
%{__python3} setup.py build
popd

%if %with_docs
# Fix for wrong-file-end-of-line-encoding problem; upstream also must fix this.
for i in `find doc -iname "*.html"`; do sed -i 's/\r//' $i; done
for i in `find doc -iname "*.css"`; do sed -i 's/\r//' $i; done

# Get rid of a "hidden" file that rpmlint complains about
%{__rm} -f doc/html/.buildinfo
%endif

%install
export PATH=%{pginstdir}/bin:$PATH
pushd psycopg
%{__python3} setup.py install --no-compile --root %{buildroot}
popd

%{__mkdir} -p %{buildroot}%{python3_sitearch}/%{sname}/

#Only on Fedora:
%if 0%{?fedora} > 32
# Copy tests directory:
%{__cp} -rp tests %{buildroot}%{python3_sitearch}/%{sname}/tests
# This test is skipped on 3.7 and has a syntax error so brp-python-bytecompile would choke on it
%{__rm} -f %{buildroot}%{python3_sitearch}/%{sname}/tests/test_async_keyword.py
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc  README.rst
%dir %{python3_sitearch}/%{sname}

%{python3_sitelib}/psycopg-3.0-py%{py3ver}.egg-info/*
%{python3_sitelib}/psycopg/*.py
%{python3_sitelib}/psycopg/__pycache__/*.pyc
%{python3_sitelib}/psycopg/pq/*.py*
%{python3_sitelib}/psycopg/pq/__pycache__/*.py*
%{python3_sitelib}/psycopg/types/*.py*
%{python3_sitelib}/psycopg/types/__pycache__/*.py*
%{python3_sitelib}/psycopg/py.typed

#Only on Fedora:
%if 0%{?fedora} > 32
%files -n python3-%{sname}-tests
%{python3_sitearch}/%{sname}/tests
%endif

%if %with_docs
%files doc
%defattr(-,root,root)
%doc doc
%endif

%changelog
* Tue Nov 2 2021 Devrim Gündüz <devrim@gunduz.org> - 3.0-3
- Add Fedora 35 support.

* Wed Oct 13 2021 Devrim Gündüz <devrim@gunduz.org> - 3.0-2
- Disable unit tests on RHEL, because of Python version. Per tip from
  Daniele: https://github.com/psycopg/psycopg/issues/106

* Wed Oct 13 2021 Devrim Gündüz <devrim@gunduz.org> - 3.0-1
- Update to 3.0

* Wed Sep 8 2021 Devrim Gündüz <devrim@gunduz.org> - 3.0-beta1-1
- Initial packaging
