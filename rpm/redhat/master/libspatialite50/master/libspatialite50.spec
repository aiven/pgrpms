%global sname libspatialite
%global libspatialiteinstdir /usr/%{name}

%global libspatialiteversion    50

%global geosmajorversion        37
%global projmajorversion        62

%global geosinstdir /usr/geos%{geosmajorversion}
%global projinstdir /usr/proj%{projmajorversion}

# Warning to ELGIS:
# 1 of the 41 tests is known to fail on EL6 (32 bit and 64 bit Intel)
# Tests pass though on PPC and PPC64
# The author is informed about that.
# The problem seems to stem from Geos.

#EPSG data in libspatialite should be in sync with our current GDAL version

# A new feature available in PostGIS 2.0
#%%global _lwgeom "--enable-lwgeom=yes"
# Disabled due to a circular dependency issue with PostGIS
# https://bugzilla.redhat.com/show_bug.cgi?id=979179
%global _lwgeom "--disable-lwgeom"

# Geocallbacks work with SQLite 3.7.3 and up, available in Fedora and EL 7
%if (0%{?fedora} || 0%{?rhel} > 6)
  %global _geocallback "--enable-geocallbacks"
%endif

%if 0%{?rhel} == 6
# Checks are known to fail if libspatialite is built without geosadvanced
#TODO: Fails to build, reported by mail. If geosadvanced is disabled, linker flags miss geos_c
#TODO: Check if that's still true anywhere
  %global _geosadvanced "--disable-geosadvanced"
  %global _no_checks 1
%endif

# check_bufovflw test fails on gcc 4.9
# https://groups.google.com/forum/#!msg/spatialite-users/zkGP-gPByXk/EAZ-schWn1MJ
%if (0%{?fedora} >= 21 || 0%{?rhel} > 7)
  %global _no_checks 1
%endif

Name:		%{sname}%{libspatialiteversion}
Version:	5.0.0
Release:	beta0_1%{?dist}
Summary:	Enables SQLite to support spatial data
License:	MPLv1.1 or GPLv2+ or LGPLv2+
URL:		https://www.gaia-gis.it/fossil/libspatialite
Source0:	http://www.gaia-gis.it/gaia-sins/%{sname}-sources/%{sname}-%{version}-beta0.tar.gz
Patch0:		%{name}-proj_api.h-configure.patch
Patch1:		%{name}-proj_api.h-c.patch
BuildRequires:	gcc autoconf
BuildRequires:	freexl-devel
BuildRequires:	geos%{geosmajorversion}-devel >= 3.7.1
BuildRequires:	proj%{projmajorversion}-devel >= 6.2.0
BuildRequires:	sqlite-devel
BuildRequires:	zlib-devel

%if (0%{?fedora} || 0%{?rhel} > 6)
BuildRequires: libxml2-devel
%endif


%description
SpatiaLite is a a library extending the basic SQLite core in order to
get a full fledged Spatial DBMS, really simple and lightweight, but
mostly OGC-SFS compliant.

%package devel
Summary:	Development libraries and headers for SpatiaLite
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{sname}-%{version}-beta0
%patch0 -p0
%patch1 -p0
autoconf

%build
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{geosinstdir}/lib64,%{projinstdir}/lib" ; export SHLIB_LINK
LDFLAGS="$LDFLAGS -L%{geosinstdir}/lib64 -L%{projinstdir}/lib"; export LDFLAGS
./configure \
	--prefix=%{libspatialiteinstdir} \
	--disable-static \
	--with-geosconfig=/%{geosinstdir}/bin/geos-config \
	--with-lwgeom \
	--enable-libxml2 \
	%{?_geocallback}   \
	%{?_geosadvanced}

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot}

# Delete undesired libtool archives
find %{buildroot} -type f -name "*.la" -delete

%check
%if 0%{?_no_checks}
# Run check but don't fail build
#%%{__make} check V=1 ||:
#%%else
#%%{__make} check V=1
%endif

%ldconfig_scriptlets

%clean
%{__rm} -rf %{buildroot}

%files
%doc COPYING AUTHORS
%{libspatialiteinstdir}/lib/%{sname}.so.7*
%{libspatialiteinstdir}/lib/mod_spatialite.so.7*
# The symlink must be present to allow loading the extension
# https://groups.google.com/forum/#!topic/spatialite-users/zkGP-gPByXk
%{libspatialiteinstdir}/lib/mod_spatialite.so

%files devel
%doc examples/*.c
%{libspatialiteinstdir}/include/spatialite.h
%{libspatialiteinstdir}/include/spatialite
%{libspatialiteinstdir}/lib/%{sname}.so
%{libspatialiteinstdir}/lib/pkgconfig/spatialite.pc


%changelog
* Wed Sep 4 2019 Devrim Gunduz <devrim@gunduz.org> - 5.0.0beta0-1
- Update to 5.0.0beta0 for new Proj

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0a-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 5 2019 Devrim Gunduz <devrim@gunduz.org> - 4.3.0a-11
- Rebuilt against Proj 5.2.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0a-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0a-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0a-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 08 2017 Merlin Mathesius <mmathesi@redhat.com> - 4.3.0a-7
- Cleanup spec file conditionals

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0a-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0a-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0a-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 24 2017 Devrim Gunduz <devrim@gunduz.org> - 4.3.0a-3
- Rebuilt against Proj 4.9.3.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Sep 17 2015 Volker Froehlich <volker27@gmx.at> - 4.3.0a-1
- New upstream release

* Fri Jul  3 2015 Volker Fröhlich <volker27@gmx.at> - 4.3.0-1
- New upstream release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 12 2015 Devrim Gunduz <devrim@gunduz.org> - 4.2.0-4
- Rebuilt against Proj 4.9.1.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 29 2014 Volker Fröhlich <volker27@gmx.at> - 4.2.0-2
- libxml2 default is now "yes"
- Disable geos support for EL5, as geos 3.2 is no longer supported
- Move the mod_spatialite symlink to the main package

* Fri Jul 25 2014 Peter Robinson <pbrobinson@fedoraproject.org> 4.2.0-1
- Update to 4.2.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 23 2014 Volker Fröhlich <volker27@gmx.at> - 4.1.1-2
- Update for EPEL 7

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul  1 2013 Volker Fröhlich <volker27@gmx.at> - 4.1.1-1
- New upstram release

* Thu Jun 27 2013 Volker Fröhlich <volker27@gmx.at> - 4.1.0-2
- Temporarily disable lwgeom features to break the circular
  dependency between gdal -- libspatialite -- postgis -- gdal

* Tue Jun  4 2013 Volker Fröhlich <volker27@gmx.at> - 4.1.0-1
- New upstream release

* Mon Apr  8 2013 Volker Fröhlich <volker27@gmx.at> - 4.0.0-3
- Disable hexgrid22 test on 32 bit systems
- Disable tests on ARM

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec  1 2012 Volker Fröhlich <volker27@gmx.at> - 4.0.0-1
- New upstream release
- Remove arch restrictions, solving BZ 663938 and 846301
- Update conditional for geosadvanced

* Sat Aug 18 2012 Volker Fröhlich <volker27@gmx.at> - 3.1.0-0.3.RC2
- Add ppc to excluded archs (BZ #846301)
- Don't build with profiling

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-0.2.RC2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 27 2012 Volker Fröhlich <volker27@gmx.at> - 3.1.0-0.1.RC2
- Add pkconfig as Requirement to the devel sub-package
- Drop freexl patch (solved), build with Freexl
- Update descriptions and summaries
- Re-design conditionals for build flags
- Don't run checks if built without advancedgeos
- Include examples as documentation

* Sat Jan 14 2012 Volker Fröhlich <volker27@gmx.at> - 3.0.1-1
- New upstream release
- Drop defattr
- Run tests
- Own spatialite include-dir
- Add GPLv2+ and LGPLv2+ as alternative licenses
- Update URL and source URL
- Reduce build conditions to EPEL or not
- Use isa macro in base package Requires

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-0.7.RC4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-0.6.RC4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 7 2010 Volker Fröhlich <volker27@gmx.at> 2.4.0-0.5.RC4
- Corrected wrong Fedora version number in if-statement

* Sun Dec 5 2010 Volker Fröhlich <volker27@gmx.at> 2.4.0-0.4.RC4
- Refined configure condition to support RHEL

* Fri Dec 3 2010 Volker Fröhlich <volker27@gmx.at> 2.4.0-0.3.RC4
- Added buildroot
- Added doc files

* Wed Dec 1 2010 Volker Fröhlich <volker27@gmx.at> 2.4.0-0.2.RC4
- Added description of devel package
- Switched to disable-static flag

* Sun Nov 28 2010 Volker Fröhlich <volker27@gmx.at> 2.4.0-0.1.RC4
- Initial packaging for Fedora
