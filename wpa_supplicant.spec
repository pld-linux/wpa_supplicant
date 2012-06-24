# TODO:
# - wpa_gui can be built with qt4 - bcond?
# - icon for wpa_gui
# - reverse madwifi bcond when appropriate packages will be available on ftp
#	/ as of madwifi-ng > r1499 and kernel > 2.6.14 wext driver could be 
#	used instead of madwifi - so madwifi bcond will become obsolete soon /
#
# Conditional build
%bcond_with	madwifi		# with madwifi support
%bcond_without	gui		# don't build gui
#
# sync archlist with madwifi.spec
%ifnarch %{x8664} arm %{ix86} mips ppc xscale
%undefine	with_madwifi
%endif
#
Summary:	Linux WPA/WPA2/RSN/IEEE 802.1X supplicant
Summary(pl.UTF-8):   Suplikant WPA/WPA2/RSN/IEEE 802.1X dla Linuksa
Name:		wpa_supplicant
Version:	0.5.7
Release:	1
License:	GPL v2
Group:		Networking
Source0:	http://hostap.epitest.fi/releases/%{name}-%{version}.tar.gz
# Source0-md5:	bd2436392ad3c6d2513da701a12f2d27
Source1:	%{name}.config
Source2:	%{name}-wpa_gui.desktop
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-0.4.7_dscape-02.patch
Patch2:		%{name}-OPTCFLAGS.patch
Patch3:		%{name}-kill-dynamic_eap_methods.patch
URL:		http://hostap.epitest.fi/wpa_supplicant/
%{?with_madwifi:BuildRequires:	madwifi-devel}
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
%if %{with gui}
BuildRequires:	qmake
BuildRequires:	qt-devel
%endif
BuildRequires:	readline-devel
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
Summary(pl.UTF-8):   Graficzny interfejs suplikanta WPA/WPA2/RSN/IEEE 802.1X dla Linuksa
Group:		X11/Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description -n wpa_gui
Linux WPA/WPA2/RSN/IEEE 802.1X supplicant GUI.

%description -n wpa_gui -l pl.UTF-8
Graficzny interfejs suplikanta WPA/WPA2/RSN/IEEE 802.1X dla Linuksa.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

install %{SOURCE1} .config

%if %{with madwifi}
echo 'CONFIG_DRIVER_MADWIFI=y' >> .config
%endif

%build
%{__make} \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags}" \
	OPTCFLAGS="%{rpmcflags}"

%if %{with gui}
%{__make} wpa_gui \
	QTDIR=/usr \
	UIC=%{_bindir}/uic \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	LDFLAGS="%{rpmldflags}" \
	OPTCFLAGS="%{rpmcflags}"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man{5,8},%{_bindir},%{_desktopdir},/var/run/%{name}}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install doc/docbook/*.5 $RPM_BUILD_ROOT%{_mandir}/man5
install doc/docbook/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

%if %{with gui}
install wpa_gui/wpa_gui $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/wpa_gui.desktop
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README eap_testing.txt todo.txt
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(755,root,root) %{_sbindir}/*
%attr(750,root,root) %dir /var/run/%{name}
%{_mandir}/man[58]/*

%if %{with gui}
%files -n wpa_gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wpa_gui
%{_desktopdir}/wpa_gui.desktop
%endif
