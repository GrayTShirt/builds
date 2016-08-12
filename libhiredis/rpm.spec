Name:           libhiredis
Version:        0.13.3
Release:        1%{?dist}.nifty1
Summary:        A minimalistic C client library for the Redis database

Group:          System Environment/Libraries
License:        GPLv3+
URL:            https://github.com/redis/hiredis/archive/v0.13.3.tar.gz
Source0:        hiredis-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc

%description
libhiredis provides minimal support for the Redis protocol, but wraps in a
high level, printf-like API.  It supports sending commands and receiving
replies (both syncrhonously and asynchronously), but also features a reply
parser that is decoupled from the I/O layer, to aide reusability.  Only the
binary-sfae Redis protocol is supported, which requires Redis 1.2.0 or
greater.

%package devel
Summary:        A minimalistic C client library for the Redis database
Group:          Development/Libraries

%description devel
libhiredis provides minimal support for the Redis protocol, but wraps in a
high level, printf-like API.  It supports sending commands and receiving
replies (both syncrhonously and asynchronously), but also features a reply
parser that is decoupled from the I/O layer, to aide reusability.  Only the
binary-sfae Redis protocol is supported, which requires Redis 1.2.0 or
greater.

This package contains the header files for developing code against
libhiredis.


%prep
%setup -q -n hiredis-%{version}


%build
make PREFIX=/usr %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make PREFIX=/usr install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
/usr/lib/libhiredis.so
/usr/lib/libhiredis.so.0.13

%files devel
%defattr(-,root,root,-)
%{_includedir}/hiredis/*.h
%{_includedir}/hiredis/adapters/*.h
/usr/lib/libhiredis.a
/usr/lib/libhiredis.so
/usr/lib/pkgconfig/hiredis.pc


%changelog
* Thu Aug 11 2016 James Hunt <pkg@niftylogic.com> 0.13.3-1.nifty1
- Initial rpmification via bolo/builds
