%global debug_package %{nil}

%if 0%{?fedora} || 0%{?rhel} >= 7
%global macros_dir %{_rpmconfigdir}/macros.d
%else
%global macros_dir %{_sysconfdir}/rpm
%endif

%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
BuildArch:	noarch
%endif

Name:		pgdg-rpm-macros
Version:	1.0.0
Release:	1%{?dist}
Summary:	RPM macros for building PostgreSQL PGDG Packages

License:	PostgreSQL
URL:		https://yum.PostgreSQL.org/pgdg-rpm-macros
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
%license COPYRIGHT
%doc AUTHORS
%{macros_dir}/macros.pgdg-postgresql

%changelog
* Fri May 31 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1
- Initial packaging for PostgreSQL RPM Repository
