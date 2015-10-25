Name:           automake
Version:        1.15
Release:        1%{?dist}.bolo1
Summary:        A GNU tool for automatically creating Makefiles.

Group:          System Environment/Libraries
License:        GPLv3
URL:            http://gnu.org
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool

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
%{_bindir}/aclocal
%{_bindir}/aclocal-1.15
%{_bindir}/automake
%{_bindir}/automake-1.15
%{_datadir}/aclocal-1.15
%{_datadir}/aclocal
%{_datadir}/automake-1.15
%doc
%{_datadir}/doc/automake
%{_infodir}/automake-history.info.gz
%{_infodir}/automake.info*.gz
%{_mandir}/man1/aclocal*.1.gz
%{_mandir}/man1/automake*.1.gz


%changelog
* Sat Oct 24 2015 James Hunt <james@niftylogiccom> 1.15-1
- Initial RPM package
