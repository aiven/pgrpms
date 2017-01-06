%global perl_vendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%global perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)
%global sname DBD-Oracle

Summary:	DBD-Oracle module for perl
Name:		perl-%{sname}
Version:	1.74
Release:	1%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
Source0:	https://github.com/pythian/%{sname}/archive/v%{version}.tar.gz
Source1:	demo.mk
URL:		https://github.com/pythian/%{sname}
BuildRoot:	%{_tmppath}/%{sname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	perl >= 0:5.6.1, perl(ExtUtils::MakeMaker)
BuildRequires:	oracle-instantclient11.2-devel
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# the version requires is not automatically picked up
Requires:	perl(DBI) >= 1.51

%description
Oracle database driver for the DBI module.

%prep
%setup -q -n %{sname}-%{version}
cp %{SOURCE1} .

%build
MKFILE=$(find /usr/share/oracle/ -name demo.mk)
%ifarch ppc ppc64
# the included version in oracle-instantclient-devel is bad on ppc arches
# using the version from i386 rpm
MKFILE=demo.mk
%endif
%ifarch x86_64 s390x
ORACLE_HOME=$(find /usr/lib/oracle/ -name client64 | tail -1)
%else
ORACLE_HOME=$(find /usr/lib/oracle/ -name client | tail -1)
%endif
export ORACLE_HOME
perl Makefile.PL -m $MKFILE INSTALLDIRS="vendor" PREFIX=%{_prefix} -V 11.2.0.4.0
make  %{?_smp_mflags} OPTIMIZE="%{optflags}"

%clean
%{__rm} -rf %{buildroot}

%install
%{__rm} -rf %{buildroot}
make PREFIX=%{buildroot}%{_prefix} pure_install

%{__rm} -f `find %{buildroot} -type f -name perllocal.pod -o -name .packlist`

%files
%defattr(-,root,root)
%{perl_vendorarch}/auto/DBD/
%{perl_vendorarch}/DBD/
%{_mandir}/man3/*

%changelog
* Tue Jul 12 2016 Devrim Gündüz <devrim@gunduz.org> 1.74-1
- Update to 1.74
- Fix rpmlint warnings
- Trim changelog
