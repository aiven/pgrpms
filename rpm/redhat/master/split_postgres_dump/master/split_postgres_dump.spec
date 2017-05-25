Summary:	Break a PostgreSQL dump file into pre-data and post-data segments
Name:		split_postgres_dump
Version:	1.3.3
Release:	2%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://bucardo.org/downloads/%{name}
Source2:	README.%{name}
URL:		https://bucardo.org/wiki/Split_postgres_dump
Requires:	perl-Data-Dumper
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

%description
split_postgres_dump is a small Perl script that breaks a --schema-only
dump file into pre and post sections. The pre section contains everything
needed to import the data, while the post section contains those actions
that should be done after the data is loaded, namely the creation of
indexes, constraints, and triggers.

%prep

%build

%install
%{__rm} -rf %{buildroot}

install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_docdir}/%{name}

install -m 755 %{SOURCE0} %{buildroot}%{_bindir}/
install -m 644 %{SOURCE2} %{buildroot}%{_docdir}/%{name}/

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/%{name}
%attr(644,root,root) %{_docdir}/%{name}/README.%{name}

%changelog
* Fri Jul 15 2016 - Devrim Gündüz <devrim@gunduz.org> 1.3.3-2
- Spec file cleanup:
 * Remove whitespaces
 * Add Requires: for perl-Data-Dumper
 * Use macros for rm
 * Fix URL

* Mon Apr 8 2013 - Devrim Gündüz <devrim@gunduz.org> 1.3.3-1
- Initial RPM packaging for PostgreSQL RPM Repository
