%global sname mod_wsgi

%{!?_httpd_apxs: %{expand: %%global _httpd_apxs %%{_sbindir}/apxs}}

%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir: %{expand: %%global _httpd_moddir    %%{_libdir}/httpd/modules}}

%global debug_package %{nil}

Name:		pgadmin4-python3_mod_wsgi
Version:	4.6.8
Release:	2%{?dist}
Summary:	A WSGI interface for Python web applications in Apache (customized
License:	ASL 2.0
URL:		https://modwsgi.readthedocs.io/
Source0:	https://github.com/GrahamDumpleton/mod_wsgi/archive/%{version}.tar.gz#/mod_wsgi-%{version}.tar.gz
Source2:	wsgi-python3.conf
Patch1:		mod_wsgi-4.5.20-exports.patch

Requires:	httpd-mmn = %{_httpd_mmn}
BuildRequires:	python3-devel
BuildRequires:	httpd-devel
BuildRequires:	gcc

# Suppress auto-provides for module DSO
%{?filter_provides_in: %filter_provides_in %{_httpd_moddir}/.*\.so$}
%{?filter_setup}

%global _description\
The mod_wsgi adapter is an Apache module that provides a WSGI compliant\
interface for hosting Python based web applications within Apache. The\
adapter is written completely in C code against the Apache C runtime and\
for hosting WSGI applications within Apache has a lower overhead than using\
existing WSGI adapters for mod_python or CGI.\

%description %_description

%prep
%autosetup -p1 -n %{sname}-%{version}

%build
export LDFLAGS="$RPM_LD_FLAGS -L%{_libdir}"
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"

%{__mkdir} py3build/
# this always produces an error (because of trying to copy py3build
# into itself) but we don't mind, so || :
%{__cp} -R * py3build/ || :
pushd py3build
%configure --enable-shared --with-apxs=%{_httpd_apxs} --with-python=python3
%{__make} %{?_smp_mflags}
%{_bindir}/python3 setup.py build
popd

%install
pushd py3build
%{__make} install DESTDIR=$RPM_BUILD_ROOT LIBEXECDIR=%{_httpd_moddir}
%{__mv} $RPM_BUILD_ROOT%{_httpd_moddir}/mod_wsgi.so $RPM_BUILD_ROOT%{_httpd_moddir}/pgadmin4-python3-mod_wsgi.so
%{__install} -d -m 755 $RPM_BUILD_ROOT%{_httpd_modconfdir}
# httpd >= 2.4.x
%{__install} -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_httpd_modconfdir}/10-wsgi-python3.conf

%{_bindir}/python3 setup.py install -O1 --skip-build --root %{buildroot}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/mod_wsgi-express{,-3}
popd

%files
%license LICENSE
%doc CREDITS.rst README.rst
%config(noreplace) %{_httpd_modconfdir}/*wsgi-python3.conf
%{_httpd_moddir}/pgadmin4-python3-mod_wsgi.so
%{python3_sitearch}/mod_wsgi-*.egg-info
%{python3_sitearch}/mod_wsgi
%{_bindir}/mod_wsgi-express-3

%changelog
* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.8-2
- Initial packaging for the PostgreSQL YUM repository
