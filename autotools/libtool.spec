Name:           libtool
Version:        2.4.6
Release:        1%{?dist}
Summary:        A GNU tool for automatically creating Makefiles.

Group:          System Environment/Libraries
License:        GPLv3
URL:            http://gnu.org
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool

Obsoletes:      libtool-ltdl

%description
Automake is a tool for automatically generating `Makefile.in'
files compliant with the GNU Coding Standards.

You should install Automake if you are developing software and would
like to use its ability to automatically generate GNU standard
Makefiles. If you install Automake, you will also need to install
GNU's Autoconf package.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_infodir}/standards.info \
      $RPM_BUILD_ROOT%{_infodir}/dir


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/libtool
%{_bindir}/libtoolize
%{_includedir}/libltdl
%{_includedir}/ltdl.h
%{_libdir}/libltdl.*
%{_datadir}/aclocal/libtool.m4
%{_datadir}/aclocal/lt*.m4
%{_datadir}/libtool
%doc
%{_infodir}/libtool*.gz
%{_mandir}/man1/libtool*.gz

%changelog
* Sat Oct 24 2015 James Hunt <james@niftylogiccom> 2.4.6-1
- Initial RPM package
