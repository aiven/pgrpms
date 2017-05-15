%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/

%global sname speaklater

Name:           pgadmin4-python-%{sname}
Version:        1.3
Release:        2%{?dist}
Summary:        Implements a lazy string for python useful for use with get-text
Group:          Development/Libraries
License:        BSD
URL:            http://github.com/mitsuhiko/speaklater
Source0:        http://pypi.python.org/packages/source/s/%{sname}/%{sname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel

%description
A module that provides lazy strings for translations. Basically you get an
object that appears to be a string but changes the value every time the value
is evaluated based on a callable you provide.

%prep
%setup -qn %{sname}-%{version}

%build
%{__ospython2} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython2} setup.py install --root=%{buildroot}

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/%{sname}* %{buildroot}/%{pgadmin4py2instdir}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc PKG-INFO README LICENSE
%{pgadmin4py2instdir}/*%{sname}*.egg-info
%{pgadmin4py2instdir}/%{sname}.py*

%changelog
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
