# NOTE: for more rencent versions see evince.spec, just without nautilus extensions
#
# - are schemas (thus GConf) needed?
#
# Conditional build:
%bcond_without	dbus		# disable DBUS support
%bcond_without	apidocs		# disable gtk-doc

%define		realname	evince
Summary:	Document viewer for multiple document formats -- the no libgnome version
Summary(pl.UTF-8):	Przeglądarka dokumentów w wielu formatach -- wersja nie wykorzystująca libgnome
Name:		evince-gtk
Version:	3.0.2
Release:	4
License:	GPL v2+
Group:		X11/Applications/Graphics
Source0:	http://ftp.gnome.org/pub/GNOME/sources/evince/3.0/%{realname}-%{version}.tar.bz2
# Source0-md5:	4eff790d9ba7a0d9e8eda5b4bb91c92b
URL:		http://www.gnome.org/projects/evince/
BuildRequires:	GConf2-devel
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake >= 1.10
BuildRequires:	cairo-devel >= 1.10.0
%{?with_dbus:BuildRequires:	dbus-glib-devel >= 0.71}
BuildRequires:	djvulibre-devel >= 3.5.17
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	ghostscript
BuildRequires:	glib2-devel >= 2.26.0
BuildRequires:	gnome-common
%{?with_apidocs:BuildRequires:	gnome-doc-utils >= 0.3.2}
BuildRequires:	gnome-icon-theme
BuildRequires:	gtk+3-devel >= 3.0.2
BuildRequires:	gtk-doc-automake
BuildRequires:	intltool >= 0.35.0
BuildRequires:	kpathsea-devel
BuildRequires:	lcms-devel
BuildRequires:	libglade2-devel >= 1:2.6.0
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libspectre-devel >= 0.2.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool
BuildRequires:	libxml2-progs
BuildRequires:	libxslt-progs >= 1.1.17
BuildRequires:	pkgconfig
BuildRequires:	poppler-glib-devel >= 0.14.0
BuildRequires:	python-libxml2
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	scrollkeeper
BuildRequires:	xorg-lib-libSM-devel
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	scrollkeeper
Requires:	cairo >= 1.2.4
Requires:	djvulibre >= 3.5.17
Requires:	gtk+3 >= 3.0.2
Requires:	poppler-glib >= 0.6
Conflicts:	evince
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		backendsdir	%{_libdir}/evince/3/backends

%description
Evince is a document viewer for multiple document formats like pdf,
postscript, and many others. The goal of evince is to replace the
multiple document viewers that exist on the GNOME Desktop, like ggv,
gpdf, and xpdf with a single simple application.

This version doesn't use GNOME libraries, but only GTK+.

%description -l pl.UTF-8
Evince jest przeglądarką dokumentów w wielu formatach takich jak pdf,
postscript i wielu innych. W zamierzeniach program ma zastąpić
przeglądarki dokumentów dla środowiska GNOME, takie jak ggv, gpdf i
xpdf jedną prostą aplikacją.

Ta wersja nie korzysta z bibliotek GNOME, a jedynie z GTK+.

%package devel
Summary:	Header files for Evince GTK+
Summary(pl.UTF-8):	Pliki nagłówkowe Evince GTK+
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gtk+3-devel >= 3.0.2

%description devel
Header files for Evince GTK+.

%description devel -l pl.UTF-8
Pliki nagłówkowe Evince GTK+.

%package apidocs
Summary:	Evince API documentation
Summary(pl.UTF-8):	Dokumentacja API aplikacji Evince
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
Evince API documentation.

This version doesn't use GNOME libraries, but only GTK+.

%description apidocs -l pl.UTF-8
Dokumentacja API aplikacji Evince.

Ta wersja nie korzysta z bibliotek GNOME, a jedynie z GTK+.

%prep
%setup -q -n %{realname}-%{version}

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_apidocs:--disable-gtk-doc} \
	%{!?with_apidocs:--disable-scrollkeeper} \
	--disable-nautilus \
	--disable-static \
	--disable-schemas-install \
	--enable-comics \
	%{!?with_dbus:--disable-dbus} \
	--enable-djvu \
	--enable-dvi \
	--enable-impress \
	--enable-pdf \
	--enable-pixbuf \
	--enable-ps \
	--enable-t1lib \
	--enable-thumbnailer \
	--enable-tiff \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{backendsdir}/*.la

%find_lang %{realname}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post
%scrollkeeper_update_post
%update_icon_cache hicolor

%postun
/sbin/ldconfig
%update_desktop_database_postun
%scrollkeeper_update_postun
%update_icon_cache hicolor

%files -f %{realname}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/evince
%attr(755,root,root) %{_bindir}/evince-previewer
%attr(755,root,root) %{_bindir}/evince-thumbnailer
%attr(755,root,root) %{_libdir}/libevdocument3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libevdocument3.so.3
%attr(755,root,root) %{_libdir}/libevview3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libevview3.so.3
%dir %{_libdir}/evince
%dir %{_libdir}/evince/3
%dir %{backendsdir}
%attr(755,root,root) %{backendsdir}/libcomicsdocument.so
%{backendsdir}/comicsdocument.evince-backend
%attr(755,root,root) %{backendsdir}/libdjvudocument.so
%{backendsdir}/djvudocument.evince-backend
%attr(755,root,root) %{backendsdir}/libdvidocument.so*
%{backendsdir}/dvidocument.evince-backend
%attr(755,root,root) %{backendsdir}/libpdfdocument.so
%{backendsdir}/pdfdocument.evince-backend
%attr(755,root,root) %{backendsdir}/libpsdocument.so
%{backendsdir}/psdocument.evince-backend
%attr(755,root,root) %{backendsdir}/libtiffdocument.so
%{backendsdir}/tiffdocument.evince-backend
%{_mandir}/man1/*
%{_datadir}/%{realname}
%{_desktopdir}/*.desktop
%{_iconsdir}/*/*/*/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libevdocument3.so
%attr(755,root,root) %{_libdir}/libevview3.so
%{_includedir}/evince
%{_pkgconfigdir}/evince-document-*.pc
%{_pkgconfigdir}/evince-view-*.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/*
%endif
