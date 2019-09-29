%global sname psutil
%global sum A process and system utilities module for Python

# Filter Python modules from Provides
%global __provides_exclude_from ^(%{python2_sitearch}|%{python3_sitearch})/.*\\.so$

%global pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} > 25 || 0%{?rhel} == 8
%{!?with_python3:%global with_python3 1}
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?rhel} == 7
%{!?with_python3:%global with_python3 0}
%global __ospython %{_bindir}/python2
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

%if 0%{?with_python3}
Name:		pgadmin4-python3-%{sname}
%else
Name:		pgadmin4-python-%{sname}
%endif

Version:	5.5.1
Release:	1%{?dist}
Summary:	%{sum}

License:	BSD
URL:		https://github.com/giampaolo/psutil
Source0:	https://github.com/giampaolo/psutil/archive/release-%{version}.tar.gz#/%{sname}-%{version}.tar.gz
#
# Disable upstream failing test
# https://github.com/giampaolo/psutil/issues/946
#
#Patch0:	psutil-5.4.3-disable-broken-tests.patch

BuildRequires:	gcc

%if 0%{?fedora} > 25 || 0%{?rhel} == 8
BuildRequires:	python3-devel python3-mock
%endif

%if 0%{?rhel} == 7
BuildRequires:	python2-devel python-mock python-ipaddress
%endif

%description
psutil is a module providing an interface for retrieving information on all
running processes and system utilization (CPU, memory, disks, network,
users) in a portable way by using Python, implementing many
functionalities offered by command line tools such as: ps, top, df,
kill, free, lsof, free, netstat, ifconfig, nice, ionice, iostat, iotop,
uptime, pidof, tty, who, taskset, pmap.


%prep
%autosetup -p0 -n %{sname}-release-%{version}

# Remove shebangs
find psutil -name \*.py | while read file; do
  sed -i.orig -e '1{/^#!/d}' $file && \
  touch -r $file.orig $file && \
  rm $file.orig
done


%build
%{__ospython} setup.py build

%install
export PYTHONUSERBASE=%{buildroot}
%{__ospython} setup.py install --user
%{__rm} -f %{buildroot}/lib/python%{pyver}/site-packages/easy-install.pth

# Move everything under pgadmin4 web/ directory.
%if 0%{?with_python3}
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}/
%{__mv} %{buildroot}//lib/python%{pyver}/site-packages/%{sname}-%{version}-py%{pyver}-linux-x86_64.egg/%{sname} %{buildroot}/%{pgadmin4py3instdir}/
%{__mv} %{buildroot}//lib/python%{pyver}/site-packages/%{sname}-%{version}-py%{pyver}-linux-x86_64.egg/ %{buildroot}/%{pgadmin4py3instdir}/
%else # Python 2
%{__mkdir} -p %{buildroot}/%{pgadmin4py2instdir}/
%{__mv} %{buildroot}//lib/python%{pyver}/site-packages/%{sname}-%{version}-py%{pyver}-linux-x86_64.egg/%{sname} %{buildroot}/%{pgadmin4py2instdir}/
%{__mv} %{buildroot}//lib/python%{pyver}/site-packages/%{sname}-%{version}-py%{pyver}-linux-x86_64.egg/ %{buildroot}/%{pgadmin4py2instdir}/
%endif # with_python3

%files
%doc CREDITS HISTORY.rst README.rst
%if 0%{?with_python3}
%dir %{pgadmin4py3instdir}/%{sname}/
%{pgadmin4py3instdir}/%{sname}/*
%{pgadmin4py3instdir}/%{sname}*egg*
%else # Python 2
%doc docs LICENSE
%dir %{pgadmin4py2instdir}/%{sname}/
%{pgadmin4py2instdir}/%{sname}/*
%{pgadmin4py2instdir}/%{sname}*egg*
%endif # python3

%changelog
* Thu Apr 18 2019 Devrim Gündüz <devrim@gunduz.org> - 5.5.1-1
- Initial packaging for PostgreSQL YUM repository, to satisfy
  pgadmin4 dependency.
