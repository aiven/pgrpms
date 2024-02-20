%{?!python_module:%define python_module() python3-%{**}}
Name:		python3-brotlipy
Version:	0.7.0
Release:	1PGDG%{dist}
Summary:	Python binding to the Brotli library
License:	MIT
URL:		https://github.com/python-hyper/brotlipy
Source0:	https://files.pythonhosted.org/packages/source/b/brotlipy/brotlipy-%{version}.tar.gz
Patch0:		merged_pr_94.patch
Patch1:		pr_154-brotli-v1.patch
BuildRequires:	%{python_module cffi >= 1.0.0}
BuildRequires:	%{python_module devel} %{python_module hypothesis}
BuildRequires:	%{python_module setuptools}
BuildRequires:	fdupes libbrotli-devel python-rpm-macros
Requires:	python3-cffi >= 1.0.0

%python_subpackages

%description
This library contains Python bindings for the reference Brotli
encoder/decoder.
This allows Python software to use the Brotli compression algorithm
directly from Python code.

%prep
%setup -q -n brotlipy-%{version}
%autopatch -p1
# Remove unnecessary dependency on stdc++
# See https://github.com/python-hyper/brotlipy/pull/151
sed -i 's/libraries.append.*stdc++.*$/pass/' src/brotli/build.py

%build
export CFLAGS="%{optflags}"
export USE_SHARED_BROTLI=1
%python3_build

%install
%python3_install
%{python_expand rm -f %{buildroot}%{$python_sitearch}/brotli/build.py* %{buildroot}%{$python_sitearch}/brotli/__pycache__/build.*
%fdupes %{buildroot}%{$python_sitearch}
}

%files %{python_files}
%license LICENSE
%doc README.rst
%{python3_sitearch}/brotli
%{python3_sitearch}/brotlipy-%{version}-py*.egg-info

%changelog
* Tue Feb 20 2024 Devrim Gündüz <devrim@gunduz.org> - 0.7.0-1PGDG
- Initial packaging for PostgreSQL RPM repository to support pg_statviz
  dependency on SLES 15. Took spec file from SuSE and cleaned up for us.

