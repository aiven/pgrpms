%global sname postgresql_faker

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	Fake Data Generator for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	0.4.0
Release:	1%{?dist}
License:	PostgreSQL
Source0:	https://gitlab.com/dalibo/%{sname}/-/archive/%{version}/%{sname}-%{version}.tar.bz2
URL:		https://gitlab.com/dalibo/%{sname}
BuildArch:	noarch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server
Requires:	postgresql%{pgmajorversion}-plpython3
%if 0%{?fedora} || 0%{?rhel} >= 7
Requires:	python3-faker
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1499
Requires:	python3-Faker
%endif
%endif

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
postgresql_faker is a PostgreSQL extension based on the awesome Python Faker
Library. This is useful to generate random-but-meaningful datasets for
functionnal testing, anonymization, training data, etc...

This extension is simply a wrapper written in pl/python procedural language.

%prep
%setup -q -n %{sname}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
# Just a workaround until next version is out.
# https://gitlab.com/dalibo/postgresql_faker/-/issues/13
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension/
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE.md
%else
%license LICENSE.md
%endif
%defattr(644,root,root,755)
%{pginstdir}/share/extension/faker--*.sql
%{pginstdir}/share/extension/faker.control
%doc %{pginstdir}/doc/extension/README-%{sname}.md

%changelog
* Wed May 19 2021 Devrim Gündüz <devrim@gunduz.org> - 0.4.0
- Update to 0.4.0

* Mon Apr 26 2021 Devrim Gündüz <devrim@gunduz.org> - 0.3.0
- Initial packaging for PostgreSQL RPM Repository
