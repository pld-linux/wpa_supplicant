# TODO:
# - icon for wpa_gui
# - reverse madwifi bcond when appropriate packages will be available on ftp
#	/ as of madwifi-ng > r1499 and kernel > 2.6.14 wext driver could be
#	used instead of madwifi - so madwifi bcond will become obsolete soon /
# - syslog-support patch should be fixed and/or ripped from debian/ubuntu
#
# Conditional build
%bcond_without	dbus		# don't build D-BUS control interface
%bcond_without	gui		# don't build gui
%bcond_with	madwifi		# with madwifi support
#
# sync archlist with madwifi.spec
%ifnarch %{x8664} arm %{ix86} mips ppc xscale
%undefine	with_madwifi
%endif
#
Summary:	Linux WPA/WPA2/RSN/IEEE 802.1X supplicant
Summary(pl.UTF-8):	Suplikant WPA/WPA2/RSN/IEEE 802.1X dla Linuksa
Name:		wpa_supplicant
Version:	0.7.3
Release:	6
License:	GPL v2
Group:		Networking
Source0:	http://hostap.epitest.fi/releases/%{name}-%{version}.tar.gz
# Source0-md5:	f516f191384a9a546e3f5145c08addda
Source1:	%{name}.config
Source2:	%{name}-wpa_gui.desktop
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-OPTCFLAGS.patch
Patch2:		%{name}-lrelease.patch
Patch3:		%{name}-syslog-support.patch
# http://www.linuxwimax.org/Download
Patch4:		%{name}-0.7.2-generate-libeap-peer.patch
Patch5:		dbus-services.patch
Patch6:		bss-changed-prop-notify.patch
URL:		http://hostap.epitest.fi/wpa_supplicant/
%{?with_dbus:BuildRequires:	dbus-devel}
BuildRequires:	libnl-devel >= 1:2.0
%{?with_madwifi:BuildRequires:	madwifi-devel}
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
%if %{with gui}
BuildRequires:	QtGui-devel
BuildRequires:	qt4-linguist
BuildRequires:	qt4-build
BuildRequires:	qt4-qmake
%endif
BuildRequires:	readline-devel
BuildRequires:	sed >= 4.0
Requires:	rc-scripts >= 0.4.1.24
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%package -n wpa_gui
Summary:	Linux WPA/WPA2/RSN/IEEE 802.1X supplicant GUI
Summary(pl.UTF-8):	Graficzny interfejs suplikanta WPA/WPA2/RSN/IEEE 802.1X dla Linuksa
Group:		X11/Applications/Networking
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
%patch2 -p0
#patch3 -p0
%patch4 -p1
%patch5 -p1
%patch6 -p1

%{__sed} -i -e 's,@LIB@,%{_lib},' src/eap_peer/libeap0.pc

install %{SOURCE1} wpa_supplicant/.config

%if %{with dbus}
echo 'CONFIG_CTRL_IFACE_DBUS=y' >> wpa_supplicant/.config
echo 'CONFIG_CTRL_IFACE_DBUS_NEW=y' >> wpa_supplicant/.config
echo 'CONFIG_CTRL_IFACE_DBUS_INTRO=y' >> wpa_supplicant/.config
%endif

%if %{with madwifi}
echo 'CONFIG_DRIVER_MADWIFI=y' >> wpa_supplicant/.config
%endif

%build
%{__make} -C wpa_supplicant \
	V=1 \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags}" \
	OPTCFLAGS="%{rpmcppflags} %{rpmcflags}"

# eapol_test:
%{__make} -C wpa_supplicant eapol_test \
	V=1 \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags}" \
	OPTCFLAGS="%{rpmcppflags} %{rpmcflags}"

%if %{with gui}
cd wpa_supplicant/wpa_gui-qt4
qmake-qt4 -o Makefile wpa_gui.pro
cd ../..
%{__make} -C wpa_supplicant wpa_gui-qt4 \
	V=1 \
	QTDIR=%{_libdir}/qt4 \
	UIC=%{_bindir}/uic-qt4 \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	LDFLAGS="%{rpmldflags}" \
	OPTCFLAGS="%{rpmcppflags} %{rpmcflags}"
%endif

%{__make} -C src/eap_peer clean
%{__make} -C src/eap_peer \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags} -shared" \
	OPTCFLAGS="%{rpmcppflags} %{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man{5,8},%{_bindir},%{_sbindir},%{_desktopdir},/var/run/%{name},%{_sysconfdir}}

install wpa_supplicant/wpa_cli $RPM_BUILD_ROOT%{_sbindir}
install wpa_supplicant/wpa_passphrase $RPM_BUILD_ROOT%{_sbindir}
install wpa_supplicant/wpa_supplicant $RPM_BUILD_ROOT%{_sbindir}

install wpa_supplicant/wpa_supplicant.conf $RPM_BUILD_ROOT%{_sysconfdir}

install wpa_supplicant/doc/docbook/*.5 $RPM_BUILD_ROOT%{_mandir}/man5
install wpa_supplicant/doc/docbook/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

%if %{with dbus}
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/dbus-1/system.d,%{_datadir}/dbus-1/system-services}
install wpa_supplicant/dbus/dbus-wpa_supplicant.conf $RPM_BUILD_ROOT%{_sysconfdir}/dbus-1/system.d/wpa_supplicant.conf
install wpa_supplicant/dbus/*.service $RPM_BUILD_ROOT%{_datadir}/dbus-1/system-services
%endif

%if %{with gui}
install wpa_supplicant/wpa_gui-qt4/wpa_gui $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/wpa_gui.desktop
%endif

install wpa_supplicant/eapol_test $RPM_BUILD_ROOT%{_bindir}

%{__make} -C src/eap_peer install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBDIR=%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post -n libeap -p /sbin/ldconfig
%postun -n libeap -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc wpa_supplicant/{ChangeLog,README,eap_testing.txt,todo.txt}
%doc wpa_supplicant/{*wpa_supplicant.conf,examples}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/eapol_test
%attr(750,root,root) %ghost %dir /var/run/%{name}
%{_mandir}/man[58]/*
%if %{with dbus}
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/wpa_supplicant.conf
%{_datadir}/dbus-1/system-services/fi.epitest.hostap.WPASupplicant.service
%{_datadir}/dbus-1/system-services/fi.w1.wpa_supplicant1.service
%endif

%if %{with gui}
%files -n wpa_gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wpa_gui
%{_desktopdir}/wpa_gui.desktop
%endif

%files -n libeap
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libeap.so.*.*.*

%files -n libeap-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libeap.so
%{_includedir}/eap_peer
%{_pkgconfigdir}/libeap0.pc
