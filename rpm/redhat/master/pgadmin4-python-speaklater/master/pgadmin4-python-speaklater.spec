%global sname speaklater

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

Name:		pgadmin4-python3-%{sname}
Version:	1.3
Release:	4%{?dist}
Summary:	Implements a lazy string for python useful for use with get-text
License:	BSD
URL:		http://github.com/mitsuhiko/speaklater
Source0:	https://pypi.python.org/packages/source/s/%{sname}/%{sname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:  python3-devel

%description
A module that provides lazy strings for translations. Basically you get an
object that appears to be a string but changes the value every time the value
is evaluated based on a callable you provide.

%prep
%setup -qn %{sname}-%{version}

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install --root=%{buildroot}

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib}/%{sname}* %{buildroot}%{python3_sitelib}/__pycache__/%{sname}* %{buildroot}/%{pgadmin4py3instdir}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%license LICENSE
%doc PKG-INFO README
%{pgadmin4py3instdir}/*%{sname}*.egg-info
%{pgadmin4py3instdir}/%{sname}.py*
%{pgadmin4py3instdir}/__pycache__/%{sname}.cpython-*.py*
%{pgadmin4py3instdir}/%{sname}.cpython-*.py*

%changelog
* Wed Mar 4 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3-4
- Switch to PY3 on RHEL 7.


* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.3-3.1
- Rebuild against PostgreSQL 11.0

* Fri Apr 6 2018 Devrim Gündüz <devrim@gunduz.org> - 1.3-3
- pgadmin4-v3 will only support Python 3.4 in EPEL on RHEL 6,
  so adjust the spec file for that.

* Tue Apr 11 2017 Devrim Gündüz <devrim@gunduz.org> - 1.3-2
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Thu Apr 11 2013 Luke Macken <lmacken@redhat.com> - 1.3-1
- Update to 1.3
- Add the README and LICENSE

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Jan 01 2011 Juan Eduardo Barba Olivet <xhaksx@fedoraproject.org> - 1.2-4
- install commands modified
- files commands modified

* Wed Dec 29 2010 Juan Eduardo Barba Olivet <xhaksx@fedoraproject.org> - 1.2-3
- Modifed documentation (get text changed to get-text)

* Mon Nov 15 2010 Juan Eduardo Barba Olivet <xhaksx@fedoraproject.org> - 1.2-2
- Modifed documentation (gettext changed)

* Mon Nov 15 2010 Juan Eduardo Barba Olivet <xhaksx@fedoraproject.org> - 1.2-1
- This is the first release of speaklater
- Added documentation
