%global sname psutil
%global sum A process and system utilities module for Python

# Filter Python modules from Provides
%global __provides_exclude_from ^(%{python2_sitearch}|%{python3_sitearch})/.*\\.so$

%global pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7
%global __ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%endif

Name:		pgadmin4-python3-%{sname}
Version:	5.7.0
Release:	1%{?dist}
Summary:	%{sum}

License:	BSD
URL:		https://github.com/giampaolo/psutil
Source0:	https://github.com/giampaolo/psutil/archive/release-%{version}.tar.gz#/%{sname}-%{version}.tar.gz

BuildRequires:	gcc
BuildRequires:	python3-devel

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 8
BuildRequires:	python3-mock
%endif

%if 0%{?rhel}== 7
BuildRequires:	python36-mock
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
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}/
%{__mv} %{buildroot}/lib/python%{pyver}/site-packages/%{sname}-%{version}-py%{pyver}-linux-%_arch.egg/%{sname} %{buildroot}/%{pgadmin4py3instdir}/
%{__mv} %{buildroot}/lib/python%{pyver}/site-packages/%{sname}-%{version}-py%{pyver}-linux-%_arch.egg/ %{buildroot}/%{pgadmin4py3instdir}/

%files
%doc CREDITS HISTORY.rst README.rst
%license LICENSE
%dir %{pgadmin4py3instdir}/%{sname}/
%{pgadmin4py3instdir}/%{sname}/*
%{pgadmin4py3instdir}/%{sname}*egg*

%changelog
* Fri May 1 2020 Devrim Gündüz <devrim@gunduz.org> - 5.7.0-1
- Update to 5.7.0

* Tue Mar 3 2020 Devrim Gündüz <devrim@gunduz.org> - 5.5.1-2
- Switch to Python3 on RHEL 7.

* Thu Apr 18 2019 Devrim Gündüz <devrim@gunduz.org> - 5.5.1-1
- Initial packaging for PostgreSQL YUM repository, to satisfy
  pgadmin4 dependency.
