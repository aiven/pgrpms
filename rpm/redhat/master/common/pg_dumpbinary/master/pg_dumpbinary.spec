Summary:	Dump a PostgreSQL database with data dumped in binary format
Name:		pg_dumpbinary
Version:	2.0
Release:	1%{?dist}
License:	BSD
Source0:	https://github.com/lzlabs/%{name}/archive/v%{version}.tar.gz
URL:		https://github.com/lzlabs/%{name}
Requires:	perl-Time-HiRes
BuildRequires:	perl-ExtUtils-MakeMaker
BuildArch:	noarch

%description
pg_dumpbinary is a program used to dump a PostgreSQL database with data
dumped in binary format. The resulting dumps must be restored using
pg_restorebinary.

%prep
%setup -q

%build
%{__perl} Makefile.PL
%{__make}

%install
%{__rm} -rf %{buildroot}

# We install everthing manually, as make install points
# to /usr/local directory.
%{__install} -d %{buildroot}%{_bindir}/
%{__install} -d %{buildroot}%{_mandir}/man1
%{__install} -m 755 pg_dumpbinary pg_restorebinary %{buildroot}%{_bindir}/
%{__install} -m 644 blib/man1/pg_dumpbinary.1p blib/man1/pg_restorebinary.1p %{buildroot}%{_mandir}/man1

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{_bindir}/pg_dumpbinary
%{_bindir}/pg_restorebinary
%{_mandir}/man1/pg_dumpbinary.1p.gz
%{_mandir}/man1/pg_restorebinary.1p.gz

%changelog
* Wed Feb 5 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0-1
- Update to 2.0

* Sun Sep 1 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Initial packaging for PostgreSQL RPM Repository.
