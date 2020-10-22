%global	sname brotli
%global	pgadmin4py2instdir %{python2_sitelib}/pgadmin4-web/
%global	pgadmin4py3instdir %{python3_sitelib}/pgadmin4-web/

%global	__ospython %{_bindir}/python3
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global	python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global	python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

Name:		pgadmin4-python3-%{sname}
Version:	1.0.7
Release:	9%{?dist}
Summary:	Lossless compression algorithm

License:	MIT
URL:		https://github.com/google/brotli
Source0:	%{url}/archive/v%{version}/%{name}-%{version}.tar.gz

%if 0%{?rhel} == 7
BuildRequires:	devtoolset-7-toolchain, devtoolset-7-libatomic-devel
%endif
BuildRequires:	gcc gcc-c++
BuildRequires:	cmake
BuildRequires:	python3-devel python3-setuptools

%description
Brotli is a generic-purpose lossless compression algorithm that compresses
data using a combination of a modern variant of the LZ77 algorithm, Huffman
coding and 2nd order context modeling, with a compression ratio comparable
to the best currently available general-purpose compression methods.
It is similar in speed with deflate but offers more dense compression.
This package installs a Python 3 module.

%prep
%autosetup -n %{sname}-%{version}
# fix permissions for -debuginfo
# rpmlint will complain if I create an extra %%files section for
# -debuginfo for this so we'll put it here instead
chmod 644 c/enc/*.[ch]
chmod 644 c/include/brotli/*.h
chmod 644 c/tools/brotli.c

%build
%if 0%{?rhel} == 7
. /opt/rh/devtoolset-7/enable
%endif
%{__mkdir} -p build
cd build
%cmake .. -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
    -DCMAKE_INSTALL_LIBDIR="%{_libdir}"
%make_build
cd ..
%py3_build

%install
%if 0%{?rhel} == 7
. /opt/rh/devtoolset-7/enable
%endif
cd build
%make_install

# I couldn't find the option to not build the static libraries
%{__rm} "%{buildroot}%{_libdir}/"*.a

cd ..
%py3_install

%ldconfig_scriptlets

# Move everything under pgadmin4 web/ directory.
%{__mkdir} -p %{buildroot}/%{pgadmin4py3instdir}
%{__mv} %{buildroot}%{python3_sitelib64}/%{sname}.py  %{buildroot}%{python3_sitelib64}/__pycache__/*%{sname}* %{buildroot}%{python3_sitelib64}/_brotli.cpython-*.so %{buildroot}%{python3_sitelib64}/Brotli-%{version}-py%{pyver}.egg-info %{buildroot}/%{pgadmin4py3instdir}

# Remove binary, include files and libraries, we don't need them:
%{__rm} -f %{buildroot}%{_bindir}/brotli
%{__rm} -f %{buildroot}%{_libdir}/libbro*
%{__rm} -fr %{buildroot}%{_includedir}/brotli
%{__rm} -f %{buildroot}%{_mandir}/*
%{__rm} -f %{buildroot}/%{_libdir}/pkgconfig/*brotli*

%files
%{pgadmin4py3instdir}/Brotli-%{version}-py%{pyver}.egg-info/*
%{pgadmin4py3instdir}/brotli.py
%{pgadmin4py3instdir}/*brotli.cpython*.so
%{pgadmin4py3instdir}/brotli.cpython*.pyc
%{pgadmin4py3instdir}/__pycache__/brotli.cpython*
%license LICENSE

%changelog
* Wed Jan 1 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.7-9
- Initial packaging for the PostgreSQL RPM Repository, based on
  Fedora rawhide spec
