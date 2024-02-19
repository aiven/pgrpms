%global __ospython %{_bindir}/python3.11

%{expand: %%global pybasever %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%{!?python311_sitearch: %global python311_sitearch %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(2))")}

Name:           python311-humanize
Version:        3.13.1
Release:        42PGDG%{?dist}
Summary:        Turns dates in to human readable format, e.g '3 minutes ago'

License:        MIT
URL:            https://github.com/jmoiron/humanize
Source0:        %{pypi_source humanize}

BuildArch:      noarch
BuildRequires:  python3-devel

%global _description\
This modest package contains various common humanization utilities, like turning\
a number into a fuzzy human readable duration ('3 minutes ago') or into a human\
readable size or throughput.\

%description %_description

%package -n python3-humanize
Summary: %summary

%description -n python3-humanize
This modest package contains various common humanization utilities, like turning
a number into a fuzzy human readable duration ('3 minutes ago') or into a human
readable size or throughput.

%prep
%autosetup -n humanize-%{version}

# Remove shebangs from libs.
for lib in src/humanize/time.py src/humanize/filesize.py src/humanize/number.py; do
 sed '1{\@^#!/usr/bin/env python@d}' $lib > $lib.new &&
 touch -r $lib $lib.new && mv $lib.new $lib
done

# Remove .po files
find -name '*.po' -delete

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files humanize

%files -n python3-humanize -f %{pyproject_files}
%doc README.md

%changelog
* Mon Feb 19 2024 Devrim Gündüz <devrim@gunduz.org> - 3.13.1-42PGDG
- Initial packaging for the PostgreSQL RPM repository to support
  pg_activity dependency on SLES 15.
