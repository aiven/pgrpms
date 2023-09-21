%global _vpath_builddir .
%global	sname libgeotiff
%global	libgeotiffversion 17

%pgdg_set_gis_variables

# Override PROJ:
%global projmajorversion %proj92majorversion
%global projfullversion %proj92fullversion
%global projinstdir %proj92instdir

Name:		%{sname}%{libgeotiffversion}
Version:	1.7.1
Release:	4PGDG%{?dist}
Summary:	GeoTIFF format library
License:	MIT
URL:		https://github.com/OSGeo/%{sname}
Source0:	https://github.com/OSGeo/%{sname}/releases/download/%{version}/%{sname}-%{version}.tar.gz
Source2:	%{name}-pgdg-libs.conf
BuildRequires:	libtiff-devel libjpeg-devel proj%{projmajorversion}-devel zlib-devel
BuildRequires:	pgdg-srpm-macros >= 1.0.33 cmake

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

%build

%{__install} -d build
pushd build
cmake .. -DCMAKE_C_COMPILER_LAUNCHER=ccache -DPROJ_LIBRARY=%{projinstdir}/lib64 \
	-DPROJ_INCLUDE_DIR=%{projinstdir}/include \
	-DGEOTIFF_BIN_DIR=%{libgeotiff17instdir}/bin -DGEOTIFF_LIB_DIR=%{libgeotiff17instdir}/lib \
	-DGEOTIFF_BIN_SUBDIR=%{libgeotiff17instdir}/bin -DGEOTIFF_MAN_PAGES=%{libgeotiff17instdir}/man \
	-DGEOTIFF_INCLUDE_SUBDIR=%{libgeotiff17instdir}/include

%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags}
popd

%install
# install libgeotiff
pushd build
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} install DESTDIR=%{buildroot}

# install manually some files
%{__mkdir} -p %{buildroot}%{libgeotiff17instdir}/bin
%{__install} -p -m 755 bin/makegeo %{buildroot}%{libgeotiff17instdir}/bin
popd

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

# Do some manual installation:
%{__mkdir} -p %{buildroot}/%{_docdir}/%{name}
%{__mkdir} -p %{buildroot}%{libgeotiff17instdir}/lib
%{__mkdir} -p %{buildroot}%{libgeotiff17instdir}/man/man1
%{__mv} %{buildroot}/usr/local/doc/* %{buildroot}%{_docdir}/%{name}
%{__mv} %{buildroot}/usr/local/lib/libgeotiff.a %{buildroot}/%{libgeotiff17instdir}/lib
%{__rm} -f %{buildroot}/usr/local/share/cmake/GeoTIFF/*cmake
%{__mv} %{buildroot}/usr/local/share/man/man1/* %{buildroot}%{libgeotiff17instdir}/man/man1

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc ChangeLog LICENSE AUTHORS COPYING INSTALL README*
%{libgeotiff17instdir}/bin/applygeo
%{libgeotiff17instdir}/bin/geotifcp
%{libgeotiff17instdir}/bin/listgeo
%{libgeotiff17instdir}/bin/makegeo
%{libgeotiff17instdir}/lib/*.a
%{libgeotiff17instdir}/man/man1/listgeo.1
%{libgeotiff17instdir}/man/man1/geotifcp.1
%{libgeotiff17instdir}/man/man1/applygeo.1

%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%dir %{libgeotiff17instdir}/include
%attr(0644,root,root) %{libgeotiff17instdir}/include/*.h
%attr(0644,root,root) %{libgeotiff17instdir}/include/*.inc
%{libgeotiff17instdir}/lib/pkgconfig/%{name}.pc


%changelog
* Thu Sep 21 2023 Devrim Gündüz <devrim@gunduz.org> - 1.7.1-4PGDG
- Support SLES 15

* Mon Aug 28 2023 Devrim Gündüz <devrim@gunduz.org> - 1.7.1-3PGDG
- Remove RHEL 7 bits
- Add PGDG branding
- Fix rpmlint and build warnings

* Thu Apr 6 2023 Devrim Gündüz <devrim@gunduz.org> - 1.7.1-2
- Use Proj 9.2.X

* Wed Mar 23 2022 Devrim Gündüz <devrim@gunduz.org> - 1.7.1-1
- Update to 1.7.1

* Wed Sep 1 2021 Devrim Gündüz <devrim@gunduz.org> - 1.7.0-1
- Initial packaging for PostgreSQL RPM repository.
