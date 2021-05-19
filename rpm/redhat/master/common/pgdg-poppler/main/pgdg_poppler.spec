%global sname poppler
%global	popplerinstdir /usr/%{name}

Summary:	PDF rendering library
Name:		pgdg-%{sname}
Version:	21.01.0
Release:	6%{?dist}
License:	(GPLv2 or GPLv3) and GPLv2+ and LGPLv2+ and MIT
URL:		https://poppler.freedesktop.org/
Source0:	https://poppler.freedesktop.org/poppler-%{version}.tar.xz

# https://bugzilla.redhat.com/show_bug.cgi?id=1185007
Patch0:		poppler-0.30.0-rotated-words-selection.patch
Patch1:		poppler-0.90.0-position-independent-code.patch
# Bogus volatiles detected by gcc-11
Patch2:		%{sname}-gcc11.patch
Patch3:		poppler-21.01.0-glib-introspection.patch

BuildRequires:	make
BuildRequires:	cmake
BuildRequires:	gcc-c++
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(cairo-ft)
BuildRequires:	pkgconfig(cairo-pdf)
BuildRequires:	pkgconfig(cairo-ps)
BuildRequires:	pkgconfig(cairo-svg)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gtk-doc)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libopenjp2)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(poppler-data)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Test)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Xml)

Requires:	pgdg-poppler-data

Obsoletes:	pgdg-poppler-glib-demos < 0.60.1-1

%description
%{name} is a PDF rendering library.

%package devel
Summary:	Libraries and headers for poppler
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
You should install the poppler-devel package if you would like to
compile applications based on poppler.

%package glib
Summary:	Glib wrapper for poppler
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description glib
%{summary}.

%package glib-devel
Summary:	Development files for glib wrapper
Requires:	%{name}-glib%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
Suggests:	%{name}-doc = %{version}-%{release}

%description glib-devel
%{summary}.

%package glib-doc
Summary:	Documentation for glib wrapper
BuildArch:	noarch

%description glib-doc
%{summary}.

%package qt5
Summary:	Qt5 wrapper for poppler
Requires:	%{name}%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-qt < 0.90.0-9
%description qt5
%{summary}.

%package qt5-devel
Summary:	Development files for Qt5 wrapper
Requires:	%{name}-qt5%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
Requires:	qt5-qtbase-devel
Obsoletes:	%{name}-qt-devel < 0.90.0-9
%description qt5-devel
%{summary}.

%package cpp
Summary:	Pure C++ wrapper for poppler
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description cpp
%{summary}.

%package cpp-devel
Summary:	Development files for C++ wrapper
Requires:	%{name}-cpp%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description cpp-devel
%{summary}.

%package utils
Summary:	Command line utilities for converting PDF files
Requires:	%{name}%{?_isa} = %{version}-%{release}
%description utils
Command line tools for manipulating PDF files and converting them to
other formats.

%prep
%autosetup -p1 -n %{sname}-%{version}

chmod -x poppler/CairoFontEngine.cc

%build
%cmake \
	-DCMAKE_INSTALL_PREFIX=/usr/pgdg-poppler \
	-DENABLE_CMS=lcms2 \
	-DENABLE_DCTDECODER=libjpeg \
	-DENABLE_GTK_DOC=ON \
	-DENABLE_LIBOPENJPEG=openjpeg2 \
	-DENABLE_UNSTABLE_API_ABI_HEADERS=ON \
	-DENABLE_ZLIB=OFF \
	..
%cmake_build

%install
%cmake_install

%ldconfig_scriptlets

%ldconfig_scriptlets glib

%ldconfig_scriptlets qt5

%ldconfig_scriptlets cpp

%files
%doc README.md
%license COPYING
%{popplerinstdir}/lib64/libpoppler.so.106*

%files devel
%{popplerinstdir}/lib64/pkgconfig/poppler.pc
%{popplerinstdir}/lib64/libpoppler.so
%dir %{popplerinstdir}/include/poppler/
# xpdf headers
%{popplerinstdir}/include/poppler/*.h
%{popplerinstdir}/include/poppler/fofi/
%{popplerinstdir}/include/poppler/goo/
%{popplerinstdir}/include/poppler/splash/

%files glib
%{popplerinstdir}/lib64/libpoppler-glib.so.8*
%{popplerinstdir}/lib64/girepository-1.0/Poppler-0.18.typelib

%files glib-devel
%{popplerinstdir}/lib64/pkgconfig/poppler-glib.pc
%{popplerinstdir}/lib64/libpoppler-glib.so
%{popplerinstdir}/share/gir-1.0/Poppler-0.18.gir
%{popplerinstdir}/include/poppler/glib/

%files glib-doc
%license COPYING
%{popplerinstdir}/share/gtk-doc/

%files qt5
%{popplerinstdir}/lib64/libpoppler-qt5.so.1*

%files qt5-devel
%{popplerinstdir}/lib64/libpoppler-qt5.so
%{popplerinstdir}/lib64/pkgconfig/poppler-qt5.pc
%{popplerinstdir}/include/poppler/qt5/

%files cpp
%{popplerinstdir}/lib64/libpoppler-cpp.so.0*

%files cpp-devel
%{popplerinstdir}/lib64/pkgconfig/poppler-cpp.pc
%{popplerinstdir}/lib64/libpoppler-cpp.so
%{popplerinstdir}/include/poppler/cpp

%files utils
%{popplerinstdir}/bin/pdf*
%{popplerinstdir}/share/man/man1/*

%changelog
* Wed May 19 2021 Devrim Gündüz <devrim@gunduz.org> - 21.01.0-6
- Initial packaging for PostgreSQL RPM repository, to prevent
  further brekages caused by Poppler updates on RHEL 8.x
