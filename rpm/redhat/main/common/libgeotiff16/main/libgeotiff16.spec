%global	sname libgeotiff
%global	libgeotiffversion 16

%pgdg_set_gis_variables

# Override some variables.
%global projmajorversion %proj92majorversion
%global projfullversion %proj92fullversion
%global projinstdir %proj92instdir

Name:		%{sname}%{libgeotiffversion}
Version:	1.6.0
Release:	7PGDG%{?dist}
Summary:	GeoTIFF format library
License:	MIT
URL:		https://github.com/OSGeo/%{sname}
Source0:	https://github.com/OSGeo/%{sname}/releases/download/%{version}/%{sname}-%{version}.tar.gz
Source2:	%{name}-pgdg-libs.conf
BuildRequires:	libtiff-devel libjpeg-devel proj%{projmajorversion}-devel zlib-devel
BuildRequires:	pgdg-srpm-macros >= 1.0.33

Obsoletes:	%{sname}15 >= 1.5.0

%description
GeoTIFF represents an effort by over 160 different remote sensing,
GIS, cartographic, and surveying related companies and organizations
to establish a TIFF based interchange format for georeferenced
raster imagery.

%package devel
Summary:	Development Libraries for the GeoTIFF file format library
Requires:	pkgconfig libtiff-devel
Requires:	%{name} = %{version}-%{release}

Obsoletes:	%{sname}15-devel >= 1.5.0

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
	--prefix=%{libgeotiffinstdir}	\
	--includedir=%{libgeotiffinstdir}/include/ \
	--mandir=%{libgeotiffinstdir}/man	\
	--libdir=%{libgeotiffinstdir}/lib	\
	--with-proj=%{projinstdir}	\
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
%{__mkdir} -p %{buildroot}%{libgeotiffinstdir}/bin
%{__install} -p -m 755 bin/makegeo %{buildroot}%{libgeotiffinstdir}/bin

# install pkgconfig file
cat > %{name}.pc <<EOF
prefix=%{libgeotiffinstdir}
exec_prefix=%{libgeotiffinstdir}
libdir=%{libgeotiffinstdir}/lib
includedir=%{libgeotiffinstdir}/include

Name: %{name}
Description: GeoTIFF file format library
Version: %{version}
Libs: -L\${libdir} -lgeotiff
Cflags: -I\${includedir}
EOF

%{__mkdir} -p %{buildroot}%{libgeotiffinstdir}/lib/pkgconfig/
%{__install} -p -m 644 %{name}.pc %{buildroot}%{libgeotiffinstdir}/lib/pkgconfig/

#clean up junks
%{__rm} -rf %{buildroot}%{libgeotiffinstdir}/lib/*.a
%{__rm} -f %{buildroot}%{libgeotiffinstdir}/lib/*.la

# Install linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%{__install} %{SOURCE2} %{buildroot}%{_sysconfdir}/ld.so.conf.d/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc ChangeLog LICENSE README
%{libgeotiffinstdir}/bin/applygeo
%{libgeotiffinstdir}/bin/geotifcp
%{libgeotiffinstdir}/bin/listgeo
%{libgeotiffinstdir}/bin/makegeo
%{libgeotiffinstdir}/lib/libgeotiff.so.*
%{libgeotiffinstdir}/man/man1/listgeo.1
%{libgeotiffinstdir}/man/man1/geotifcp.1
%{libgeotiffinstdir}/man/man1/applygeo.1
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%dir %{libgeotiffinstdir}/include
%attr(0644,root,root) %{libgeotiffinstdir}/include/*.h
%attr(0644,root,root) %{libgeotiffinstdir}/include/*.inc
%{libgeotiffinstdir}/lib/libgeotiff.so
%{libgeotiffinstdir}/lib/pkgconfig/%{name}.pc


%changelog
* Tue Sep 12 2023 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-7PGDG
- Rebuild against Proj 9.2.x
- Remove RHEL 7 support
- Add PGDG branding

* Sat Jan 8 2022 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-6
- Rebuild against Proj 8.2.x

* Tue May 18 2021 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-5
- Rebuild against Proj 8.0.1

* Mon Mar 22 2021 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-4
- Emergency commit to fix RHEL 7 issues.

* Mon Mar 22 2021 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-3
- Override PROJ major version on RHEL 7. libspatialite 4.3
  does not build against 8.0.0 as of March 2021.

* Fri Mar 12 2021 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-2
- Rebuild against Proj 8.0.0
- Update URLs

* Mon May 4 2020 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-1
- Initial packaging for PostgreSQL RPM repository.
