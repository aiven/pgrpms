%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	A wrapper library for the Firebird C API
Name:		libfq
Version:	0.4.2
Release:	1%{dist}
Source:		https://github.com/ibarwick/%{name}/archive/0.4.2.tar.gz
URL:		https://github.com/ibarwick/%{name}
License:	PostgreSQL
Group:		Development/Libraries/C and C++
BuildRequires:	firebird-devel libfbclient2

%if 0%{?rhel} && 0%{?rhel} == 7
Requires:	firebird-libfbclient
%else
Requires:	libfbclient2
%endif

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
A wrapper library for the Firebird C API, loosely based on libpq for PostgreSQL.

%prep
%setup -q -n %{name}-%{version}

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
./configure --prefix=%{_prefix} \
	--with-ibase=%{_includedir}/firebird --libdir=%{_libdir}/

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%{_libdir}/%{name}.a
%{_libdir}/%{name}.la
%{_libdir}/%{name}.so
%{_libdir}/%{name}-%version.so
%{_includedir}/%{name}-expbuffer.h
%{_includedir}/%{name}-int.h
%{_includedir}/%{name}.h

%changelog
* Tue Oct 20 2020 Devrim Gündüz <devrim@gunduz.org> - 0.4.2-1
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  firebird_fdw dependency. This is an improved version of the upstream
  spec file.
