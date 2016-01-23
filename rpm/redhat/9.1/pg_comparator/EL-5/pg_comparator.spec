%global pgmajorversion 91
%global pginstdir /usr/pgsql-9.1
%global sname pg_comparator

Summary:	Efficient table content comparison and synchronization for PostgreSQL and MySQL
Name:		%{sname}%{pgmajorversion}
Version:	2.2.5
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/3661/%{sname}-%{version}.tgz
Patch0:		Makefile-pgxs.patch
URL:		http://pgfoundry.org/projects/pg-comparator
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	perl(Getopt::Long), perl(Time::HiRes), perl-Pod-Usage

%description
pg_comparator is a tool to compare possibly very big tables in
different locations and report differences, with a network and
time-efficient approach.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p1

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
make USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}
install -d %{buildroot}%{pginstdir}/share/contrib/

%post
# Create alternatives entries for binaries
%{_sbindir}/update-alternatives --install /usr/bin/pg_comparator pgcomparator %{pginstdir}/bin/pg_comparator %{pgmajorversion}0

%preun
# Drop alternatives entries for common binaries and man files
%{_sbindir}/update-alternatives --remove pgcomparator %{pginstdir}/bin/pg_comparator

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/contrib/README.%{sname}
%doc %{pginstdir}/doc/contrib/README.pgc_casts
%doc %{pginstdir}/doc/contrib/README.pgc_checksum
%doc %{pginstdir}/doc/contrib/README.xor_aggregate
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%{pginstdir}/bin/%{sname}
%{pginstdir}/lib/pgc_casts.so
%{pginstdir}/lib/pgc_checksum.so
%{pginstdir}/share/contrib/*.sql

%changelog
* Sun Jan 24 2016 - Devrim GUNDUZ <devrim@gunduz.org> 2.2.5-1
- Update to 2.2.5
- Unified spec file for all distros
- Use more macros
- Don't strip .so file
- Whitespace cleanup

* Thu Feb 13 2014 - Devrim GUNDUZ <devrim@gunduz.org> 2.2.2-1
- Update to 2.2.2

* Sun Jun 30 2013 - Devrim GUNDUZ <devrim@gunduz.org> 2.2.1-1
- Update to 2.2.1

* Wed Nov 14 2012 - Devrim GUNDUZ <devrim@gunduz.org> 2.1.2-1
- Update to 2.1.2

* Fri Sep 14 2012 - Devrim GUNDUZ <devrim@gunduz.org> 2.1.1-1
- Update to 2.1.1
- Use a better URL for tarball

* Fri Oct 8 2010 - Devrim GUNDUZ <devrim@gunduz.org> 1.6.2-1
- Refactor spec for 9.0 compatibility.

* Tue Apr 20 2010 - Devrim GUNDUZ <devrim@gunduz.org> 1.6.1-1
- Initial RPM packaging for PostgreSQL RPM Repository

