Name:           bolo-collectors
Version:        0.4.13
Release:        1%{?dist}.nifty1
Summary:        Monitoring System Collectors

Group:          Applications/System
License:        GPLv3+
URL:            https://github.com/bolo/bolo-collectors
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  ctap
BuildRequires:  pcre-devel
BuildRequires:  libzmq-devel
BuildRequires:  libvigor-devel
BuildRequires:  mysql-devel

%if 0%{?el6} || 0%{?el7}
BuildRequires:  libcurl-devel
%else
BuildRequires:  curl-devel
%endif

%description
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides a set of baseline collectors for system metrics.

%package clockwork
Summary:        Monitoring System Collectors for clockwork
Group:          Applications/System

%description clockwork
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides a collector for monitoring the health of
the cogd agent for health and functionality.

%package fw
Summary:        Monitoring System Collectors for iptables firewalls
Group:          Applications/System

%description fw
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides a collector for monitoring the traffic
transiting an iptables / ip6tables firewall.


%package httpd
Summary:        Monitoring System Collectors for HTTP web servers
Group:          Applications/System

%description httpd
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides a collector that monitors the health of HTTP
web servers like Apache and nginx, via their scoreboard endpoints.


%package mysql
Summary:        Monitoring System Collectors for MySQL databases
Group:          Applications/System

%description mysql
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides a collector for monitoring the health of a
MySQL database server and its databases.


%package nagios
Summary:        Monitoring System Collectors for wrapping Nagios check plugins
Group:          Applications/System

%description nagios
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides a collector that wraps pre-existing Nagios
check plugins.


%package postgres
Summary:        Monitoring System Collectors for PostgreSQL databases
Group:          Applications/System

%description postgres
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides a collector for monitoring the health of a
PostgreSQL cluster and its databases.


%package rrdcache
Summary:        Monitoring System Collectors for rrdcached
Group:          Applications/System

%description rrdcache
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides a collector for monitoring the health of the
rrdcached RRDtool caching daemon.


%package perl
Summary:        Perl Libraries for Monitoring System Collectors
Group:          System Environment/Libraries

%description perl
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides a Perl framework for writing collectors.


%package snmp
Summary:        Monitoring System Collectors for SNMP endpoints
Group:          Applications/System
Requires:       bolo-collectors-perl

%description snmp
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides collectors for monitoring SNMP endpoints
like networking gear.

%prep
%setup -q


%build
%configure --with-all-collectors --prefix=/usr PERLDIR=/usr/share/perl5
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_bindir}/rrdq


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_libdir}/bolo/collectors/files
%{_libdir}/bolo/collectors/hostinfo
%{_libdir}/bolo/collectors/linux
%{_libdir}/bolo/collectors/netstat
%{_libdir}/bolo/collectors/process
%{_libdir}/bolo/collectors/tcp

%files clockwork
%{_libdir}/bolo/collectors/cogd

%files fw
%{_libdir}/bolo/collectors/fw

%files httpd
%{_libdir}/bolo/collectors/httpd

%files mysql
%{_libdir}/bolo/collectors/mysql

%files nagios
%{_libdir}/bolo/collectors/nagwrap

%files postgres
%{_libdir}/bolo/collectors/postgres
%{_datadir}/bolo-collectors/pg.sql

%files rrdcache
%{_libdir}/bolo/collectors/rrdcache

%files perl
%{_datadir}/perl5/Bolo/Collector.pm

%files snmp
%{_libdir}/bolo/collectors/snmp_cisco
%{_libdir}/bolo/collectors/snmp_cisco_detect
%{_libdir}/bolo/collectors/snmp_cisco_ifaces
%{_libdir}/bolo/collectors/snmp_cisco_sys
%{_libdir}/bolo/collectors/snmp_ifaces
%{_libdir}/bolo/collectors/snmp_system

%changelog
* Thu Aug 11 2016 James Hunt <pkg@niftylogic.com> 0.4.13-1.nifty1
- Initial rpmification via bolo/builds
