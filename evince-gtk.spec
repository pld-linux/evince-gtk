#
# - are schemas (thus GConf) needed?
#
# Conditional build:
%bcond_without	dbus		# disable DBUS support
%bcond_without	apidocs		# disable gtk-doc
#
Summary:	Document viewer for multiple document formats -- the no libgnome version
Summary(pl.UTF-8):	Przeglądarka dokumentów w wielu formatach -- wersja nie wykorzystująca libgnome
%define		_realname	evince
Name:		evince-gtk
Version:	2.29.5
Release:	1
License:	GPL v2
Group:		X11/Applications/Graphics
Source0:	http://ftp.gnome.org/pub/gnome/sources/evince/2.29/%{_realname}-%{version}.tar.bz2
# Source0-md5:	6b847d060fe3cbe96a156f82a28ee4d9
URL:		http://www.gnome.org/projects/evince/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_dbus:BuildRequires:	dbus-glib-devel >= 0.71}
BuildRequires:	djvulibre-devel >= 3.5.17
BuildRequires:	ghostscript
%{?with_apidocs:BuildRequires:	gnome-doc-utils >= 0.3.2}
BuildRequires:	gtk+2-devel >= 2:2.10.6
BuildRequires:	intltool >= 0.35.0
BuildRequires:	kpathsea-devel
BuildRequires:	libglade2-devel >= 1:2.6.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libxslt-progs >= 1.1.17
BuildRequires:	pkgconfig
BuildRequires:	poppler-glib-devel >= 0.6
BuildRequires:	python-libxml2
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	scrollkeeper
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk+2 >= 2:2.10.6
Requires(post,postun):	scrollkeeper
Requires:	cairo >= 1.2.4
Requires:	djvulibre >= 3.5.17
Requires:	gtk+2 >= 2:2.10.6
Requires:	poppler-glib >= 0.6
Conflicts:	evince
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         backendsdir     %{_libdir}/evince/2/backends

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

%package devel
Summary:        Header files for Evince GTK+
Summary(pl.UTF-8):      Pliki nagłówkowe Evince GTK+
Group:          X11/Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       gtk+2-devel >= 2:2.16.0

%description devel
Header files for Evince GTK+.

%description devel -l pl.UTF-8
Pliki nagłówkowe Evince GTK+.

%prep
%setup -q -n %{_realname}-%{version}

%build
%{__intltoolize}
%{__aclocal}
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

%{__rm} $RPM_BUILD_ROOT%{backendsdir}/*.la

%find_lang %{_realname}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post
%scrollkeeper_update_post
%update_icon_cache hicolor

%preun

%postun
/sbin/ldconfig
%update_desktop_database_postun
%scrollkeeper_update_postun
%update_icon_cache hicolor

%files -f %{_realname}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/evince
%attr(755,root,root) %{_bindir}/evince-previewer
%attr(755,root,root) %{_bindir}/evince-thumbnailer
%attr(755,root,root) %{_libdir}/libevdocument.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libevdocument.so.2
%attr(755,root,root) %{_libdir}/libevview.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libevview.so.2
%attr(755,root,root) %{_libdir}/evinced
%attr(755,root,root) %{_libdir}/evince-convert-metadata
%dir %{_libdir}/%{_realname}
%dir %{_libdir}/%{_realname}/2
%dir %{backendsdir}
%{backendsdir}/comicsdocument.evince-backend
%{backendsdir}/djvudocument.evince-backend
%{backendsdir}/dvidocument.evince-backend
%{backendsdir}/impressdocument.evince-backend
%{backendsdir}/pdfdocument.evince-backend
%{backendsdir}/pixbufdocument.evince-backend
%{backendsdir}/psdocument.evince-backend
%{backendsdir}/tiffdocument.evince-backend
%attr(755,root,root) %{backendsdir}/libcomicsdocument.so
%attr(755,root,root) %{backendsdir}/libdjvudocument.so 
%attr(755,root,root) %{backendsdir}/libdvidocument.so 
%attr(755,root,root) %{backendsdir}/libimpressdocument.so
%attr(755,root,root) %{backendsdir}/libpdfdocument.so
%attr(755,root,root) %{backendsdir}/libpixbufdocument.so
%attr(755,root,root) %{backendsdir}/libpsdocument.so
%attr(755,root,root) %{backendsdir}/libtiffdocument.so
%{_mandir}/man1/*
%{_datadir}/%{_realname}
%{_desktopdir}/*.desktop
%{_iconsdir}/*/*/*/*
%{_omf_dest_dir}/evince

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/*
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libevdocument.so
%attr(755,root,root) %{_libdir}/libevview.so
%{_libdir}/libevdocument.la
%{_libdir}/libevview.la
%dir %{_includedir}/%{_realname}
%dir %{_includedir}/%{_realname}/2.29
%dir %{_includedir}/%{_realname}/2.29/libdocument
%dir %{_includedir}/%{_realname}/2.29/libview
%{_includedir}/%{_realname}/2.29/*.h
%{_includedir}/%{_realname}/2.29/libdocument/*.h
%{_includedir}/%{_realname}/2.29/libview/*.h
%{_pkgconfigdir}/evince-document-*.pc
%{_pkgconfigdir}/evince-view-*.pc
