%global debug_package %{nil}
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

%{expand: %%global py3ver %(python3 -c 'import sys;print(sys.version[0:3])')}

Summary:	BigQuery Foreign Data Wrapper for PostgreSQL
Name:		bigquery_fdw
Version:	1.3.2
Release:	1%{?dist}
# The exceptions allow linking to OpenSSL and PostgreSQL's libpq
License:	LGPLv3+ with exceptions
Url:		https://github.com/gabfl/%{name}/
Source0:	https://github.com/gabfl/%{name}/archive/1.3.2.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
BuildRequires:	python3-devel

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
%prep
%setup -q -n %{name}-%{version}

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
# Change /usr/bin/python to /usr/bin/python2 in the scripts:
for i in `find . -iname "*.py"`; do sed -i "s/\/usr\/bin\/env python/\/usr\/bin\/env python3/g" $i; done

python3 setup.py build

%install
python3 setup.py install --no-compile --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc docs/ README.md
%license LICENSE
%{_bindir}/bq_client_test
%{python3_sitelib}/%{name}/*.py
%{python3_sitelib}/%{name}/__pycache__/*.pyc
%dir %{python3_sitelib}/%{name}-%{version}-py%{py3ver}.egg-info
%{python3_sitelib}/%{name}-%{version}-py%{py3ver}.egg-info/*

%changelog
* Mon May 4 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.2-1
- Initial packaging for PostgreSQL YUM repository
