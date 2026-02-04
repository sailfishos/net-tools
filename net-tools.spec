#specfile originally created for Fedora, modified for Moblin Linux
%define npversion	1.2.9

Summary: Basic networking tools
Name: net-tools
Version: 2.10
Release: 2
License: GPLv2+
URL: http://sourceforge.net/projects/net-tools/
Source0: net-tools-%{version}.tar.xz
Source2: net-tools-config.h
Source3: net-tools-config.make
Source4: ether-wake.c
Source5: ether-wake.8
Source6: mii-diag.c
Source7: mii-diag.8
# adds <delay> option that allows netstat to cycle printing through statistics every delay seconds.
Patch1: net-tools-cycle.patch

# use all interfaces instead of default (#1003875)
Patch20: ether-wake-interfaces.patch

# use all interfaces instead of default (#1003875)
Patch27: net-tools-iface-name-too-long.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext

%description
The net-tools package contains basic networking tools, including
ifconfig, netstat, route, and others.

%package extra
Summary: Extra goodies from net-tools package

%description extra
net-tools extra goodies, including not-so commonly needed tools
(nisdomainname, ypdomainname, ether-wake, ipmaddr, mii-diag, mii-tool,
plipconfig and slattach), translations of the man pages and
localized support.

%package doc
Summary:   Documentation for %{name}
Requires:  %{name} = %{version}-%{release}

%description doc
Man pages for %{name}.

%prep
%setup -q

cp %SOURCE2 ./config.h
cp %SOURCE3 ./config.make
cp %SOURCE4 .
cp %SOURCE5 ./man/en_US
cp %SOURCE6 .
cp %SOURCE7 ./man/en_US

%autopatch -p1

%build
yes '' | ./configure.sh config.in
sed -i "s/HAVE_SELINUX=1/HAVE_SELINUX=0/g" ./config.make 
%make_build
gcc $RPM_OPT_FLAGS -Iinclude ether-wake.c -Llib -lnet-tools -o ether-wake
gcc $RPM_OPT_FLAGS -o mii-diag mii-diag.c

%install

make BASEDIR=$RPM_BUILD_ROOT mandir=%{_mandir} install

# ifconfig and route are installed into /bin by default
# add symlinks for backward compatibility
ln -s ../bin/ifconfig %{buildroot}/sbin
ln -s ../bin/route %{buildroot}/sbin

install -m 755 ether-wake %{buildroot}/sbin
install -m 755 mii-diag %{buildroot}/sbin


rm %{buildroot}/sbin/rarp
rm -rf %{buildroot}%{_mandir}/*/man*

%files
%license COPYING
/bin/*
/sbin/*
%exclude /bin/nisdomainname
%exclude /bin/ypdomainname
%exclude /sbin/ether-wake
%exclude /sbin/ipmaddr
%exclude /sbin/mii-diag
%exclude /sbin/mii-tool
%exclude /sbin/plipconfig
%exclude /sbin/slattach

%files extra
/bin/nisdomainname
/bin/ypdomainname
/sbin/ether-wake
/sbin/ipmaddr
/sbin/mii-diag
/sbin/mii-tool
/sbin/plipconfig
/sbin/slattach

%files doc
%{_mandir}/man*/*.*
