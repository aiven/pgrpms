%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%global tarName speaklater

Name:           python-%{tarName}
Version:        1.3
Release:        1%{?dist}
Summary:        Implements a lazy string for python useful for use with get-text
Group:          Development/Libraries
License:        BSD
URL:            http://github.com/mitsuhiko/speaklater
Source0:        http://pypi.python.org/packages/source/s/%{tarName}/%{tarName}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel

%description
A module that provides lazy strings for translations. Basically you get an
object that appears to be a string but changes the value every time the value
is evaluated based on a callable you provide.

%prep
%setup -qn %{tarName}-%{version}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{python_sitelib}/speaklater*
%doc PKG-INFO README LICENSE

%changelog
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
