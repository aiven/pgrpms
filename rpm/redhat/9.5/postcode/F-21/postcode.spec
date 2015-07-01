%global pgmajorversion 95
%global pginstdir /usr/pgsql-9.5
%global sname postcode

Summary:	UK postcode type optimised for indexing
Name:		%{sname}_%{pgmajorversion}
Version:	1.3.0
Release:	1%{?dist}
License:	BSD
Source0:	http://api.pgxn.org/dist/postcode/%{version}/postcode-%{version}.zip
Patch0:		%{sname}-1.3.0-c99-and-pgconfig.patch
URL:		http://pgxn.org/dist/postcode/

%description
UK postcode encoded in 32 bits and optimised for indexing and partial matches.
Parses and encodes UK postcodes in 32 bits optimised for indexing and partial
matches. Also provides suitable type for delivery point suffixes.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%{__make} %{?_smp_mflags}

%install
%make_install
# Let's also install documentation:
%{__mkdir} -p %{buildroot}%{pginstdir}/share/extension
%{__cp} README.md %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md
# Install sql/ directory:
%{__mkdir} -p %{buildroot}/%{_datadir}/%{name}/
%{__cp} -rp sql/ %{buildroot}/%{_datadir}/%{name}/

%postun -p /sbin/ldconfig
%post -p /sbin/ldconfig

%files
%license LICENSE
%doc %{pginstdir}/share/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control
%{_datadir}/%{name}

%changelog
* Tue May 12 2015 - Devrim GUNDUZ <devrim@gunduz.org> 1.3.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
