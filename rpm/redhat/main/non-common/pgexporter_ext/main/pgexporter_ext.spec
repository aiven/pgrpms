%global sname	pgexporter_ext
%global _vpath_builddir .

Name:           %{sname}_%{pgmajorversion}
Version:	0.1.0
Release:	1%{dist}
Summary:	PostgreSQL extension to provide additional Prometheus metrics for pgexporter.
License:	BSD
URL:		https://github.com/pgexporter/%{sname}
Source0:	https://github.com/pgexporter/%{sname}/archive/refs/tags/%{version}.tar.gz

BuildRequires:	gcc cmake3 make
BuildRequires:	openssl openssl-devel postgresql%{pgmajorversion}-devel
Requires:	openssl postgresql%{pgmajorversion}-server

%description
pgexporter_ext is an extension for PostgreSQL to provide additional
Prometheus metrics for pgexporter.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__mkdir} build
cd build
export PATH=%{pginstdir}/bin/:$PATH
cmake -DCMAKE_BUILD_TYPE=Release ..
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags}

%install
cd build
export PATH=%{pginstdir}/bin/:$PATH
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} install \
	DESTDIR=%{buildroot}

%files
%license LICENSE
%doc CODE_OF_CONDUCT.md README.md AUTHORS
%{pginstdir}/lib/%{sname}.so*
%{pginstdir}/share/extension/%{sname}*

%changelog
* Fri Oct 22 2021 - Devrim Gündüz <devrim@gunduz.org> 0.1.0-1
- Initial packaging for PostgreSQL RPM repository. Used upstream's
  spec file.

