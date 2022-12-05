%global sname	pg_auth_mon

Summary:	PostgreSQL extension to store authentication attempts
Name:		%{sname}_%{pgmajorversion}
Version:	1.0
Release:	1%{?dist}
License:	MIT
Source0:	https://github.com/RafiaSabih/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/RafiaSabih/%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-libs

%description
The goal of this extension is to ease monitoring of login attempts to your database.
Although each failed login is written to database log file, but it is not straightforward
to identify through that information alone if your database is under some malicious
intents. However, if the information like total failed as well as successful login
attempts, timestamp of last failed and successful login are maintained individually,
then we can easily answer questions like,
 * if the user genuinely mistyped their password or their username is being compromised?
 * if there is any particular time when the malicious user/application is active?

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
  %endif
 %endif
%endif

%changelog
* Thu Feb 25 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Initial packaging for PostgreSQL RPM Repository
