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
Version:	0.5.5
Release:	2%{?dist}
Source0:	https://github.com/devrimgunduz/postgresql-%{sname}/archive/%{version}.tar.gz
Source1:	plruby.control
License:	Ruby or GPL+
Group:		Applications/Databases
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Url:		https://github.com/devrimgunduz/postgresql-plruby
BuildRequires:	ruby >= 1.8 ruby-devel >= 1.8 postgresql%{pgmajorversion}
Requires:	postgresql%{pgmajorversion}-libs, ruby(release)

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

%build
ruby extconf.rb --vendor --with-pg-config=%{pginstdir}/bin/pg_config --with-safe-level=3
make

%install
rm -rf %{buildroot}
# ruby_headers= applied as workaround for rhbz#921650.
make DESTDIR=%{buildroot} %{?_smp_mflags} ruby_headers= install
mkdir -p %{buildroot}%{pginstdir}/share/extension
install %{SOURCE1}  %{buildroot}%{pginstdir}/share/extension

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README.markdown
%dir %{ruby_vendorarchdir}/plruby
%{ruby_vendorarchdir}/plruby.so
%{ruby_vendorarchdir}/plruby/plruby_*.so
/usr/pgsql-9.4/share/extension/plruby.control

%files doc
%defattr(-,root,root,-)
%doc docs/plruby.rb plruby.html

%changelog
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
