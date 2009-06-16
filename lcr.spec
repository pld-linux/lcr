#
%define		_snap	20090615
Summary:	Linux-Call-Router - an ISDN PBX for Linux
Summary(pl.UTF-8):	Linux-Call-Router - centralka ISDN dla Linuksa
Name:		lcr
Version:	1.5
Release:	0.%{_snap}.1
License:	GPL v2+
Group:		Applications/System
Source0:	http://www.linux-call-router.de/download/lcr-1.5/%{name}_%{_snap}.tar.gz
# Source0-md5:	84eabeba617c578f89c33e1aadd59d03
Source1:	%{name}.sysconfig
Source2:	%{name}.init
Patch0:		%{name}-ncurses.patch
Patch1:		%{name}-dirs.patch
Patch2:		%{name}-no_compat.patch
URL:		http://www.linux-call-router.de/
BuildRequires:	asterisk-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	mISDNuser-devel >= 2.0
BuildRequires:	ncurses-devel
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Formerly known as "PBX4Linux", Linux-Call-Router is not only a router,
it is a real ISDN PBX which interconnects ISDN telephones and ISDN
lines. It is possible to connect telephones to a Linux box. It is a
pure software solution except for the ISDN cards and telephones. The
great benefit is the NT-mode that allows to connect telephones to an
ISDN card. Special cards are needed and a little bit of different
cabeling. It supports lots of features, that only expensive PBXs have.
It include a channel driver that can link LCR to Asterisk PBX.

%package -n asterisk-chan_lcr
Summary:	Linux-Call-Router channel for Asterisk
Group:		Applications/System

%description -n asterisk-chan_lcr
chan_lcr turns LCR into an ISDN channel driver for Asterisk PBX.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}

%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%dir %{_sysconfdir}/lcr
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lcr/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_datadir}/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}

%files -n asterisk-chan_lcr
%defattr(644,root,root,755)
%{_libdir}/asterisk/modules/*
