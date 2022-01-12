Name:		pgprtdbg
Version:	0.3.0
Release:	1%{dist}
Summary:	Turn PostgreSQL protocol v3 interaction into a trace file.
License:	BSD
URL:		https://github.com/jesperpedersen/%{name}/%{name}
Source0:	https://github.com/jesperpedersen/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz

BuildRequires:	gcc cmake make

%description
pgprtdbg is an application that turns PostgreSQL protocol v3 interaction
into a trace file.

%prep
%setup -q -n %{name}-%{version}

%build
%{__mkdir} build
cd build
cmake -DCMAKE_BUILD_TYPE=Release .. -DCMAKE_INSTALL_PREFIX=/
%{__make}

%install
cd build
%{__make} install DESTDIR=%{buildroot}

# Move docs and config file under docdir:
%{__install} -d %{buildroot}/%{_docdir}/%{name}
%{__mv} %{buildroot}/share/doc/%{name}/*  %{buildroot}/%{_docdir}/%{name}
%{__mv} %{buildroot}/%{_docdir}/%{name}/etc/pgprtdbg.conf %{buildroot}/%{_docdir}/%{name}

%files
%license LICENSE
%config %{_sysconfdir}/%{name}.conf
%doc CONFIGURATION.md GETTING_STARTED.md RPM.md %{name}.conf
%{_libdir}/lib%{name}*
%{_bindir}/%{name}

%changelog
* Mon Jan 10 2022 Devrim Gündüz <devrim@gunduz.org> 0.3.0-1
- Initial packaging for PostgreSQL RPM repository.
