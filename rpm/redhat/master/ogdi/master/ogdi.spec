Name:		ogdi
Version:	3.2.0
Release:	4%{?dist}
Summary:	Open Geographic Datastore Interface
Group:		Applications/Engineering
License:	BSD
URL:		http://ogdi.sourceforge.net/
Source0:	https://downloads.sourceforge.net/project/ogdi/ogdi/3.2.0/ogdi-3.2.0.tar.gz
Source1:	http://ogdi.sourceforge.net/ogdi.pdf
# https://bugzilla.redhat.com/show_bug.cgi?id=1470896
Patch0:		ogdi-3.2.0.beta2-sailer.patch

BuildRequires:	unixODBC-devel zlib-devel
BuildRequires:	expat-devel proj49-devel tcl-devel

%description
OGDI is the Open Geographic Datastore Interface. OGDI is an
application programming interface (API) that uses a standardized
access methods to work in conjunction with GIS software packages (the
application) and various geospatial data products. OGDI uses a
client/server architecture to facilitate the dissemination of
geospatial data products over any TCP/IP network, and a
driver-oriented approach to facilitate access to several geospatial
data products/formats.


%package devel
Summary:	OGDI header files and documentation
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
Requires:	zlib-devel expat-devel proj49-devel

%description devel
OGDI header files and developer's documentation.


%package odbc
Summary:	ODBC driver for OGDI
Group:		System Environment/Libraries
Requires:	%{name} = %{version}-%{release}

%description odbc
ODBC driver for OGDI.


%package tcl
Summary:	TCL wrapper for OGDI
Group:		System Environment/Libraries
Requires:	%{name} = %{version}-%{release}

%description tcl
TCL wrapper for OGDI.


%prep
%setup -q
%patch0 -p0 -b .rhbz1470896

# include documentation
%{__cp} -p %{SOURCE1} .


%build
TOPDIR=`pwd`; TARGET=Linux; export TOPDIR TARGET
INST_LIB=%{_libdir}/;export INST_LIB
export CFG=debug # for -g

# do not compile with ssp. it will trigger internal bugs (to_fix_upstream)
OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//g'`
export CFLAGS="$OPT_FLAGS -fPIC -DPIC -DDONT_TD_VOID -DUSE_TERMIO"
%configure \
	--with-binconfigs \
	--with-expat \
	--with-proj=/usr/proj49 \
	--with-zlib

# WARNING !!!
# using %{?_smp_mflags} may break build
%{__make}

# build tcl interface
%{__make} -C ogdi/tcl_interface \
	TCL_LINKLIB="-ltcl"

# build contributions
%{__make} -C contrib/gdal

# build odbc drivers
ODBC_LINKLIB="-lodbc"
%{__make} -C ogdi/attr_driver/odbc \
	ODBC_LINKLIB="-lodbc"


%install
# export env
TOPDIR=`pwd`; TARGET=Linux; export TOPDIR TARGET

%{__make} install \
	INST_INCLUDE=%{buildroot}%{_includedir}/%{name} \
	INST_LIB=%{buildroot}%{_libdir} \
	INST_BIN=%{buildroot}%{_bindir}

# install plugins olso
%{__make} install -C ogdi/tcl_interface \
	INST_LIB=%{buildroot}%{_libdir}
%{__make} install -C contrib/gdal \
	INST_LIB=%{buildroot}%{_libdir}
%{__make} install -C ogdi/attr_driver/odbc \
	INST_LIB=%{buildroot}%{_libdir}

# remove example binary
%{__rm} %{buildroot}%{_bindir}/example?

# we have multilib ogdi-config
%if "%{_lib}" == "lib"
%global cpuarch 32
%else
%global cpuarch 64
%endif

# fix file(s) for multilib issue
touch -r ogdi-config.in ogdi-config

# install pkgconfig file and ogdi-config
%{__mkdir} -p %{buildroot}%{_libdir}/pkgconfig
%{__install} -p -m 644 ogdi.pc %{buildroot}%{_libdir}/pkgconfig/
%{__install} -p -m 755 ogdi-config %{buildroot}%{_bindir}/ogdi-config-%{cpuarch}
# ogdi-config wrapper for multiarch
cat > %{buildroot}%{_bindir}/%{name}-config <<EOF
#!/bin/bash

ARCH=\$(uname -m)
case \$ARCH in
x86_64 | ppc64 | ppc64le | ia64 | s390x | sparc64 | alpha | alphaev6 | aarch64 )
ogdi-config-64 \${*}
;;
*)
ogdi-config-32 \${*}
;;
esac
EOF
chmod 755 %{buildroot}%{_bindir}/%{name}-config
touch -r ogdi-config.in %{buildroot}%{_bindir}/%{name}-config


%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc LICENSE NEWS ChangeLog README
%{_bindir}/gltpd
%{_bindir}/ogdi_*
%{_libdir}/libogdi.so.*
%dir %{_libdir}/ogdi
%exclude %{_libdir}/%{name}/liblodbc.so
%exclude %{_libdir}/%{name}/libecs_tcl.so
%{_libdir}/%{name}/lib*.so

%files devel
%doc ogdi.pdf
%doc ogdi/examples/example1/example1.c
%doc ogdi/examples/example2/example2.c
%{_bindir}/%{name}-config
%{_bindir}/%{name}-config-%{cpuarch}
%{_libdir}/pkgconfig/%{name}.pc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/libogdi.so

%files odbc
%{_libdir}/%{name}/liblodbc.so

%files tcl
%{_libdir}/%{name}/libecs_tcl.so


%changelog
* Mon Dec 18 2017 Devrim Gündüz <devrim@gunduz.org> - 3.2.0-4
* Initial packaging for PostgreSQL RPM repository, which uses our own
  proj49 package.
