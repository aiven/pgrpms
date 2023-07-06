Name:		pgdg-pyproject-rpm-macros
Summary:	PGDG RPM macros for PEP 517 Python packages
License:	MIT
Version:	1.9.0
Release:	1PGDG%{?dist}
URL:		https://src.fedoraproject.org/rpms/pyproject-rpm-macros
# Macro files
Source001:	macros.pyproject
Source002:	macros.aaa-pyproject-srpm
# Implementation files
Source101:	pyproject_buildrequires.py
Source102:	pyproject_save_files.py
Source103:	pyproject_convert.py
Source104:	pyproject_preprocess_record.py
Source105:	pyproject_construct_toxenv.py
Source106:	pyproject_requirements_txt.py
Source107:	pyproject_wheel.py
# Metadata
Source901:	README.md
Source902:	LICENSE

BuildArch:	noarch

# We build on top of those:
BuildRequires:	python-rpm-macros
BuildRequires:	python-srpm-macros
BuildRequires:	python3-rpm-macros
Requires:	python-rpm-macros
Requires:	python-srpm-macros
Requires:	python3-rpm-macros
Requires:	(pgdg-pyproject-srpm-macros = %{?epoch:%{epoch}:}%{version}-%{release} if pgdg-pyproject-srpm-macros)

# We use the following tools outside of coreutils
Requires:	/usr/bin/find
Requires:	/usr/bin/sed

%description
These macros allow projects that follow the Python packaging specifications
to be packaged as RPMs in the PostgreSQL RPM repository.

They work for:

* traditional Setuptools-based projects that use the setup.py file,
* newer Setuptools-based projects that have a setup.cfg file,
* general Python projects that use the PEP 517 pyproject.toml file
  (which allows using any build system, such as setuptools, flit or poetry).

These macros replace %%py3_build and %%py3_install,
which only work with setup.py.


%package -n pgdg-pyproject-srpm-macros
Summary:	Minimal implementation of %%pyproject_buildrequires
Requires:	(pyproject-rpm-macros = %{?epoch:%{epoch}:}%{version}-%{release} if pyproject-rpm-macros)

%description -n pgdg-pyproject-srpm-macros
This package contains a minimal implementation of %%pyproject_buildrequires.
When used in %%generate_buildrequires, it will generate BuildRequires
for pyproject-rpm-macros. When both packages are installed, the full version
takes precedence.


%prep
# Not strictly necessary but allows working on file names instead
# of source numbers in install section
%setup -c -T
%{__cp} -p %{sources} .

%build
# nothing to do, sources are not buildable

%install
%{__mkdir} -p %{buildroot}%{_rpmmacrodir}
%{__mkdir} -p %{buildroot}%{_rpmconfigdir}/redhat
%{__install} -pm 644 macros.pyproject %{buildroot}%{_rpmmacrodir}/
%{__install} -pm 644 macros.aaa-pyproject-srpm %{buildroot}%{_rpmmacrodir}/
%{__install} -pm 644 pyproject_buildrequires.py %{buildroot}%{_rpmconfigdir}/redhat/
%{__install} -pm 644 pyproject_convert.py %{buildroot}%{_rpmconfigdir}/redhat/
%{__install} -pm 644 pyproject_save_files.py %{buildroot}%{_rpmconfigdir}/redhat/
%{__install} -pm 644 pyproject_preprocess_record.py %{buildroot}%{_rpmconfigdir}/redhat/
%{__install} -pm 644 pyproject_construct_toxenv.py %{buildroot}%{_rpmconfigdir}/redhat/
%{__install} -pm 644 pyproject_requirements_txt.py %{buildroot}%{_rpmconfigdir}/redhat/
%{__install} -pm 644 pyproject_wheel.py %{buildroot}%{_rpmconfigdir}/redhat/

%check
# assert the two signatures of %%pyproject_buildrequires match exactly
signature1="$(grep '^%%pyproject_buildrequires' macros.pyproject | cut -d' ' -f1)"
signature2="$(grep '^%%pyproject_buildrequires' macros.aaa-pyproject-srpm | cut -d' ' -f1)"
test "$signature1" == "$signature2"
# but also assert we are not comparing empty strings
test "$signature1" != ""

%files
%{_rpmmacrodir}/macros.pyproject
%{_rpmconfigdir}/redhat/pyproject_buildrequires.py
%{_rpmconfigdir}/redhat/pyproject_convert.py
%{_rpmconfigdir}/redhat/pyproject_save_files.py
%{_rpmconfigdir}/redhat/pyproject_preprocess_record.py
%{_rpmconfigdir}/redhat/pyproject_construct_toxenv.py
%{_rpmconfigdir}/redhat/pyproject_requirements_txt.py
%{_rpmconfigdir}/redhat/pyproject_wheel.py

%doc README.md
%license LICENSE

%files -n pgdg-pyproject-srpm-macros
%{_rpmmacrodir}/macros.aaa-pyproject-srpm
%license LICENSE

%changelog
* Wed Jul 5 2023 Devrim Gündüz <devrim@gunduz.org> - 1.9.0-1PGDG
* Initial packaging for the PostgreSQL RPM repository. Took spec file
  and other components from Fedora rawhide, and made very little adjustments.
  Currently for RHEL 8 only. These macros are already available on RHEL 9 and
  Fedora.
