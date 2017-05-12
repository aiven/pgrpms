%if 0%{?fedora} > 24
%{!?with_python3:%global with_python3 1}
%global __ospython3 %{_bindir}/python3
%{expand: %%global py3ver %(echo `%{__ospython3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%else
%{!?with_python3:%global with_python3 0}
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%endif

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/

%global oname   beautifulsoup4

Name:           pgadmin4-python-beautifulsoup4
Version:        4.5.1
Release:        2%{?dist}
Summary:        HTML/XML parser for quick-turnaround applications like screen-scraping
Group:          Development/Languages
License:        MIT
URL:            http://www.crummy.com/software/BeautifulSoup/
Source0:        https://files.pythonhosted.org/packages/source/b/%{oname}/%{oname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-devel >= 2.6 python-setuptools python-lxml
Requires:       python-lxml

%description
Beautiful Soup is a Python HTML/XML parser designed for quick
turnaround projects like screen-scraping. Three features make it
powerful:

Beautiful Soup won't choke if you give it bad markup.

Beautiful Soup provides a few simple methods and Pythonic idioms for
navigating, searching, and modifying a parse tree.

Beautiful Soup automatically converts incoming documents to Unicode
and outgoing documents to UTF-8.

Beautiful Soup parses anything you give it.

Valuable data that was once locked up in poorly-designed websites is
now within your reach. Projects that would have taken hours take only
minutes with Beautiful Soup.

%prep
%setup -q -n %{oname}-%{version}
%{__mv} AUTHORS.txt AUTHORS.txt.iso
iconv -f ISO-8859-1 -t UTF-8 -o AUTHORS.txt AUTHORS.txt.iso
touch -r AUTHORS.txt.iso AUTHORS.txt

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}
%{__mv} %{buildroot}%{python2_sitelib}/bs4 %{buildroot}%{python2_sitelib}/%{oname}-%{version}-py%{py2ver}.egg-info %{buildroot}/%{pgadmin4py2instdir}

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc AUTHORS.txt NEWS.txt README.txt TODO.txt COPYING.txt
%else
%license COPYING.txt
%doc AUTHORS.txt NEWS.txt README.txt TODO.txt
%endif
%{pgadmin4py2instdir}/%{oname}-%{version}*.egg-info
%{pgadmin4py2instdir}/bs4

%changelog
* Mon Apr 10 2017 Devrim Gündüz <devrim@gunduz.org> - 4.5.1-2
- Move the components under pgadmin web directory, per #2332.
- Do a spring cleanup in the spec file.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 4.5.1-1
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.

