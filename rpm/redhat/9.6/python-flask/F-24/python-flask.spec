%if 0%{?fedora} > 23
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global py2ver %(echo `%{__python} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%{expand: %%global py3ver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%else
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%endif

%global modname flask
%global srcname Flask

%if 0%{?with_python3}
Name:           python-%{modname}
%else
Name:           python-%{modname}
%endif
Version:        0.11.1
Release:        3%{?dist}
Epoch:          1
Summary:        A micro-framework for Python based on Werkzeug, Jinja 2 and good intentions

License:        BSD
URL:            http://flask.pocoo.org/
Source0:        https://files.pythonhosted.org/packages/source/%(n=%{srcname}; echo ${n:0:1})/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

%description
Flask is called a “micro-framework” because the idea to keep the core
simple but extensible. There is no database abstraction layer, no form
validation or anything else where different libraries already exist
that can handle that. However Flask knows the concept of extensions
that can add this functionality into your application as if it was
implemented in Flask itself. There are currently extensions for object
relational mappers, form validation, upload handling, various open
authentication technologies and more.

%if 0%{?with_python3}
%{?python_provide:%python_provide python3-%{modname}}
%{?python_provide:%python_provide python3-%{modname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
BuildRequires:  python3-jinja2
BuildRequires:  python3-werkzeug
BuildRequires:  python3-itsdangerous
BuildRequires:  python3-click
Requires:       python3-jinja2
Requires:       python3-werkzeug
Requires:       python3-itsdangerous
Requires:       python3-click
%else
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pytest
BuildRequires:  python-jinja2
BuildRequires:  python-werkzeug
BuildRequires:  python-itsdangerous
BuildRequires:  python-click
Requires:       python-jinja2
Requires:       python-werkzeug
Requires:       python-itsdangerous
Requires:       python-click
%endif

%prep
%autosetup -n %{srcname}-%{version}
%{__rm} -vf examples/flaskr/.gitignore

%build
%if 0%{?with_python3}
%py3_build
%else
%{__ospython} setup.py build
%endif

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/%{modname}{,-%{python3_version}}
ln -s %{modname}-%{python3_version} %{buildroot}%{_bindir}/%{modname}-3

ln -sf %{modname}-2 %{buildroot}%{_bindir}/%{modname}
%else
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install --skip-build --root %{buildroot}
%endif

%files
%{_bindir}/%{modname}
%if 0%{?with_python3}
%license LICENSE
%doc CHANGES README
%{_bindir}/%{modname}-3
%{_bindir}/%{modname}-%{python3_version}
%{python3_sitelib}/%{srcname}-*.egg-info/
%{python3_sitelib}/%{modname}/
%else
%doc CHANGES README LICENSE
#%{_bindir}/%{modname}-%{python2_version}
%{python2_sitelib}/%{srcname}-*.egg-info/
%{python2_sitelib}/%{modname}/
%endif

%changelog
* Mon Aug 22 2016 Igor Gnatenko <ignatenko@redhat.com> - 1:0.11.1-3
- Fix FTBFS
- Ton of fixes in spec

* Tue Aug 16 2016 Ricky Elrod <relrod@redhat.com> - 1:0.11.1-2
- Attempt a completely fresh build with new NVR.

* Tue Aug 16 2016 Ricky Elrod <relrod@redhat.com> - 1:0.11.1-1
- Latest upstream release.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.10.1-9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.10.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 1:0.10.1-7
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.10.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.10.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1:0.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4
- Minor fix to rhel macro logic

* Mon Jul 29 2013 Haïkel Guémar <hguemar@fedoraproject.org> - 1:0.10.1-3
- fix wrong requires on sphinx (RHBZ #989361)

* Sat Jul 20 2013 Ricky Elrod <codeblock@fedoraproject.org> - 1:0.10.1-2
- Nuke a Python3 specific file owned by python3-setuptools.

* Sat Jun 15 2013 Haïkel Guémar <hguemar@fedoraproject.org> - 1:0.10.1-1
- upstream 0.10.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 17 2012 Ricky Elrod <codeblock@fedoraproject.org> - 0.9-5
- Add epoch to subpackage Requires.

* Wed Aug 8 2012 Ricky Elrod <codeblock@fedoraproject.org> - 0.9-4
- Fix changelog messup.

* Wed Aug 8 2012 Ricky Elrod <codeblock@fedoraproject.org> - 0.9-3
- Unified spec for EL6 and Fedora

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  2 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 0.9.0-1
- upstream 0.9
- spec cleanups

* Sun Jul  1 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 0.8.1-1
- upstream 0.8.1 (minor bugfixes)

* Wed Jan 25 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 0.8.0-1
- upstream 0.8

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 16 2011 Dan Young <dyoung@mesd.k12.or.us> - 0.7.2-2
- don't own easy-install.pth

* Fri Jul 22 2011 Steve Milner <smilner@fedoraproject.org> - 0.7.2-1
- update for upstream release

* Thu Feb 24 2011 Dan Young <dyoung@mesd.k12.or.us> - 0.6.1-2
- fix rpmlint spelling warning
- BR python2-devel rather than python-devel
- run test suite in check

* Tue Feb 22 2011 Dan Young <dyoung@mesd.k12.or.us> - 0.6.1-1
- Initial package
