%if (0%{?fedora})
%global _hardened_build 1
%endif
%global pgmajorversion 96
%global pginstdir /usr/pgsql-9.6
%global sname	pgadmin3

Summary:	Graphical client for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.22.1
Release:	2%{?dist}
License:	BSD
Source:		https://download.postgresql.org/pub/%{sname}/release/v%{version}/src/%{sname}-%{version}.tar.gz
Patch2:		%{sname}-desktop.patch
# Move this == null check to a static function.  This works, but I opted
# for the compiler flag since it "fixes" all cases, and pgadmin4 is on the
# way.
%if (0%{?fedora})
Patch3:		%{sname}-nullthis.patch
%endif
URL:		http://www.pgadmin.org/
%if 0%{?rhel} && 0%{?rhel} <= 5
Group:		Applications/Databases
%endif
BuildRequires:	wxGTK-devel postgresql%{pgmajorversion}-devel ImageMagick
BuildRequires:	desktop-file-utils openssl-devel libxml2-devel libxslt-devel
Requires:	wxGTK
Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

%description
pgAdmin III is a powerful administration and development
platform for the PostgreSQL database, free for any use.
It is designed to answer the needs of all users,
from writing simple SQL queries to developing complex
databases. The graphical interface supports all PostgreSQL
features and makes administration easy.

pgAdmin III is designed to answer the needs of all users,
from writing simple SQL queries to developing complex databases.
The graphical interface supports all PostgreSQL features and
makes administration easy. The application also includes a syntax
highlighting SQL editor, a server-side code editor, an
SQL/batch/shell job scheduling agent, support for the Slony-I
replication engine and much more. No additional drivers are
required to communicate with the database server.

%package docs
Summary:	Documentation for pgAdmin3
%if 0%{?rhel} && 0%{?rhel} <= 5
Group:		Applications/Databases
%endif
Requires:	%{sname}_%{pgmajorversion} = %{version}

%description docs
This package contains documentation for various languages,
which are in html format.

%prep
%setup -q -n %{sname}-%{version}

# touch to avoid autotools re-run
for f in configure{,.ac} ; do touch -r $f $f.stamp ; done
%patch2 -p0
%if (0%{?fedora})
%patch3 -p0
%endif
# extract 48x48 png from ico
convert "pgadmin/include/images/pgAdmin3.ico[3]" pgadmin/include/images/pgAdmin3-48.png

%build
# This is only for Fedora for now:
%if (0%{?fedora})
CFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
CXXFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
export CFLAGS
export CXXFLAGS
%endif
export LIBS="-lwx_gtk2u_core-2.8"
./configure --disable-debug --disable-dependency-tracking --with-wx-version=2.8 --with-wx=/usr --with-pgsql=%{pginstdir} --prefix=%{pginstdir}
%{__make} %{?_smp_mflags} all

%install
%{__rm} -rf %{buildroot}
%make_install DESTDIR=%{buildroot}

%{__mkdir} -p %{buildroot}%{_datadir}/%{name}/
for size in 16 32 48 ; do
	install -Dpm 644 pgadmin/include/images/pgAdmin3-$size.png \
	%{buildroot}/%{_datadir}/icons/hicolor/${size}x$size/apps/pgAdmin3.png
done

%{__mkdir} -p %{buildroot}/%{_datadir}/applications
%{__mv} ./pkg/%{sname}.desktop ./pkg/%{name}.desktop
desktop-file-install --vendor fedora --dir %{buildroot}/%{_datadir}/applications \
	--add-category X-Fedora\
	--add-category Application\
	--add-category Development\
	./pkg/%{name}.desktop

%clean
%{__rm} -rf %{buildroot}

%preun
if [ $1 = 0 ] ; then
	%{_sbindir}/update-alternatives --remove %{sname} %{pginstdir}/bin/%{sname}
fi

%post
%{_sbindir}/update-alternatives --install /usr/bin/%{sname} %{sname} %{pginstdir}/bin/%{sname} 960

%postun
if [ $1 -eq 0 ] ; then
	touch --no-create %{_datadir}/icons/hicolor &>/dev/null
	gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%if (0%{?fedora} || 0%{?rhel} > 6)
%license LICENSE
%endif
%doc BUGS CHANGELOG README
%{pginstdir}/bin/%{sname}
%{pginstdir}/share/%{sname}
%{_datadir}/applications/fedora-%{sname}_%{pgmajorversion}.desktop
%{_datadir}/icons/hicolor/16x16/apps/pgAdmin3.png
%{_datadir}/icons/hicolor/32x32/apps/pgAdmin3.png
%{_datadir}/icons/hicolor/48x48/apps/pgAdmin3.png

%files docs
%doc docs/*

%changelog
* Sat Sep 10 2016 Devrim GUNDUZ <devrim@gunduz.org> - 1.22.1-2
- Add a patch to fix crashes on Fedora 23+

* Wed Feb 17 2016 Devrim GUNDUZ <devrim@gunduz.org> - 1.22.1-1
- Update to 1.22.1
- Put Fedora-related compile flags into conditionals for unified spec file.

* Tue Jan 5 2016 Devrim GUNDUZ <devrim@gunduz.org> - 1.22.0-1
- Update to 1.22.0 Gold.

* Tue Nov 10 2015 Devrim GUNDUZ <devrim@gunduz.org> - 1.22.0-beta1-1
- Update to 1.22.0 beta1
- Add -fPIC and -pie to CFLAGS and CXXFLAGS, per Fedora 23 packaging
  requirements. This currently applies only to Fedora.
- Update download URL

* Tue Apr 28 2015 Devrim GUNDUZ <devrim@gunduz.org> - 1.20.0-3
- Install better icons, per Ville @ RH bugilla #1211723
- Mark LICENSE as %%license, per Ville @ RH bugilla #1211723
- omit deprecated Group: tags and %%clean section
- Use %%make_install macro
- Get rid of BuildRoot definition
- No need to cleanup buildroot during %%install
- Remove %%defattr
- Use more macros, where available.

* Mon Jan 5 2015 Devrim GUNDUZ <devrim@gunduz.org> 1.20.0-2
- Update/fix alternatives version.

* Mon Dec 15 2014 Devrim GUNDUZ <devrim@gunduz.org> 1.20.0-1
- Update to 1.20.0 Gold

* Wed Oct 15 2014 Devrim GUNDUZ <devrim@gunduz.org> 1.20.0-beta2-1
- Update to 1.20.0-beta2

* Thu Aug 28 2014 Devrim GUNDUZ <devrim@gunduz.org> 1.20.0-beta1-1
- Update to 1.20.0-beta1

* Tue Nov 19 2013 Devrim GUNDUZ <devrim@gunduz.org> 1.18.1-2
- Fix file paths, per #118.
- Fix alternatives version.

* Tue Oct 8 2013 Devrim GUNDUZ <devrim@gunduz.org> 1.18.1-1
- Update to 1.18.1

* Fri Aug 30 2013 Devrim GUNDUZ <devrim@gunduz.org> 1.18.0-1
- Update to 1.18.0 Gold

* Mon Feb 11 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.16.1-4
- More fixes to the %%preun section.

* Fri Jan 25 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.16.1-3
- Fix typo in init script.

* Wed Jan 23 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.16.1-2
- Fix %%post and %%postin issues.

* Mon Dec 10 2012 Devrim GUNDUZ <devrim@gunduz.org> 1.16.1-1
- Update to 1.16.1

* Thu Sep 6 2012 Devrim GUNDUZ <devrim@gunduz.org> 1.16.0-1
- Update to 1.16.0 Gold

* Tue Nov 15 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.14.0-3
- Fix paths in desktop file paths, per Stephen Blake. Also bump up the
  alternatives version..

* Mon Oct 31 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.14.0-2
-  Fix desktop file. Patch from Kim Bisgaard.

* Fri Sep 9 2011 Devrim GUNDUZ <devrim@gunduz.org> 1.14.0-1
- Update to 1.14.0 Gold

* Fri Apr 15 2011 Devrim GUNDUZ <devrim@gunduz.org> 1.12.3-1
- Update to 1.12.3

* Tue Dec 14 2010 Devrim GUNDUZ <devrim@gunduz.org> 1.12.2-2
- Update to 1.12.2

* Thu Oct 7 2010 Devrim GUNDUZ <devrim@gunduz.org> 1.12.1-1
- Update to 1.12.1

* Mon Sep 20 2010 Devrim GUNDUZ <devrim@gunduz.org> 1.12.0-1
- Update to 1.12.0
- Apply multiple postmaster specific changes and patch.
- Trim changelog.

* Tue Mar 9 2010 Devrim GUNDUZ <devrim@gunduz.org> 1.10.2-1
- Update to 1.10.2
- Improve configure line to support new multiple postmaster installation
  feature.

* Sat Dec 5 2009 Devrim GUNDUZ <devrim@gunduz.org> 1.10.1-1
- Update to 1.10.1

* Mon Jun 29 2009 Devrim GUNDUZ <devrim@gunduz.org> 1.10.0
- Update to 1.10.0 Gold

* Wed Mar 25 2009 Devrim GUNDUZ <devrim@gunduz.org> 1.10.0-beta2
- Update to 1.10.0 beta2

* Fri Mar 13 2009 Devrim GUNDUZ <devrim@gunduz.org> 1.10.0-beta1
- Update to 1.10.0 beta1
- Update patch0

* Tue Jul 15 2008 Devrim GUNDUZ <devrim@gunduz.org> 1.8.4-2
- Use $RPM_OPT_FLAGS, build with dependency tracking disabled
(#229054). Patch from Ville Skyttä

* Thu Jun 5 2008 Devrim GUNDUZ <devrim@gunduz.org> 1.8.4-1
- Update to 1.8.4

* Tue Jun 3 2008 Devrim GUNDUZ <devrim@gunduz.org> 1.8.3-1
- Update to 1.8.3

* Fri Feb 1 2008 Devrim GUNDUZ <devrim@gunduz.org> 1.8.2-1
- Update to 1.8.2

* Fri Jan 4 2008 Devrim GUNDUZ <devrim@gunduz.org> 1.8.1-1
- Update to 1.8.1

* Wed Dec 05 2007 Devrim GUNDUZ <devrim@gunduz.org> 1.8.0-2
- Rebuild for openssl bump

