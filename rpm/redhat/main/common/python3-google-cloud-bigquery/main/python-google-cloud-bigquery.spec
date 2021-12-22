%global library google-cloud-bigquery

Name:		python3-%{library}
Version:	1.24.0
Release:	1%{?dist}
Epoch:		1
Summary:	Google Cloud Client Library for Python
License:	ASL 2.0
URL:		https://github.com/googleapis/google-cloud-python

Source0:	https://github.com/googleapis/google-cloud-python/archive/bigquery-1.24.0.tar.gz

BuildArch:	noarch

%description
Google Cloud Python Client

BuildRequires:	python3-devel python3-setuptools

%prep
%autosetup -n google-cloud-python-bigquery-%{version}

%build
pushd bigquery
%py3_build
popd

%install
pushd bigquery
%py3_install
popd

%check

%files
%license LICENSE
%{python3_sitelib}/google/cloud/bigquery
%{python3_sitelib}/google/cloud/bigquery_v2
%{python3_sitelib}/google_cloud_bigquery-%{version}*.egg-info
%{python3_sitelib}/google_cloud_bigquery-%{version}*.pth

%changelog
* Mon May 18 2020 Devrim Gündüz <devrim@gunduz.org> - 1.24.0-1
- Initial packaging for PostgreSQL RPM repository to satisfy
  bigquery_fdw dependency.
