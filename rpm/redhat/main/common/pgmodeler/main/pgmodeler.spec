%global _privatelibs lib(objrenderer|parsers|pgconnector|pgmodeler|pgmodeler_ui|utils)\\.so
%global __provides_exclude (%{_privatelibs})
%global __requires_exclude (%{_privatelibs})

Name:		pgmodeler
Version:	1.0.6
Release:	1PGDG%{?dist}
Summary:	PostgreSQL Database Modeler
License:	GPLv3
URL:		http://pgmodeler.io/
Source0:	https://github.com/%{name}/%{name}/archive/v%{version}.tar.gz
Source2:	%{name}.desktop
Source3:	%{name}-mime-dbm.xml

Requires:	hicolor-icon-theme shared-mime-info libpq5
BuildRequires:	desktop-file-utils gettext libxml2-devel libpq5-devel

%if 0%{?suse_version} && 0%{?suse_version} >= 1400
BuildRequires:	libappstream-glib8 qt6-base-devel qt6-svg-devel qt6-macros
%else
BuildRequires:	qt6-qtbase-devel qt6-qtsvg-devel qt6-rpm-macros libappstream-glib
%endif

%description
PostgreSQL Database Modeler, or simply, pgModeler is an
open source tool for modeling databases that merges the classical
concepts of entity-relationship diagrams with specific features that
only PostgreSQL implements. The pgModeler translates the models created
by the user to SQL code and apply them onto database clusters (Version
9.x).

%prep
%setup -q -n %{name}-%{version}

%build

# @TODO Due to the bug (https://github.com/pgmodeler/pgmodeler/issues/559) CONFDIR, LANGDIR, SAMPLESDIR, SCHEMASDIR seems ignored?
# SHAREDIR=%%{_sharedstatedir}/%%{name} \
# CONFDIR=%%{_sysconfdir}/%%{name} \
# LANGDIR=%%{_datadir}/locale \
# SCHEMASDIR=%%{_sysconfdir}/%%{name} \
%qmake_qt6 \
 PREFIX=%{_prefix} \
 BINDIR=%{_bindir} \
 PRIVATEBINDIR=%{_libexecdir} \
 PLUGINSDIR=%{_libdir}/%{name}/plugins \
 SHAREDIR=%{_datarootdir}/%{name} \
 DOCDIR=%{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}} \
 PRIVATELIBDIR=%{_libdir}/%{name} \
  %{name}.pro

%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

desktop-file-install --mode 644 --dir %{buildroot}%{_datadir}/applications/ %{SOURCE2}
# icon, mime and menu-entry
%{__install} -p -dm 755 %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/ %{buildroot}%{_datadir}/mime/packages/
%{__install} -p -m 644 libs/libgui/res/icons/%{name}_logo.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/
%{__install} -p -m 644 %{SOURCE3} %{buildroot}%{_datadir}/mime/packages/%{name}.xml
# https://github.com/pgmodeler/pgmodeler/issues/783
%{__mkdir} -p %{buildroot}%{_libdir}/%{name}/plugins

%{__install} -Dp -m 644 %{name}.appdata.xml %{buildroot}/%{_datadir}/appdata/%{name}.appdata.xml
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/%{name}.appdata.xml

# License installed separately
%{__rm} -f %{buildroot}/%{_docdir}/%{name}/LICENSE

%files
%doc CHANGELOG.md README.md RELEASENOTES.md
%license LICENSE
%{_bindir}/%{name}
%{_bindir}/%{name}-cli
%{_libexecdir}/%{name}-*
# %%{_libdir}/%%{name}/lib*.so are not devel files! All in subdirectory and needs to load plugins only
%{_libdir}/%{name}
%{_datarootdir}/%{name}
%{_datadir}/icons/hicolor/256x256/apps/pgmodeler_logo.png
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml

%changelog
* Wed Oct 18 2023 Devrim Gündüz <devrim@gunduz.org> 1.0.6-1PGDG
- Update to 1.0.6

* Wed Aug 2 2023 Devrim Gündüz <devrim@gunduz.org> 1.0.5-1PGDG
- Update to 1.0.5
- Add PGDG branding

* Tue Apr 18 2023 Devrim Gündüz <devrim@gunduz.org> 1.0.2-2
- Add SLES 15 support
- Remove no longer needed dependencies.

* Wed Apr 12 2023 Devrim Gündüz <devrim@gunduz.org> 1.0.2-1
- Update to 1.0.2
- Build with QT6, as this new version require it.

* Tue Feb 8 2022 Devrim Gündüz <devrim@gunduz.org> 0.9.4-1
- Update to 0.9.4

* Thu Mar 11 2021 Devrim Gündüz <devrim@gunduz.org> 0.9.3-1
- Update to 0.9.3

* Sun Nov 15 2020 Devrim Gündüz <devrim@gunduz.org> 0.9.3-beta1-1
- Initial packaging for PostgreSQL RPM repository. This is an improved
  version of the spec file written by Pavel Alexeev <Pahan@Hubbitus.info
  for Fedora.
