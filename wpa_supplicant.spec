# TODO:
# - consider using CONFIG_PRIVSEP
# - icon for wpa_gui
#
# Conditional build
%bcond_without	dbus		# D-BUS control interface
%bcond_without	gui		# GUI (wpa_gui) package
%bcond_with	pcsc		# PC/SC support for smartcards
%bcond_without	qt5		# use Qt 5 instead of Qt 4

Summary:	Linux WPA/WPA2/RSN/IEEE 802.1X supplicant
Summary(pl.UTF-8):	Suplikant WPA/WPA2/RSN/IEEE 802.1X dla Linuksa
Name:		wpa_supplicant
Version:	2.10
Release:	2
License:	BSD
Group:		Networking
Source0:	http://w1.fi/releases/%{name}-%{version}.tar.gz
# Source0-md5:	d26797fcb002898d4ee989179346e1cc
Source1:	%{name}.config
Source2:	%{name}-wpa_gui.desktop
Source3:	%{name}.tmpfiles
Source4:	%{name}.service
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-gui-qt4.patch
# http://www.linuxwimax.org/Download
Patch2:		%{name}-0.7.2-generate-libeap-peer.patch
Patch3:		dbus-services.patch
URL:		http://w1.fi/wpa_supplicant/
%{?with_dbus:BuildRequires:	dbus-devel}
BuildRequires:	libnl-devel >= 1:3.5
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
%{?with_pcsc:BuildRequires:	pcsc-lite-devel}
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.647
%if %{with gui}
%if %{with qt5}
BuildRequires:	Qt5Gui-devel >= 5
BuildRequires:	Qt5Widgets-devel >= 5
BuildRequires:	qt5-build >= 5
BuildRequires:	qt5-linguist >= 5.13.0-3
BuildRequires:	qt5-qmake >= 5
%else
BuildRequires:	QtGui-devel >= 4
BuildRequires:	qt4-build >= 4
BuildRequires:	qt4-linguist >= 4
BuildRequires:	qt4-qmake >= 4
%endif
%endif
BuildRequires:	readline-devel
BuildRequires:	sed >= 4.0
Requires:	rc-scripts >= 0.4.1.24
Requires:	systemd-units >= 38
Suggests:	%{name}-utils = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qtver	%{?with_qt5:5}%{!?with_qt5:4}

%description
wpa_supplicant is a WPA Supplicant with support for WPA and WPA2 (IEEE
802.11i / RSN). Supplicant is the IEEE 802.1X/WPA component that is
used in the client stations. It implements key negotiation with a WPA
Authenticator and it controls the roaming and IEEE 802.11
authentication/association of the wlan driver.

wpa_supplicant is designed to be a "daemon" program that runs in the
background and acts as the backend component controlling the wireless
connection. Support for separate frontend programs is included and an
example text-based frontend, wpa_cli, is included with wpa_supplicant.

Supported WPA/IEEE 802.11i features:
- WPA-PSK ("WPA-Personal")
- WPA with EAP (e.g., with RADIUS authentication server)
  ("WPA-Enterprise") (currently, EAP-TLS and EAP-PEAP/MSCHAPv2 are
  supported with an integrated IEEE 802.1X Supplicant; other EAP types
  may be used with an external program, Xsupplicant)
- key management for CCMP, TKIP, WEP104, WEP40
- RSN/WPA2 (IEEE 802.11i)

%description -l pl.UTF-8
wpa_supplicant to suplikant WPA z obsługą WPA oraz WPA2 (IEEE 802.11i
/ RSN). Suplikant to element IEEE 802.1X/WPA używany na stacjach
klienckich. Implementuje negocjację kluczy z elementem
uwierzytelniającym WPA (WPA Authenticator) i kontroluje roaming oraz
uwierzytelnianie/kojarzenie sterownika wlan zgodnie z IEEE 802.11.

wpa_supplicant jest zaprojektowany tak, by był wspólnym programem
działającym w tle i działa jako element backendu sterujący połączeniem
bezprzewodowym. Dostępna jest obsługa oddzielnych programów
frontendowych, a w pakiecie wpa_supplicant załączony jest prosty
frontend tekstowy - wpa_cli.

Obsługiwane możliwości WPA/IEEE 802.11i:
- WPA-PSK ("WPA-Personal")
- WPA z EAP (np. z serwerem uwierzytleniającym RADIUS)
  ("WPA-Enterprise") (aktualnie EAP-TLS i EAP-PEAP/MSCHAPv2 są
  obsługiwane przez załączonego suplikanta IEEE 802.1X; inne rodzaje EAP
  mogą być używane przez zewnętrzny program - Xsupplicant)
- zarządzanie kluczy dla CCMP, TKIP, WEP104, WEP40
- RSN/WPA2 (IEEE 802.11i)

%package utils
Summary:	wpa_supplicant utilities
Summary(pl.UTF-8):	Narzędzia dla wpa_supplicant

%description utils
wpa_supplicant utilities.

%description utils -l pl.UTF-8
Narzędzia dla wpa_supplicant.

%package -n wpa_gui
Summary:	Linux WPA/WPA2/RSN/IEEE 802.1X supplicant GUI
Summary(pl.UTF-8):	Graficzny interfejs suplikanta WPA/WPA2/RSN/IEEE 802.1X dla Linuksa
Group:		X11/Applications/Networking
Requires(post,postun):	desktop-file-utils
Requires:	%{name} = %{version}-%{release}

%description -n wpa_gui
Linux WPA/WPA2/RSN/IEEE 802.1X supplicant GUI.

%description -n wpa_gui -l pl.UTF-8
Graficzny interfejs suplikanta WPA/WPA2/RSN/IEEE 802.1X dla Linuksa.

%package -n libeap
Summary:	EAP Peer library
Summary(pl.UTF-8):	Biblioteka EAP Peer
Group:		Libraries

%description -n libeap
EAP Peer library.

%description -n libeap -l pl.UTF-8
Biblioteka EAP Peer.

%package -n libeap-devel
Summary:	Development files for eap library
Summary(pl.UTF-8):	Pliki programistyczne dla biblioteki eap
Group:		Development/Libraries
Requires:	libeap = %{version}-%{release}

%description -n libeap-devel
Development files for eap library.

%description -n libeap-devel -l pl.UTF-8
Pliki programistyczne dla biblioteki eap.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%{__sed} -i -e 's,@LIB@,%{_lib},' src/eap_peer/libeap0.pc

cp -p %{SOURCE1} wpa_supplicant/.config

%if %{with dbus}
echo 'CONFIG_CTRL_IFACE_DBUS=y' >> wpa_supplicant/.config
echo 'CONFIG_CTRL_IFACE_DBUS_NEW=y' >> wpa_supplicant/.config
echo 'CONFIG_CTRL_IFACE_DBUS_INTRO=y' >> wpa_supplicant/.config
%endif

%if %{with pcsc}
echo 'CONFIG_PCSC=y' >> wpa_supplicant/.config
echo 'CONFIG_EAP_SIM=y' >> wpa_supplicant/.config
echo 'CONFIG_EAP_AKA=y' >> wpa_supplicant/.config
echo 'CONFIG_EAP_AKA_PRIME=y' >> wpa_supplicant/.config
%endif

%build
CFLAGS="%{rpmcppflags} %{rpmcflags}" \
%{__make} -C wpa_supplicant \
	V=1 \
	CC="%{__cc}" \
	BINDIR="%{_sbindir}" \
	LDFLAGS="%{rpmldflags}"

# eapol_test:
CFLAGS="%{rpmcppflags} %{rpmcflags}" \
%{__make} -C wpa_supplicant eapol_test \
	V=1 \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags}"

%if %{with gui}
cd wpa_supplicant/wpa_gui-qt4
qmake-qt%{qtver} -o Makefile wpa_gui.pro \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags}" \
	QMAKE_LFLAGS_RELEASE="%{rpmldflags}"
cd ../..
%{__make} -C wpa_supplicant wpa_gui-qt4 \
	V=1 \
	QTDIR=%{_libdir}/qt%{qtver} \
	QMAKE='qmake-qt%{qtver}' \
	LRELEASE='%{_libdir}/qt%{qtver}/bin/lrelease' \
	UIC=%{_bindir}/uic-qt%{qtver}
%endif

%{__make} -C src/eap_peer -f Makefile.libeap clean
%{__make} -C src/eap_peer -f Makefile.libeap \
	CC="%{__cc}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags} -MMD -Wall $(pkg-config --cflags libnl-3.0) -DTLS_DEFAULT_CIPHERS=\\\"PROFILE=SYSTEM:3DES\\\"" \
	LDFLAGS="%{rpmldflags} -shared"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man{5,8},%{_bindir},%{_sbindir},%{_desktopdir},/var/run/%{name},%{_sysconfdir}} \
	$RPM_BUILD_ROOT{%{systemdtmpfilesdir},%{systemdunitdir}}

install -p wpa_supplicant/wpa_cli $RPM_BUILD_ROOT%{_sbindir}
install -p wpa_supplicant/wpa_passphrase $RPM_BUILD_ROOT%{_bindir}
install -p wpa_supplicant/wpa_supplicant $RPM_BUILD_ROOT%{_sbindir}

cp -p wpa_supplicant/wpa_supplicant.conf $RPM_BUILD_ROOT%{_sysconfdir}

cp -p wpa_supplicant/doc/docbook/*.5 $RPM_BUILD_ROOT%{_mandir}/man5
cp -p wpa_supplicant/doc/docbook/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

# program exists with CONFIG_PRIVSEP only
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man8/wpa_priv.8

%if %{with dbus}
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/dbus-1/system.d,%{_datadir}/dbus-1/system-services}
cp -p wpa_supplicant/dbus/dbus-wpa_supplicant.conf $RPM_BUILD_ROOT%{_sysconfdir}/dbus-1/system.d/wpa_supplicant.conf
cp -p wpa_supplicant/dbus/*.service $RPM_BUILD_ROOT%{_datadir}/dbus-1/system-services
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service
%endif

%if %{with gui}
install -p wpa_supplicant/wpa_gui-qt4/wpa_gui $RPM_BUILD_ROOT%{_bindir}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/wpa_gui.desktop
%endif

install -p wpa_supplicant/eapol_test $RPM_BUILD_ROOT%{_bindir}
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

%{__make} -C src/eap_peer -f Makefile.libeap install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBDIR=%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post wpa_supplicant.service

%preun
%systemd_preun wpa_supplicant.service

%postun
%systemd_reload

%post -n wpa_gui
%update_desktop_database_post

%postun -n wpa_gui
%update_desktop_database_postun

%post	-n libeap -p /sbin/ldconfig
%postun	-n libeap -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING wpa_supplicant/{ChangeLog,README,README-{HS20,P2P,WPS},eap_testing.txt,todo.txt,*wpa_supplicant.conf,examples}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(755,root,root) %{_bindir}/eapol_test
%attr(755,root,root) %{_sbindir}/wpa_cli
%attr(755,root,root) %{_sbindir}/wpa_supplicant
%attr(750,root,root) %ghost %dir /var/run/%{name}
%{systemdtmpfilesdir}/%{name}.conf
%{_mandir}/man5/wpa_supplicant.conf.5*
%{_mandir}/man8/eapol_test.8*
%{_mandir}/man8/wpa_background.8*
%{_mandir}/man8/wpa_cli.8*
%{_mandir}/man8/wpa_supplicant.8*
%if %{with dbus}
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/wpa_supplicant.conf
%{_datadir}/dbus-1/system-services/fi.w1.wpa_supplicant1.service
%{systemdunitdir}/%{name}.service
%endif

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wpa_passphrase
%{_mandir}/man8/wpa_passphrase.8*

%if %{with gui}
%files -n wpa_gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wpa_gui
%{_mandir}/man8/wpa_gui.8*
%{_desktopdir}/wpa_gui.desktop
%endif

%files -n libeap
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libeap.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libeap.so.0

%files -n libeap-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libeap.so
%{_includedir}/eap_peer
%{_pkgconfigdir}/libeap0.pc
