Name:		sqlsmith
Version:	1.2.1
Release:	1%{dist}
Summary:	Random SQL generator
License:	GPLv3
URL:		https://github.com/anse1/%{name}
Source0:	https://github.com/anse1/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
Patch0:		sqlsmith-libpqxx7.patch

BuildRequires:	gcc-c++ libpqxx-devel libpq5-devel
#Requires:	libpq5

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
%patch0 -p0

%build
PKG_CONFIG_PATH=%{pginstdir}/lib/pkgconfig ./configure CXX='g++ -std=gnu++17' --with-postgresql=%{_bindir}/pg_config --prefix=/usr
%{__make} -j %{?_smp_mflags}

%install
%{__make} -j %{?_smp_mflags}

%files
%license %{_docdir}/%{name}/LICENSE

%changelog
* Fri Jul 10 2020 Devrim Gündüz <devrim@gunduz.org> - 1.2.1-1
- Initial packaging for PostgreSQL RPM repository, per upstream spec.
