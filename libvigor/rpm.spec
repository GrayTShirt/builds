Name:           libvigor
Version:        1.2.10
Release:        1%{?dist}.nifty1
Summary:        Missing Bits of C

Group:          System Environment/Libraries
License:        GPLv3+
URL:            https://github.com/jhunt/libvigor
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  ctap
BuildRequires:  libzmq-devel
BuildRequires:  libsodium-devel

%description
libvigor is a set of primitives for getting past the inherent shortcomings
of a beautifully simple language like C.  It provides robust list and hash
representations, and several other abstractions like daemonization, command
execution management, a 0MQ packet layer, time and timing functions and more.

%package devel
Summary:        Missing Bits of C - Development Files
Group:          Development/Libraries

%description devel
libvigor is a set of primitives for getting past the inherent shortcomings
of a beautifully simple language like C.  It provides robust list and hash
representations, and several other abstractions like daemonization, command
execution management, a 0MQ packet layer, time and timing functions and more.

This package contains the header files for developing code against libvigor.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/usr/bin/fuzz-config


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_libdir}/libvigor.so.1
%{_libdir}/libvigor.so.1.1.0

%files devel
%defattr(-,root,root,-)
%{_includedir}/vigor.h
%{_libdir}/libvigor.a
%{_libdir}/libvigor.la
%{_libdir}/libvigor.so
%{_libdir}/pkgconfig/libvigor.pc


%changelog
* Thu Aug 11 2016 James Hunt <pkg@niftylogic.com> 1.2.10-1.nifty1
- Initial rpmification via bolo/builds
