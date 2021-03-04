%global		name perl-DBD-Oracle
%global		pkgname %(echo %{name}| sed 's/perl-//')
%{!?version:%global version 1.80}
%{!?oi_ver:%global oi_ver instantclient21.1}
%{!?oi_release:%global oi_release 21.1.0.0.0}
%global		release %{oi_release}%{dist}
%global		perl_vendorarch %(eval "$(%{__perl} -V:installvendorarch)"; echo $installvendorarch)
%global		_use_internal_dependency_generator 0
%global		custom_find_req %{_tmppath}/%{pkgname}-%{version}-find-requires
%global		__find_requires %{custom_find_req}
%global		__perl_requires %{custom_find_req}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	DBD-Oracle - Oracle database driver for the DBI module
License:	GPL+ or Artistic
URL:		https://github.com/pythian/DBD-Oracle
Source0:	https://www.cpan.org/modules/by-module/DBD/DBD-Oracle-1.80.tar.gz
# A temp patch until the next release of perl-DBD-Oracle
# so that it recognizes the new packaging as of OIC 21
Patch0:		%{name}-OIC21.patch
Requires:	libaio
Requires:	perl(:MODULE_COMPAT_%(eval "$(%{__perl} -V:version)"; echo $version))
Requires:	perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:	perl(DBI) >= 1.51 perl(ExtUtils::MakeMaker) >= 6.30
Requires:	perl(DBI) >= 1.51
Requires:	oracle-instantclient-basic = %{oi_release}
BuildRequires:	oracle-instantclient-devel = %{oi_release}
BuildRequires:	oracle-instantclient-sqlplus = %{oi_release}
Provides:	perl(DBD-Oracle) = %{version}

%description
DBD::Oracle is a Perl module which works with the DBI module to provide
access to Oracle databases.
This documentation describes driver specific behaviour and restrictions.
It is not supposed to be used as the only reference for the user.
In any case consult the DBI documentation first!

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p0
chmod -R u+w %{_builddir}/%{pkgname}-%{version}

%build
export ORACLE_HOME=$(dirname $(dirname $(rpm -ql oracle-instantclient-sqlplus | grep '/usr/lib/oracle/.*/sqlplus')))
export LD_LIBRARY_PATH=$ORACLE_HOME/lib
MKFILE=$(rpm -ql oracle-instantclient-devel | grep demo.mk)
%{__perl} Makefile.PL -m $MKFILE INSTALLDIRS="vendor" PREFIX=%{_prefix} -V %{oi_release}
%{__make} %{?_smp_mflags} OPTIMIZE="%{optflags}"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
cat << 'EOF' > %{custom_find_req}
#!/bin/sh
/usr/lib/rpm/redhat/find-requires | grep -v -e 'libclntsh.so.' -e 'libocci.so.'
EOF
chmod 755 %{custom_find_req}
%{__make} PREFIX=%{buildroot}%{_prefix} pure_install
%{__rm} -f $(find %{buildroot} -type f -name perllocal.pod -o -name .packlist)

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
%{__rm} -f %{custom_find_req}

%files
%defattr(-,root,root)
%defattr(-,root,root)
%{perl_vendorarch}/auto/DBD/
%{perl_vendorarch}/DBD/
%{_mandir}/man3/*

%changelog
* Thu Mar 4 2021 Devrim Gündüz <devrim@gunduz.org> - 1.80-4
- Rebuild for instant client 21.1.0.0.0
- Add a temp patch until the next release of perl-DBD-Oracle,
  so that it recognizes the new packaging as of OIC 21.

* Thu Sep 24 2020 Devrim Gündüz <devrim@gunduz.org> - 1.80-3
- Rebuild for instant client 19.8.0.0.0

* Sat Jul 11 2020 Devrim Gündüz <devrim@gunduz.org> - 1.80-2
- Rebuild for instant client 19.6.0.0.0

* Fri Nov 15 2019 Devrim Gündüz <devrim@gunduz.org> - 1.80-1
- Initial packaging for PostgreSQL RPM repository.
