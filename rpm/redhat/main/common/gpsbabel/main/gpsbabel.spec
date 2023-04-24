%global tarballversion 1_8_0

Name:		gpsbabel
Version:	1.8.0
Release:	2%{?dist}.1
Summary:	A tool to convert between various formats used by GPS devices

License:	GPLv2+
URL:		https://www.gpsbabel.org
# Upstream's website hides tarball behind some ugly php script
# Original repo is at https://github.com/gpsbabel/gpsbabel
Source0:	https://github.com/GPSBabel/gpsbabel/archive/refs/tags/%{name}_%{tarballversion}.tar.gz
Source2:	%{name}.png

# No automatic phone home by default (RHBZ 668865)
Patch2:		%{name}-0002-No-solicitation.patch

BuildRequires:	libusb-devel
BuildRequires:	zlib-devel
BuildRequires:	desktop-file-utils
BuildRequires:	shapelib-devel
BuildRequires:	cmake

%if 0%{?suse_version} >= 1315
BuildRequires:	libqt5-qtbase-devel
BuildRequires:	libqt5-qtserialport-devel
%else
BuildRequires:	qt5-qtbase-devel
BuildRequires:	qt5-qtserialport-devel
%endif

%ifarch %{qt5_qtwebengine_arches}
# HACK: Don't build GUI on archs not supported by qtwebengine
%global build_gui 1
BuildRequires:	qt5-qtwebchannel-devel
BuildRequires:	qt5-qtwebengine-devel
%endif

%description
Converts GPS waypoint, route, and track data from one format type
to another.

%if 0%{?build_gui}
%package gui
Summary:	Qt GUI interface for GPSBabel
License:	GPLv2+
Requires:	%{name} = %{version}-%{release}

%description gui
Qt GUI interface for GPSBabel
%endif

%prep
%setup -q -n %{name}-%{name}_%{tarballversion}

%patch -P 2 -p1

%build
%cmake \
  -DGPSBABEL_WITH_ZLIB=pkgconfig \
  -DGPS_BABEL_WITH_SHAPE_LIB=pkgconfig \
  -DGPSBABEL_WITH_SHAPELIB=pkgconfig \
  %{?!build_gui:-DGPSBABEL_MAPPREVIEW=OFF} \
  ..
%cmake_build

%install
%cmake_install

install -m 0755 -d %{buildroot}%{_bindir}/
install -m 0755 -p %{_vpath_builddir}/gpsbabel %{buildroot}%{_bindir}/

%if 0%{?build_gui}
install -m 0755 -d %{buildroot}%{_bindir}/
install -m 0755 -p %{_vpath_builddir}/gui/GPSBabelFE/gpsbabelfe %{buildroot}%{_bindir}/

install -m 0755 -d %{buildroot}%{_qt5_translationdir}/
install -m 0644 -p gui/gpsbabelfe_*.qm  %{buildroot}%{_qt5_translationdir}/

install -m 0755 -d %{buildroot}%{_qt5_translationdir}/
install -m 0644 -p gui/coretool/gpsbabel_*.qm %{buildroot}%{_qt5_translationdir}/

install -m 0755 -d %{buildroot}%{_datadir}/gpsbabel
install -m 0644 -p gui/gmapbase.html %{buildroot}%{_datadir}/gpsbabel

desktop-file-install \
	--dir %{buildroot}/%{_datadir}/applications \
	gui/gpsbabel.desktop

install -m 0755 -d %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/
install -m 0644 -p %{SOURCE2} %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/

%find_lang %{name} --with-qt --all-name
%endif

%files
%doc README* AUTHORS
%license COPYING
%{_bindir}/gpsbabel

%if 0%{?build_gui}
%files gui -f %{name}.lang
%doc gui/{AUTHORS,README*,TODO}
%license gui/COPYING*
%{_bindir}/gpsbabelfe
%{_datadir}/gpsbabel
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/256x256/apps/*
%endif

%changelog
* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 1.8.0-2.1
- Modernise %patch usage, which has been deprecated in Fedora 38

* Thu Jul 21 2022 Devrim Gunduz <devrim@gunduz.org> - 1.8.0-2
- Add SLES 12 support

* Wed Jul 13 2022 Devrim Gunduz <devrim@gunduz.org> - 1.8.0-1
- Initial packaging for RHEL 9, until EPEL provides a package itself.
