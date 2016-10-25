Summary:	PostgreSQL Log Analyzer Script
Name:		pgsi
Version:	1.7.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://bucardo.org/downloads/%{name}-%{version}.tar.gz
URL:		http://bucardo.org/pgsi
Requires:	postgresql-server
Requires:	perl(Data::Dumper) perl(Getopt::Long) perl(IO::Handle) perl(Time::Local)
BuildRequires:	perl-Test-Simple >= 0.80 perl-ExtUtils-MakeMaker
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
PGSI is a Perl utility for parsing and analyzing PostgreSQL logs to
produce wiki-ready system impact reports.

%prep
%setup -q

%build
perl Makefile.PL
make

%install
%{__rm} -rf %{buildroot}

# We install everthing manually, as make install points
# to /usr/local directory.
%{__install} -d %{buildroot}%{_bindir}/
%{__install} -d %{buildroot}%{_mandir}/man1
%{__install} -d %{buildroot}%{_docdir}/%{name}-%{version}
%{__install} -m 755 pgsi.pl %{buildroot}%{_bindir}/
%{__install} -m 644 blib/man1/pgsi.pl.1 %{buildroot}%{_mandir}/man1
%{__install} -m 644 pgsi.html  %{buildroot}%{_docdir}/%{name}-%{version}/

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%{_bindir}/%{name}.pl
%{_mandir}/man1/*
%dir %{_docdir}/%{name}-%{version}
%{_docdir}/%{name}-%{version}/*

%changelog
* Tue Jan 26 2016 - Devrim Gündüz <devrim@gunduz.org> 1.7.1-1
- Update to 1.7.1
- Use more macros, for unified spec file
- Cosmetic updates

* Thu May 27 2010 - Devrim GUNDUZ <devrim@gunduz.org> 1.2.0-1
- Update to 1.2.0

* Sun Feb 15 2009 - Devrim GUNDUZ <devrim@gunduz.org> 1.1.1-1
- Initial RPM packaging for yum.postgresql.org
