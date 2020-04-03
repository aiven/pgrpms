%global sname plruby

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

%{!?ruby_vendorarchdir: %global ruby_vendorarchdir %(ruby -rrbconfig -e 'puts Config::CONFIG["vendorarchdir"] ' 2>/dev/null)}

Summary:	PostgreSQL Ruby Procedural Language
Name:		%{sname}%{pgmajorversion}
Version:	0.5.7
Release:	2%{?dist}.1
Source0:	https://github.com/devrimgunduz/postgresql-%{sname}/archive/%{version}.tar.gz
Source1:	plruby.control
%if 0%{?rhel} && 0%{?rhel} <= 6
# plruby.so fails to build w/o this patch on RHEL 6.
Patch0:		%{sname}-rhel6-include.patch
%endif
License:	Ruby or GPL+
Url:		https://github.com/devrimgunduz/postgresql-plruby
BuildRequires:	ruby >= 1.8 ruby-devel >= 1.8 postgresql%{pgmajorversion}
Requires:	postgresql%{pgmajorversion}-libs, ruby(release)
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
PL/Ruby is a loadable procedural language for the PostgreSQL database
system that enable the Ruby language to create functions and trigger
procedures.

%package doc
Summary:	Documentation for plruby
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation for plruby.

%prep
%setup -q -n postgresql-%{sname}-%{version}
%if 0%{?rhel} && 0%{?rhel} <= 6
%patch0 -p0
%endif

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
        PATH=%{atpath}/bin/:%{atpath}/sbin:$PATH ; export PATH
%endif
## Using safe-level=3, since Ruby 2.1+ and later does not support safe level
## bigger than 3.
## https://bugs.ruby-lang.org/issues/8468
## https://bugs.ruby-lang.org/projects/ruby-trunk/repository/revisions/41259
## Upstream report: https://github.com/knu/postgresql-plruby/issues/9

# Using safe-level=1, since Ruby 2.3+ and later does not support safe level
# bigger than 1.
# https://github.com/ruby/ruby/blob/v2_3_0/NEWS#L323
ruby extconf.rb --vendor --with-pg-config=%{pginstdir}/bin/pg_config --with-safe-level=1
%{__make}

%install
%{__rm} -rf %{buildroot}
# ruby_headers= applied as workaround for rhbz#921650.
%{__make} DESTDIR=%{buildroot} %{?_smp_mflags} ruby_headers= install
%{__mkdir} -p %{buildroot}%{pginstdir}/share/extension
%{__install} extension/* %{buildroot}%{pginstdir}/share/extension/

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README.markdown
%dir %{ruby_vendorarchdir}/plruby
%{ruby_vendorarchdir}/plruby.so
%{ruby_vendorarchdir}/plruby/plruby_*.so
%{pginstdir}/share/extension/plruby.control
%{pginstdir}/share/extension/plruby*.sql

%files doc
%defattr(-,root,root,-)
%doc docs/plruby.rb plruby.html

%changelog
* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.5.7-2.1
- Rebuild against PostgreSQL 11.0

* Mon May 29 2017 Devrim Gündüz <devrim@gunduz.org> 0.5.7-2
- Also install .sql file so that extensions can be created.

* Sun May 28 2017 Devrim Gündüz <devrim@gunduz.org> 0.5.7-1
- Update to 0.5.7, which includes a few more fixes from Fedora
  so that it can be compiled against all supported PostgreSQL
  and ruby versions.
- Add Power support.

* Wed Feb 25 2015 Devrim Gündüz <devrim@gunduz.org> 0.5.5-1
- Fork to new repo, and release 0.5.5 with patches applied.
- Build with safe level 3.

* Wed Feb 25 2015 Devrim Gündüz <devrim@gunduz.org> 0.5.4-6
- Resync patches from Fedora
- Update URL
- Use the right pg_config

* Wed Jul 30 2014 Devrim Gündüz <devrim@gunduz.org> 0.5.4-5
- Resync with Fedora spec file

* Wed Jul 2 2014 Devrim Gündüz <devrim@gunduz.org> 0.5.4-4
- Sync with Fedora spec file
- Trim changelog
