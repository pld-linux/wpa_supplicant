Summary:	Linux WPA/WPA2/RSN/IEEE 802.1X supplicant
Summary(pl):	Suplikant WPA/WPA2/RSN/IEEE 802.1X dla Linuksa
Name:		wpa_supplicant
Version:	0.4.5
Release:	2
License:	GPL v2
Group:		Networking 
Source0:	http://hostap.epitest.fi/releases/%{name}-%{version}.tar.gz
# Source0-md5:	28347563119f09fc963bcdf9d16265a3
Source1:	%{name}.config
Patch0:		%{name}-makefile.patch
URL:		http://hostap.epitest.fi/wpa_supplicant/
BuildRequires:	madwifi-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	readline-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
wpa_supplicant is a WPA Supplicant with support for WPA and WPA2
(IEEE 802.11i / RSN). Supplicant is the IEEE 802.1X/WPA component
that is used in the client stations. It implements key negotiation
with a WPA Authenticator and it controls the roaming and IEEE 802.11
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

%description -l pl
wpa_supplicant to suplikant WPA z obs�ug� WPA oraz WPA2 (IEEE 802.11i
/ RSN). Suplikant to element IEEE 802.1X/WPA u�ywany na stacjach
klienckich. Implementuje negocjacj� kluczy z elementem
uwierzytelniaj�cym WPA (WPA Authenticator) i kontroluje roaming oraz
uwierzytelnianie/kojarzenie sterownika wlan zgodnie z IEEE 802.11.

wpa_supplicant jest zaprojektowany tak, by by� wsp�lnym programem
dzia�aj�cym w tle i dzia�a jako element backendu steruj�cy po��czeniem
bezprzewodowym. Dost�pna jest obs�uga oddzielnych program�w
frontendowych, a w pakiecie wpa_supplicant za��czony jest prosty
frontend tekstowy - wpa_cli.

Obs�ugiwane mo�liwo�ci WPA/IEEE 802.11i:
- WPA-PSK ("WPA-Personal")
- WPA z EAP (np. z serwerem uwierzytleniaj�cym RADIUS)
  ("WPA-Enterprise") (aktualnie EAP-TLS i EAP-PEAP/MSCHAPv2 s�
  obs�ugiwane przez za��czonego suplikanta IEEE 802.1X; inne rodzaje
  EAP mog� by� u�ywane przez zewn�trzny program - Xsupplicant)
- zarz�dzanie kluczy dla CCMP, TKIP, WEP104, WEP40
- RSN/WPA2 (IEEE 802.11i)

%prep
%setup -q
%patch0 -p1
sed -i -e 's#-O2#$(OPT)#g' Makefile

install %{SOURCE1} .config

%build
%{__make} \
	CC="%{__cc}" \
	OPT="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man{5,8}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install doc/docbook/*.5 $RPM_BUILD_ROOT%{_mandir}/man5
install doc/docbook/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README eap_testing.txt todo.txt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man[58]/*
