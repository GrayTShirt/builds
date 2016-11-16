Name:           bolo
Version:        0.3.0
Release:        1%{?dist}.nifty1
Summary:        Monitoring System

Group:          Applications/System
License:        GPLv3+
URL:            https://github.com/bolo/bolo
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  pcre-devel
BuildRequires:  libzmq-devel
BuildRequires:  rrdtool-devel
BuildRequires:  libvigor-devel
BuildRequires:  postgresql-devel
BuildRequires:  libhiredis-devel
BuildRequires:  ncurses-devel
BuildRequires:  libcurl-devel

%description
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides the server implementation.

%prep
%setup -q


%build
%configure \
  --with-rrd-subscriber \
  --with-redis-subscriber \
  --with-pg-subscriber \
  --with-console-subscriber \
  --without-sqlite-subscriber
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_bindir}/bolo_nsca

# dist config
install -m 0644 -D examples/bolo.conf       $RPM_BUILD_ROOT%{_sysconfdir}/bolo.conf
install -m 0644 -D examples/schema/pg.sql   $RPM_BUILD_ROOT%{_datadir}/bolo/schema/pg.sql
# init scripts
%if 0%{?rhel} >= 7
	install -m 0755 -D /srv/redhat/systemd/bolo.service          $RPM_BUILD_ROOT%{_unitdir}/bolo.service
	install -m 0755 -D /srv/redhat/systemd/bolo-cache.service    $RPM_BUILD_ROOT%{_unitdir}/bolo-cache.service
	install -m 0755 -D /srv/redhat/systemd/bolo2meta.service     $RPM_BUILD_ROOT%{_unitdir}/bolo2meta.service
	install -m 0755 -D /srv/redhat/systemd/bolo2pg.service       $RPM_BUILD_ROOT%{_unitdir}/bolo2pg.service
	install -m 0755 -D /srv/redhat/systemd/bolo2redis.service    $RPM_BUILD_ROOT%{_unitdir}/bolo2redis.service
	install -m 0755 -D /srv/redhat/systemd/bolo2rrd.service      $RPM_BUILD_ROOT%{_unitdir}/bolo2rrd.service
	install -m 0755 -D /srv/redhat/systemd/dbolo.service         $RPM_BUILD_ROOT%{_unitdir}/dbolo.service
	install -m 0755 -D /srv/redhat/systemd/bolo2slack.service    $RPM_BUILD_ROOT%{_unitdir}/bolo2slack.service
	install -m 0755 -D /srv/redhat/systemd/bolo2influxdb.service $RPM_BUILD_ROOT%{_unitdir}/bolo2influxdb.service
	install -m 0755 -D /srv/redhat/systemd/opentsdb2bolo.service $RPM_BUILD_ROOT%{_unitdir}/opentsdb2bolo.service
%else
	install -m 0755 -D /srv/redhat/sysvinit/dbolo         $RPM_BUILD_ROOT%{_initrddir}/dbolo
	install -m 0755 -D /srv/redhat/sysvinit/bolo          $RPM_BUILD_ROOT%{_initrddir}/bolo
	install -m 0755 -D /srv/redhat/sysvinit/bolo2rrd      $RPM_BUILD_ROOT%{_initrddir}/bolo2rrd
	install -m 0755 -D /srv/redhat/sysvinit/bolo2redis    $RPM_BUILD_ROOT%{_initrddir}/bolo2redis
	install -m 0755 -D /srv/redhat/sysvinit/bolo2pg       $RPM_BUILD_ROOT%{_initrddir}/bolo2pg
	install -m 0755 -D /srv/redhat/sysvinit/bolo2meta     $RPM_BUILD_ROOT%{_initrddir}/bolo2meta
	install -m 0755 -D /srv/redhat/sysvinit/bolo2slack    $RPM_BUILD_ROOT%{_initrddir}/bolo2slack
	install -m 0755 -D /srv/redhat/sysvinit/bolo2influxdb $RPM_BUILD_ROOT%{_initrddir}/bolo2influxdb
	install -m 0755 -D /srv/redhat/sysvinit/opentsdb2bolo $RPM_BUILD_ROOT%{_initrddir}/opentsdb2bolo
%endif
ln -s %{_bindir}/bolo $RPM_BUILD_ROOT%{_sbindir}/bolo

# don't need the libtool archives
rm -f $RPM_BUILD_ROOT%{_libdir}/libbolo.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libtsdp.la


%clean
rm -rf $RPM_BUILD_ROOT


%post
%if 0%{?rhel} >= 7
	/bin/systemctl daemon-reload
	/bin/systemctl enable bolo
%else
	/sbin/chkconfig --add bolo
%endif


%preun
if [ $1 == 0 ]; then # erase!
	%if 0%{?rhel} >= 7
		/bin/systemctl stop bolo
		/bin/systemctl disable bolo
	%else
		/sbin/service stop bolo
		/sbin/chkconfig --del bolo
	%endif
fi


%postun
if [ $1 == 0 ]; then # upgrade!
	%if 0%{?rhel} >= 7
		/bin/systemctl restart bolo
	%else
		/sbin/service condrestart bolo
	%endif
fi


%files
%defattr(-,root,root,-)
%{_bindir}/bolo
%{_sbindir}/bolo
%if 0%{?rhel} >= 7
	%{_unitdir}/bolo.service
	%{_unitdir}/bolo-cache.service
%else
	%{_initrddir}/bolo
%endif
%doc %{_datadir}/bolo
%config %{_sysconfdir}/bolo.conf
%{_mandir}/man5/bolo.conf.5.gz
%{_mandir}/man1/bolo.1.gz
%{_mandir}/man1/bolo-aggr.1.gz
%{_mandir}/man1/bolo-cache.1.gz
%{_mandir}/man1/bolo-forget.1.gz
%{_mandir}/man1/bolo-name.1.gz
%{_mandir}/man1/bolo-query.1.gz
%{_mandir}/man1/bolo-send.1.gz
%{_mandir}/man1/bolo-spy.1.gz


#######################################################################

%package -n dbolo
Summary:        Monitoring System Agent
Group:          Applications/System

%description -n dbolo
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides the dbolo monitoring agent for bolo.


%post -n dbolo
%if 0%{?rhel} >= 7
	/bin/systemctl daemon-reload
	/bin/systemctl enable dbolo
%else
	/sbin/chkconfig --add dbolo
%endif


%preun -n dbolo
if [ $1 == 0 ]; then # erase!
	%if 0%{?rhel} >= 7
		/bin/systemctl stop dbolo
		/bin/systemctl disable dbolo
	%else
		/sbin/service stop dbolo
		/sbin/chkconfig --del dbolo
	%endif
fi


%postun -n dbolo
if [ $1 == 0 ]; then # upgrade!
	%if 0%{?rhel} >= 7
		/bin/systemctl restart dbolo
	%else
		/sbin/service condrestart dbolo
	%endif
fi


%files -n dbolo
%defattr(-,root,root,-)
%{_sbindir}/dbolo
%if 0%{?rhel} >= 7
	%{_unitdir}/dbolo.service
%else
	%{_initrddir}/dbolo
%endif
%{_mandir}/man1/dbolo.1.gz
%{_mandir}/man5/dbolo.conf.5.gz


#######################################################################
%package redis-subscriber

Summary:        Monitoring System Redis Subscriber
Group:          Applications/System

%description redis-subscriber
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides the redis subscriber component for bolo.


%post redis-subscriber
%if 0%{?rhel} >= 7
	/bin/systemctl daemon-reload
	/bin/systemctl enable bolo2redis
%else
	/sbin/chkconfig --add bolo2redis
%endif


%preun redis-subscriber
if [ $1 == 0 ]; then # erase!
	%if 0%{?rhel} >= 7
		/bin/systemctl stop bolo2redis
		/bin/systemctl disable bolo2redis
	%else
		/sbin/service stop bolo2redis
		/sbin/chkconfig --del bolo2redis
	%endif
fi


%postun redis-subscriber
if [ $1 == 0 ]; then # upgrade!
	%if 0%{?rhel} >= 7
		/bin/systemctl restart bolo2redis
	%else
		/sbin/service condrestart bolo2redis
	%endif
fi


%files redis-subscriber
%defattr(-,root,root,-)
%{_sbindir}/bolo2redis
%if 0%{?rhel} >= 7
	%{_unitdir}/bolo2redis.service
%else
	%{_initrddir}/bolo2redis
%endif
%{_mandir}/man8/bolo2redis.8.gz


#######################################################################
%package rrd-subscriber
Summary:        Monitoring System RRD Subscriber
Group:          Applications/System

%description rrd-subscriber
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides the RRD subscriber component for bolo.


%post rrd-subscriber
%if 0%{?rhel} >= 7
	/bin/systemctl daemon-reload
	/bin/systemctl enable bolo2rrd
%else
	/sbin/chkconfig --add bolo2rrd
%endif


%preun rrd-subscriber
if [ $1 == 0 ]; then # erase!
	%if 0%{?rhel} >= 7
		/bin/systemctl stop bolo2rrd
		/bin/systemctl disable bolo2rrd
	%else
		/sbin/service stop bolo2rrd
		/sbin/chkconfig --del bolo2rrd
	%endif
fi


%postun rrd-subscriber
if [ $1 == 0 ]; then # upgrade!
	%if 0%{?rhel} >= 7
		/bin/systemctl restart bolo2rrd
	%else
		/sbin/service condrestart bolo2rrd
	%endif
fi


%files rrd-subscriber
%defattr(-,root,root,-)
%{_sbindir}/bolo2rrd
%if 0%{?rhel} >= 7
	%{_unitdir}/bolo2rrd.service
%else
	%{_initrddir}/bolo2rrd
%endif
%{_mandir}/man8/bolo2rrd.8.gz


#######################################################################
%package pg-subscriber
Summary:        Monitoring System Postgres Subscriber
Group:          Applications/System

%description pg-subscriber
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides the postgres subscriber component for bolo.


%post pg-subscriber
%if 0%{?rhel} >= 7
	/bin/systemctl daemon-reload
	/bin/systemctl enable bolo2pg
%else
	/sbin/chkconfig --add bolo2pg
%endif


%preun pg-subscriber
if [ $1 == 0 ]; then # erase!
	%if 0%{?rhel} >= 7
		/bin/systemctl stop bolo2pg
		/bin/systemctl disable bolo2pg
	%else
		/sbin/service stop bolo2pg
		/sbin/chkconfig --del bolo2pg
	%endif
fi


%postun pg-subscriber
if [ $1 == 0 ]; then # upgrade!
	%if 0%{?rhel} >= 7
		/bin/systemctl restart bolo2pg
	%else
		/sbin/service condrestart bolo2pg
	%endif
fi


%files pg-subscriber
%defattr(-,root,root,-)
%{_sbindir}/bolo2pg
%if 0%{?rhel} >= 7
	%{_unitdir}/bolo2pg.service
%else
	%{_initrddir}/bolo2pg
%endif
%{_mandir}/man8/bolo2pg.8.gz


#######################################################################
%package console-subscriber
Summary:        Monitoring System Console Subscriber
Group:          Applications/System

%description console-subscriber
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides the console subscriber component for bolo.


%files console-subscriber
%defattr(-,root,root,-)
%{_sbindir}/bolo2console
%{_mandir}/man8/bolo2console.8.gz


#######################################################################
%package log-subscriber
Summary:        Monitoring System Log Subscriber
Group:          Applications/System

%description log-subscriber
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides the log subscriber component for bolo.


%files log-subscriber
%defattr(-,root,root,-)
%{_sbindir}/bolo2log
%{_mandir}/man8/bolo2log.8.gz


#######################################################################
%package meta-subscriber
Summary:        Monitoring System Meta Subscriber
Group:          Applications/System

%description meta-subscriber
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides the meta subscriber component for bolo.


%post meta-subscriber
%if 0%{?rhel} >= 7
	/bin/systemctl daemon-reload
	/bin/systemctl enable bolo2meta
%else
	/sbin/chkconfig --add bolo2meta
%endif


%preun meta-subscriber
if [ $1 == 0 ]; then # erase!
	%if 0%{?rhel} >= 7
		/bin/systemctl stop bolo2meta
		/bin/systemctl disable bolo2meta
	%else
		/sbin/service stop bolo2meta
		/sbin/chkconfig --del bolo2meta
	%endif
fi


%postun meta-subscriber
if [ $1 == 0 ]; then # upgrade!
	%if 0%{?rhel} >= 7
		/bin/systemctl restart bolo2meta
	%else
		/sbin/service condrestart bolo2meta
	%endif
fi


%files meta-subscriber
%defattr(-,root,root,-)
%{_sbindir}/bolo2meta
%if 0%{?rhel} >= 7
	%{_unitdir}/bolo2meta.service
%else
	%{_initrddir}/bolo2meta
%endif
%{_mandir}/man8/bolo2meta.8.gz


#######################################################################
%package slack-subscriber
Summary:        Monitoring System Slack Subscriber
Group:          Applications/System

%description slack-subscriber
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides the slack subscriber component for bolo.


%post slack-subscriber
%if 0%{?rhel} >= 7
	/bin/systemctl daemon-reload
	/bin/systemctl enable bolo2slack
%else
	/sbin/chkconfig --add bolo2slack
%endif


%preun slack-subscriber
if [ $1 == 0 ]; then # erase!
	%if 0%{?rhel} >= 7
		/bin/systemctl stop bolo2slack
		/bin/systemctl disable bolo2slack
	%else
		/sbin/service stop bolo2slack
		/sbin/chkconfig --del bolo2slack
	%endif
fi


%postun slack-subscriber
if [ $1 == 0 ]; then # upgrade!
	%if 0%{?rhel} >= 7
		/bin/systemctl restart bolo2slack
	%else
		/sbin/service condrestart bolo2slack
	%endif
fi


%files slack-subscriber
%defattr(-,root,root,-)
%{_sbindir}/bolo2slack
%if 0%{?rhel} >= 7
	%{_unitdir}/bolo2slack.service
%else
    %{_initrddir}/bolo2slack
%endif
%{_mandir}/man8/bolo2slack.8.gz


#######################################################################
%package influxdb-subscriber
Summary:        Monitoring System InfluxDB Subscriber
Group:          Applications/System

%description influxdb-subscriber
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides the influxdb subscriber component for bolo.


%post influxdb-subscriber
%if 0%{?rhel} >= 7
	/bin/systemctl daemon-reload
	/bin/systemctl enable bolo2influxdb
%else
	/sbin/chkconfig --add bolo2influxdb
%endif


%preun influxdb-subscriber
if [ $1 == 0 ]; then # erase!
	%if 0%{?rhel} >= 7
		/bin/systemctl stop bolo2influxdb
		/bin/systemctl disable bolo2influxdb
	%else
		/sbin/service stop bolo2influxdb
		/sbin/chkconfig --del bolo2influxdb
	%endif
fi


%postun influxdb-subscriber
if [ $1 == 0 ]; then # upgrade!
	%if 0%{?rhel} >= 7
		/bin/systemctl restart bolo2influxdb
	%else
		/sbin/service condrestart bolo2influxdb
	%endif
fi


%files influxdb-subscriber
%defattr(-,root,root,-)
%{_sbindir}/bolo2influxdb
%if 0%{?rhel} >= 7
	%{_unitdir}/bolo2influxdb.service
%else
    %{_initrddir}/bolo2influxdb
%endif
%{_mandir}/man8/bolo2influxdb.8.gz


#######################################################################
%package opentsdb-consumer
Summary:        Monitoring System OpenTSDP Consumer
Group:          Applications/System

%description opentsdb-consumer
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides the opentsdp consumer component for bolo.


%post opentsdb-consumer
%if 0%{?rhel} >= 7
	/bin/systemctl daemon-reload
	/bin/systemctl enable opentsdb2bolo
%else
	/sbin/chkconfig --add opentsdb2bolo
%endif


%preun opentsdb-consumer
if [ $1 == 0 ]; then # erase!
	%if 0%{?rhel} >= 7
		/bin/systemctl stop opentsdb2bolo
		/bin/systemctl disable opentsdb2bolo
	%else
		/sbin/service stop opentsdb2bolo
		/sbin/chkconfig --del opentsdb2bolo
	%endif
fi


%postun opentsdb-consumer
if [ $1 == 0 ]; then # upgrade!
	%if 0%{?rhel} >= 7
		/bin/systemctl restart opentsdb2bolo
	%else
		/sbin/service condrestart opentsdb2bolo
	%endif
fi


%files opentsdb-consumer
%defattr(-,root,root,-)
%{_sbindir}/opentsdb2bolo
%if 0%{?rhel} >= 7
	%{_unitdir}/opentsdb2bolo.service
%else
    %{_initrddir}/opentsdb2bolo
%endif
%{_mandir}/man8/opentsdb2bolo.8.gz


#######################################################################
%package -n libbolo1
Summary:        Monitoring System Libraries
Group:          System Environment/Libraries

%description -n libbolo1
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides libraries that are linked to in user
subscribers.


%files -n libbolo1
%defattr(-,root,root,-)
%{_libdir}/libbolo.so.*
%{_libdir}/libtsdp.so.*


#######################################################################
%package -n libtsdp1
Summary:        Monitoring System Libraries
Group:          System Environment/Libraries

%description -n libtsdp1
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides libraries that are linked to in user
subscribers.


%files -n libtsdp1
%defattr(-,root,root,-)
%{_libdir}/libbolo.so.*
%{_libdir}/libtsdp.so.*


#######################################################################
%package devel
Summary:        Monitoring System Developer Libraries
Group:          Development/Libraries
Requires:       libbolo1
Requires:       libtsdp1

%description devel
bolo is a lightweight and scalable monitoring system that can
track samples, counters, states and configuration data.

This package provides developer libraries and headers used to
write user subscribers.


%files devel
%defattr(-,root,root,-)
%{_includedir}/bolo.h
%{_includedir}/tsdp.h
%{_libdir}/libbolo.a
%{_libdir}/libbolo.so
%{_libdir}/libtsdp.a
%{_libdir}/libtsdp.so


#######################################################################
%changelog
* Thu Aug 11 2016 James Hunt <pkg@niftylogic.com> 0.2.18-1.nifty1
- Initial rpmification via bolo/builds
