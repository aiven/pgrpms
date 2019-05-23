Name:           perl-Text-CSV_XS
Version:        1.39
Release:        1%{?dist}
Summary:        Comma-separated values manipulation routines
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Text-CSV_XS
Source0:        https://cpan.metacpan.org/modules/by-module/Text/Text-CSV_XS-%{version}.tgz
# Build:
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config::Tiny)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Run-time:
BuildRequires:  perl(Carp)
# Specific version ≥ 2.92 for Encode is recommended but not required
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(strict)
BuildRequires:  perl(UNIVERSAL::isa)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl(base)
BuildRequires:  perl(charnames)
BuildRequires:  perl(Config)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Tie::Scalar)
# Dependencies
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
# Specific version ≥ 2.92 for Encode is recommended but not required
Requires:       perl(Encode)
# IO::Handle is loaded by XS code
Requires:       perl(IO::Handle)
Requires:       perl(UNIVERSAL::isa)

%{?perl_default_filter}

%description
Text::CSV provides facilities for the composition and decomposition of
comma-separated values.  An instance of the Text::CSV class can combine
fields into a CSV string and parse a CSV string into fields.

%prep
%setup -q -n Text-CSV_XS-%{version}

chmod -c a-x examples/*

# Upstream does this on purpose (2011-03-23):
# "As Text::CSV_XS is so low-level, most of these files are actually *examples*
# and not ready-to-run out-of-the-box scripts that work as expected, though
# I must admit that some have evolved into being like that."
#find . -type f -exec sed -i '1s/pro/usr/' {} \;

%build
perl Makefile.PL \
  INSTALLDIRS=vendor \
  OPTIMIZE="%{optflags}" \
  NO_PACKLIST=true \
  NO_PERLLOCAL=true
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make %{?_smp_mflags} test

%files
%doc ChangeLog CONTRIBUTING.md README examples/
%{perl_vendorarch}/Text/
%{perl_vendorarch}/auto/Text/
%{_mandir}/man3/Text::CSV_XS.3*

%changelog
* Fri May 24 2019 Devrim Gündüz <devrim@gunduz.org> - 1.39-1
- Initial packaging for PostgreSQL RPM repository, to satisfy
  pgBadger dependency on Red Hat Enterprise Linux 7.
