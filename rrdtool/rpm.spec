%define rrdcached_user rrdcached

Name:           rrdtool
Version:        1.6.0
Release:        1%{?dist}.nifty1
Summary:        Round Robin Database Tool to store and display time-series data

Group:          Applications/Databases
License:        GPLv2+ with exceptions
URL:            http://oss.oetiker.ch/rrdtool/
Source0:        http://oss.oetiker.ch/rrdtool/pub/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?el6} || 0%{?el7}
Requires:       dejavu-lgc-sans-mono-fonts
%else
Requires:       dejavu-lgc-fonts
%endif

BuildRequires:  gcc-c++, openssl-devel, freetype-devel
BuildRequires:  libpng-devel, zlib-devel, intltool >= 0.35.0
BuildRequires:  cairo-devel >= 1.2, pango-devel >= 1.14
BuildRequires:  libtool, groff
BuildRequires:  gettext, libxml2-devel
BuildRequires:  pcre-devel

%description
RRD is the Acronym for Round Robin Database. RRD is a system to store and
display time-series data (i.e. network bandwidth, machine-room temperature,
server load average). It stores the data in a very compact way that will not
expand over time, and it presents useful graphs by processing the data to
enforce a certain data density. It can be used either via simple wrapper
scripts (from shell or Perl) or via frontends that poll network devices and
put a friendly user interface on it.

%package devel
Summary:        RRDtool libraries and header files
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
RRD is the Acronym for Round Robin Database. RRD is a system to store and
display time-series data (i.e. network bandwidth, machine-room temperature,
server load average). This package allow you to use directly this library.

%package perl
Summary:        Perl RRDtool bindings
Group:          Development/Languages

Requires:       %{name} = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

Obsoletes:      perl-%{name} < %{version}-%{release}

Provides:       perl-%{name} = %{version}-%{release}

%description perl
The Perl RRDtool bindings

%package cached
Summary:        Data caching daemon for RRDtool
Group:          Applications/Databases
Requires:       %{name} = %{version}-%{release}

%description cached
rrdcached is a daemon that receives updates to existing RRD files,
accumulates them and, if enough have been received or a defined time has
passed, writes the updates to the RRD file.  The daemon was written with
big setups in mind which usually runs into I/O related problems.  This
daemon was written to alleviate these problems.

%prep
%setup -q -n %{name}-%{version}

# Fix to find correct python dir on lib64
%{__perl} -pi -e 's|get_python_lib\(0,0,prefix|get_python_lib\(1,0,prefix|g' \
    configure

# Most edits shouldn't be necessary when using --libdir, but
# w/o, some introduce hardcoded rpaths where they shouldn't
%{__perl} -pi.orig -e 's|/lib\b|/%{_lib}|g' configure Makefile.in*

# Perl 5.10 seems to not like long version strings, hack around it
%{__perl} -pi.orig -e 's|1.299907080300|1.29990708|' \
    bindings/perl-shared/RRDs.pm bindings/perl-piped/RRDp.pm


%build
%configure \
    CFLAGS="-g -O0" \
    --with-perl-options='INSTALLDIRS="vendor"' \
    --disable-tcl \
    --disable-python \
    --disable-ruby \
    --disable-lua \
    --enable-perl-site-install \
    --disable-static \
    --with-pic

# Fix another rpath issue
%{__perl} -pi.orig -e 's|-Wl,--rpath -Wl,\$rp||g' \
    bindings/perl-shared/Makefile.PL

make -j4 %{?_smp_mflags}

# Fix @perl@ and @PERL@
find examples/ -type f \
    -exec %{__perl} -pi -e 's|^#! \@perl\@|#!%{__perl}|gi' {} \;
find examples/ -name "*.pl" \
    -exec %{__perl} -pi -e 's|\015||gi' {} \;

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR="$RPM_BUILD_ROOT" install

# We only want .txt and .html files for the main documentation
%{__mkdir_p} doc2/html doc2/txt
%{__cp} -a doc/*.txt doc2/txt/
%{__cp} -a doc/*.html doc2/html/

# Put perl docs in perl package
%{__mkdir_p} doc3/html
%{__mv} doc2/html/RRD*.html doc3/html/

# Clean up the examples
%{__rm} -f examples/Makefile* examples/*.in

# This is so rpm doesn't pick up perl module dependencies automatically
find examples/ -type f -exec chmod 0644 {} \;

# Clean up the buildroot
%{__rm} -rf $RPM_BUILD_ROOT%{_docdir}/%{name}-* \
	$RPM_BUILD_ROOT%{perl_vendorarch}/ntmake.pl \
	$RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod \
        $RPM_BUILD_ROOT%{_datadir}/%{name}/examples \
        $RPM_BUILD_ROOT%{perl_vendorarch}/auto/*/{.packlist,*.bs}

# Set up rrdcached
%__install -d -m 0755 $RPM_BUILD_ROOT/%{_sysconfdir}/default
%__install -d -m 0755 $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d
%__install -m 0644 etc/rrdcached-default-redhat $RPM_BUILD_ROOT/%{_sysconfdir}/default/rrdcached
%__install -m 0755 etc/rrdcached-init-redhat $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/rrdcached
%__install -d -m 0755 $RPM_BUILD_ROOT/%{_localstatedir}/run/rrdcached

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre cached
/usr/sbin/groupadd %rrdcached_user &>/dev/null ||:
/usr/sbin/useradd -s /sbin/nologin -g %rrdcached_user -c %rrdcached_user -d %{_localstatedir}/run/rrdcached  %rrdcached_user &>/dev/null || :

%post -p /sbin/ldconfig

%post cached
/sbin/chkconfig --add rrdcached
/sbin/service rrdcached start

%preun cached
/sbin/service rrdcached stop

%postun -p /sbin/ldconfig

%postun cached
/sbin/chkconfig --del rrdcached
test "$1" != 0 || /usr/sbin/userdel %rrdcached_user &>/dev/null || :
#test "$1" != 0 || /usr/sbin/groupdel %rrdcached_user &>/dev/null || :

%files
%defattr(-,root,root,-)
%{_bindir}/*
%exclude %{_bindir}/rrdcached
%{_libdir}/*.so.*
%{_datadir}/%{name}
%{_mandir}/man1/*
%exclude %{_mandir}/man1/rrdcached*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%exclude %{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/librrd.pc

%files perl
%defattr(-,root,root,-)
%doc doc3/html
%{_mandir}/man3/*
%{perl_vendorarch}/*.pm
%attr(0755,root,root) %{perl_vendorarch}/auto/RRDs/
%{perl_vendorlib}/*.pm

%files cached
%{_bindir}/rrdcached
%config %{_sysconfdir}/default/*
%config %{_sysconfdir}/rc.d/init.d/*
%{_mandir}/man1/rrdcached*
%attr(0775 %rrdcached_user %rrdcached_user) %dir %{_localstatedir}/run/rrdcached
%if 0%{?el7}
/usr/lib/systemd/system/rrdcached.service
/usr/lib/systemd/system/rrdcached.socket
%endif

%changelog
* Thu Aug 11 2016 James Hunt <pkg@niftylogic.com> 1.6.0-1.nifty1
- Initial rpmification via bolo/builds
