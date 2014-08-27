Name:           perl-Mojolicious
Version:        5.33
Release:        1%{?dist}
Summary:        A next generation web framework for Perl
License:        Artistic 2.0

URL:            http://mojolicio.us/
Source0:        http://search.cpan.org/CPAN/authors/id/S/SR/SRI/Mojolicious-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl >= 0:5.010001
BuildRequires:  perl(Compress::Raw::Zlib)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(Digest::SHA)
BuildRequires:  perl(IO::Compress::Gzip)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Time::HiRes)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
Back in the early days of the web there was this wonderful Perl library
called CGI, many people only learned Perl because of it. It was simple
enough to get started without knowing much about the language and powerful
enough to keep you going, learning by doing was much fun. While most of the
techniques used are outdated now, the idea behind it is not. Mojolicious is
a new attempt at implementing this idea using state of the art technology.

%prep
%setup -q -n Mojolicious-%{version}
mv README.md lib/Mojolicious/

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
#make test

%files
%license LICENSE
%doc Changes examples
%{_bindir}/mojo
%{_bindir}/hypnotoad
%{_bindir}/morbo
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Wed Aug 27 2014 Devrim Gündüz <devrim@gunduz.org> - 5.33-1
- Initial packaging for PostgreSQL RPM repository, to satisfy
  powa dependency on RHEL 6 and RHEL 7.
