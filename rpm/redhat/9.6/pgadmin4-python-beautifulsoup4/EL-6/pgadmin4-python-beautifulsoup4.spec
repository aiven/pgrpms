%global oname   beautifulsoup4

Name:           python-beautifulsoup4
Version:        4.5.1
Release:        1%{?dist}
Summary:        HTML/XML parser for quick-turnaround applications like screen-scraping
Group:          Development/Languages
License:        MIT
URL:            http://www.crummy.com/software/BeautifulSoup/
Source0:        https://files.pythonhosted.org/packages/source/b/%{oname}/%{oname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-devel >= 2.6
# html5lib BR just for test coverage
BuildRequires:  python-html5lib
BuildRequires:  python-setuptools
BuildRequires:  python-lxml
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
mv AUTHORS.txt AUTHORS.txt.iso
iconv -f ISO-8859-1 -t UTF-8 -o AUTHORS.txt AUTHORS.txt.iso
touch -r AUTHORS.txt.iso AUTHORS.txt

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc AUTHORS.txt NEWS.txt README.txt TODO.txt COPYING.txt
%else
%license COPYING.txt
%doc AUTHORS.txt NEWS.txt README.txt TODO.txt
%endif
%{python_sitelib}/beautifulsoup4-%{version}*.egg-info
%{python_sitelib}/bs4

%changelog
* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> - 4.5.1-1
- Initial version for PostgreSQL RPM repository to satisfy
  pgadmin4 dependency.

