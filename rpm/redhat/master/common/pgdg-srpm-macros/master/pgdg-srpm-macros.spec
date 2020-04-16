%global debug_package %{nil}

%if 0%{?fedora} || 0%{?rhel} >= 7
%global macros_dir %{_rpmconfigdir}/macros.d
%else
%global macros_dir %{_sysconfdir}/rpm
%endif

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 8
BuildArch:	noarch
%endif

Name:		pgdg-srpm-macros
Version:	1.0.1
Release:	1%{?dist}
Summary:	SRPM macros for building PostgreSQL PGDG Packages

License:	PostgreSQL
URL:		https://yum.PostgreSQL.org/pgdg-srpm-macros
Source0:	macros.pgdg-postgresql
Source1:	COPYRIGHT
Source2:	AUTHORS

%description
A set of macros for building PostgreSQL PGDG packages. 3rd party packagers can
override these macros and use their own.

%prep
%setup -c -T
%{__cp} %{SOURCE1} %{SOURCE2} .


%build
echo no build stage needed

%install
%{__install} -p -D -m 0644 %{SOURCE0} %{buildroot}/%{macros_dir}/macros.pgdg-postgresql

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYRIGHT AUTHORS
%else
%license COPYRIGHT
%doc AUTHORS
%endif
%{macros_dir}/macros.pgdg-postgresql

%changelog
* Thu Apr 16 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.1-1
- Add CXX flags for PPC64LE. Extracted from another patch by Talha.

* Fri May 31 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1
- Initial packaging for PostgreSQL RPM Repository
