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
Version:	0.9.3
Release:	1
License:	GPL v2
Group:		X11/Applications/Graphics
Source0:	http://ftp.gnome.org/pub/gnome/sources/evince/0.9/%{_realname}-%{version}.tar.bz2
# Source0-md5:	64259f5b7084f5c98b463eb42b000114
Patch0:		%{_realname}-desktop.patch
Patch1:		%{_realname}-gs8.patch
URL:		http://www.gnome.org/projects/evince/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_dbus:BuildRequires:	dbus-glib-devel >= 0.71}
BuildRequires:	djvulibre-devel >= 3.5.17
BuildRequires:	ghostscript
BuildRequires:	gtk+2-devel >= 2:2.10.6
BuildRequires:	intltool >= 0.35.0
BuildRequires:	kpathsea-devel
BuildRequires:	libglade2-devel >= 1:2.6.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libxslt-progs >= 1.1.17
BuildRequires:	pkgconfig
BuildRequires:	poppler-glib-devel >= 0.5.9
BuildRequires:	python-libxml2
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	scrollkeeper
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk+2 >= 2:2.10.6
Requires(post,postun):	scrollkeeper
Requires:	cairo >= 1.2.4
Requires:	djvulibre >= 3.5.17
Requires:	gtk+2 >= 2:2.10.6
Requires:	poppler-glib >= 0.5.9
Conflicts:	evince
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%prep
%setup -q -n %{_realname}-%{version}
%patch0 -p1
%patch1 -p1

%build
#%%{__intltoolize}
#%%{__aclocal}
#%%{__autoconf}
#%%{__autoheader}
#%%{__automake}
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
	--with-print=gtk \
	--with-html-dir=%{_gtkdocdir} \
	--without-libgnome

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}

%find_lang %{_realname}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%scrollkeeper_update_post
%update_icon_cache hicolor

%preun

%postun
%update_desktop_database_postun
%scrollkeeper_update_postun
%update_icon_cache hicolor

%files -f %{_realname}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*
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
