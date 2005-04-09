# TODO:
# - init script or supporin rc-scripts
# - pl descrition (and propable better en one)
# - separate cli, check BRs/Rs
#
Summary:	Linux WPA/WPA2/RSN/IEEE 802.1X supplicant
Summary(pl):	Suplikant WPA/WPA2/RSN/IEEE 802.1X dla Linuksa
Name:		wpa_supplicant
Version:	0.3.8
Release:	0.1
License:	GPL v2
Group:		Networking 
Source0:	http://hostap.epitest.fi/releases/%{name}-%{version}.tar.gz
# Source0-md5:	c9ced104f0322f834a84336c293b4b57
Source1:	%{name}.config
Patch0:		%{name}-makefile.patch
URL:		http://hostap.epitest.fi/wpa_supplicant/
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
- WPA with EAP (e.g., with RADIUS authentication server) ("WPA-Enterprise")
(currently, EAP-TLS and EAP-PEAP/MSCHAPv2 are supported with an integrated
IEEE 802.1X Supplicant;
other EAP types may be used with an external program, Xsupplicant)
- key management for CCMP, TKIP, WEP104, WEP40
- RSN/WPA2 (IEEE 802.11i)

#%description -l pl
# write me

%prep
%setup -q
%patch0 -p1

install %{SOURCE1} .config

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README developer.txt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(755,root,root) %{_sbindir}/*
