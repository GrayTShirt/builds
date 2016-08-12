Name:           libzmq
Version:        4.1.5
Release:        1%{?dist}.nifty1
Summary:        Distributed Messaging

Group:          System Environment/Libraries
License:        LGPLv3+
URL:            http://github.com/jedisct1/libzmq
Source0:        zeromq-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  libsodium-devel
BuildRequires:  asciidoc
BuildRequires:  xmlto

Requires: libsodium

%description
ZeroMQ (also known as ØMQ, 0MQ, or zmq) looks like an embeddable networking
library but acts like a concurrency framework. It gives you sockets that carry
atomic messages across various transports like in-process, inter-process, TCP,
and multicast. You can connect sockets N-to-N with patterns like fan-out,
pub-sub, task distribution, and request-reply. It's fast enough to be the
fabric for clustered products. Its asynchronous I/O model gives you scalable
multicore applications, built as asynchronous message-processing tasks. It has
a score of language APIs and runs on most operating systems. ZeroMQ is from
iMatix and is LGPLv3 open source.

%package devel
Summary:        Distributed Messaging - Development Files
Group:          Development/Libraries

%description devel
ZeroMQ (also known as ØMQ, 0MQ, or zmq) looks like an embeddable networking
library but acts like a concurrency framework. It gives you sockets that carry
atomic messages across various transports like in-process, inter-process, TCP,
and multicast. You can connect sockets N-to-N with patterns like fan-out,
pub-sub, task distribution, and request-reply. It's fast enough to be the
fabric for clustered products. Its asynchronous I/O model gives you scalable
multicore applications, built as asynchronous message-processing tasks. It has
a score of language APIs and runs on most operating systems. ZeroMQ is from
iMatix and is LGPLv3 open source.

This package contains the header files for developing code against libzmq.

%prep
%setup -q -n zeromq-%{version}


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_libdir}/libzmq.so*
%{_bindir}/curve_keygen
%doc
%{_mandir}/man3/zmq*
%{_mandir}/man7/zmq*


%files devel
%defattr(-,root,root,-)
%{_includedir}/zmq*
%{_libdir}/libzmq.a
%{_libdir}/libzmq.la
%{_libdir}/pkgconfig/libzmq.pc


%changelog
* Thu Aug 11 2016 James Hunt <pkg@niftylogic.com> 1.4.5-1.nifty1
- Initial rpmification via bolo/builds
