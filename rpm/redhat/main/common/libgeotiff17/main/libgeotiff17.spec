%global	sname libgeotiff
%global	libgeotiffversion 17

%pgdg_set_gis_variables

# Override PROJ major version on RHEL 7.
# libspatialite 4.3 does not build against 8.0.0 as of March 2021.
%if 0%{?rhel} && 0%{?rhel} == 7
%global projmajorversion 72
%global projfullversion 7.2.1
%global projinstdir /usr/proj%{projmajorversion}
%endif

Name:		%{sname}%{libgeotiffversion}
Version:	1.7.0
Release:	1%{?dist}
Summary:	GeoTIFF format library
License:	MIT
URL:		https://github.com/OSGeo/%{sname}
Source0:	https://github.com/OSGeo/%{sname}/releases/download/%{version}/%{sname}-%{version}.tar.gz
Source2:	%{name}-pgdg-libs.conf
BuildRequires:	libtiff-devel libjpeg-devel proj%{projmajorversion}-devel zlib-devel
BuildRequires:	pgdg-srpm-macros >= 1.0.17

%description
GeoTIFF represents an effort by over 160 different remote sensing,
GIS, cartographic, and surveying related companies and organizations
to establish a TIFF based interchange format for georeferenced
raster imagery.

%package devel
Summary:	Development Libraries for the GeoTIFF file format library
Requires:	pkgconfig libtiff-devel
Requires:	%{name} = %{version}-%{release}

%description devel
The GeoTIFF library provides support for development of geotiff image format.

%prep
%setup -q -n %{sname}-%{version}

# fix wrongly encoded files from tarball
set +x
for f in `find . -type f` ; do
   if file $f | grep -q ISO-8859 ; then
      set -x
      iconv -f ISO-8859-1 -t UTF-8 $f > ${f}.tmp && \
	mv -f ${f}.tmp $f
      set +x
   fi
   if file $f | grep -q CRLF ; then
      set -x
      sed -i -e 's|\r||g' $f
      set +x
   fi
done
set -x

# remove junks
find . -name ".cvsignore" -exec rm -rf '{}' \;

%build

# disable -g flag removal
sed -i 's| \| sed \"s\/-g \/\/\"||g' configure

# use gcc -shared instead of ld -shared to build with -fstack-protector
sed -i 's|LD_SHARED=@LD_SHARED@|LD_SHARED=@CC@ -shared|' Makefile.in

./configure \
	--prefix=%{libgeotiff17instdir}	\
	--includedir=%{libgeotiff17instdir}/include/ \
	--mandir=%{libgeotiff17instdir}/man	\
	--libdir=%{libgeotiff17instdir}/lib	\
	--with-proj=%{proj81instdir}	\
	--with-tiff		\
	--with-jpeg		\
	--with-zip
# WARNING
# disable %{?_smp_mflags}
# it breaks compile

%{__make}

%install
# install libgeotiff
%{__make} install DESTDIR=%{buildroot} INSTALL="%{__install} -p"

# install manualy some file
%{__mkdir} -p %{buildroot}%{libgeotiff17instdir}/bin
%{__install} -p -m 755 bin/makegeo %{buildroot}%{libgeotiff17instdir}/bin

# install pkgconfig file
cat > %{name}.pc <<EOF
prefix=%{libgeotiff17instdir}
exec_prefix=%{libgeotiff17instdir}
libdir=%{libgeotiff17instdir}/lib
includedir=%{libgeotiff17instdir}/include

Name: %{name}
Description: GeoTIFF file format library
Version: %{version}
Libs: -L\${libdir} -lgeotiff
Cflags: -I\${includedir}
EOF

%{__mkdir} -p %{buildroot}%{libgeotiff17instdir}/lib/pkgconfig/
%{__install} -p -m 644 %{name}.pc %{buildroot}%{libgeotiff17instdir}/lib/pkgconfig/

#clean up junks
%{__rm} -rf %{buildroot}%{libgeotiff17instdir}/lib/*.a
%{__rm} -f %{buildroot}%{libgeotiff17instdir}/lib/*.la

# Install linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%{__install} %{SOURCE2} %{buildroot}%{_sysconfdir}/ld.so.conf.d/

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc ChangeLog LICENSE README
%{libgeotiff17instdir}/bin/applygeo
%{libgeotiff17instdir}/bin/geotifcp
%{libgeotiff17instdir}/bin/listgeo
%{libgeotiff17instdir}/bin/makegeo
%{libgeotiff17instdir}/lib/libgeotiff.so.*
%{libgeotiff17instdir}/man/man1/listgeo.1
%{libgeotiff17instdir}/man/man1/geotifcp.1
%{libgeotiff17instdir}/man/man1/applygeo.1
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%dir %{libgeotiff17instdir}/include
%attr(0644,root,root) %{libgeotiff17instdir}/include/*.h
%attr(0644,root,root) %{libgeotiff17instdir}/include/*.inc
%{libgeotiff17instdir}/lib/libgeotiff.so
%{libgeotiff17instdir}/lib/pkgconfig/%{name}.pc


%changelog
* Wed Sep 1 2021 Devrim Gündüz <devrim@gunduz.org> - 1.7.0-1
- Initial packaging for PostgreSQL RPM repository.
