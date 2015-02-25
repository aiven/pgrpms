%global pgmajorversion 94
%global pginstdir /usr/pgsql-9.4
%global sname plruby

%if 0%{?rhel} <= 5
%{!?ruby_sitearch: %global ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"] ' 2>/dev/null)}
%{!?ruby_vendorarchdir: %global ruby_vendorarchdir %ruby_sitearch}
%else
%{!?ruby_vendorarchdir: %global ruby_vendorarchdir %(ruby -rrbconfig -e 'puts Config::CONFIG["vendorarchdir"] ' 2>/dev/null)}
%endif

Summary:	PostgreSQL Ruby Procedural Language
Name:		%{sname}%{pgmajorversion}
Version:	0.5.4
Release:	6%{?dist}
Source0:	https://github.com/knu/postgresql-%{sname}/archive/v0.5.4/postgresql-%{sname}-%{version}.tar.gz
License:	Ruby or GPL+
Group:		Applications/Databases
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Url:		https://github.com/knu/postgresql-plruby
BuildRequires:	ruby >= 1.8 ruby-devel >= 1.8 postgresql%{pgmajorversion}
Requires:	postgresql%{pgmajorversion}-libs, ruby(release)

Patch0:	postgresql-plruby-bitopers.patch
Patch2:	postgresql-plruby-retval.patch
Patch3:	postgresql-plruby-includes.patch
Patch4:	postgresql-plruby-version.patch
Patch5:	postgresql-plruby-ruby22-rbconfig.patch

%description
PL/Ruby is a loadable procedural language for the PostgreSQL database
system that enable the Ruby language to create functions and trigger
procedures.

%package doc
Summary:	Documentation for plruby
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation for plruby.

%prep
%setup -q -n postgresql-%{sname}-%{version}

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%patch0 -p1 -b .biopers
%endif
%patch2 -p1 -b .retval
%patch3 -p1 -b .debug
%patch4 -p1 -b .version
%patch5 -p1 -b .rbconfig

%build
ruby extconf.rb --vendor --with-pg-config=%{pginstdir}/bin/pg_config
make

%install
rm -rf %{buildroot}
# ruby_headers= applied as workaround for rhbz#921650.
make DESTDIR=%{buildroot} %{?_smp_mflags} ruby_headers= install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README.en plruby.html
%dir %{ruby_vendorarchdir}/plruby
%{ruby_vendorarchdir}/plruby/plruby_*.so

%files doc
%defattr(-,root,root,-)
%doc docs/plruby.rb

%changelog
* Wed Feb 25 2015 Devrim Gündüz <devrim@gunduz.org> 0.5.4-6
- Resync patches from Fedora
- Update URL
- Use the right pg_config

* Wed Jul 30 2014 Devrim Gündüz <devrim@gunduz.org> 0.5.4-5
- Resync with Fedora spec file

* Wed Jul 2 2014 Devrim Gündüz <devrim@gunduz.org> 0.5.4-4
- Sync with Fedora spec file
- Trim changelog
