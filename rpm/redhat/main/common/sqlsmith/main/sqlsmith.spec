Name:		sqlsmith
Version:	1.4
Release:	2PGDG%{dist}
Summary:	Random SQL generator
License:	GPLv3
URL:		https://github.com/anse1/%{name}
Source0:	https://github.com/anse1/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:	gcc-c++ libpqxx-devel libpq5-devel sqlite-devel
Requires:	libpqxx boost-regex sqlite-libs


%description
SQLsmith is a random SQL query generator. Its paragon is Csmith, which proved
valuable for quality assurance in C compilers.

It currently supports generating queries for PostgreSQL, SQLite 3 and MonetDB.
To add support for another RDBMS, you need to implement two classes providing
schema information about and connectivity to the device under test.

Besides developers of the RDBMS products, users developing extensions might
also be interested in exposing their code to SQLsmith’s random workload.

%prep
%setup -q

%build
PKG_CONFIG_PATH=%{pginstdir}/lib/pkgconfig ./configure CXX='g++ -std=gnu++17' --with-postgresql=%{_bindir}/pg_config --prefix=/usr
%{__make} -j %{?_smp_mflags}

%install
%{__make} -j %{?_smp_mflags} DESTDIR=%{buildroot} install

%files
%doc README.org
%{_bindir}/%{name}
%license COPYING

%changelog
* Sat Jul 29 2023 Devrim Gündüz <devrim@gunduz.org> - 1.4-2PGDG
- Rebuild against new libpqxx
- Add PGDG branding

* Sat Oct 22 2022 Devrim Gündüz <devrim@gunduz.org> - 1.4-1
- Update to 1.4

* Wed Feb 23 2022 Devrim Gündüz <devrim@gunduz.org> - 1.3-1
- Initial packaging for PostgreSQL RPM repository, per upstream spec.
