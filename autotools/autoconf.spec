Name:           autoconf
Version:        2.69
Release:        1%{?dist}
Summary:        A GNU tool for automatically configuring source code.

Group:          System Environment/Libraries
License:        GPLv3
URL:            http://gnu.org
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool

%description
GNU's Autoconf is a tool for configuring source code and Makefiles.
Using Autoconf, programmers can create portable and configurable
packages, since the person building the package is allowed to
specify various configuration options.

You should install Autoconf if you are developing software and
would like to create shell scripts that configure your source code
packages. If you are installing Autoconf, you will also need to
install the GNU m4 package.

Note that the Autoconf package is not required for the end-user who
may be configuring software with an Autoconf-generated script;
Autoconf is only required for the generation of the scripts, not
their use.

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
%{_bindir}/autoconf
%{_bindir}/autoheader
%{_bindir}/autom4te
%{_bindir}/autoreconf
%{_bindir}/autoscan
%{_bindir}/autoupdate
%{_bindir}/ifnames
%{_datadir}/autoconf
%doc
%{_infodir}/autoconf.info.gz
%{_mandir}/man1/autoconf.1.gz
%{_mandir}/man1/autoheader.1.gz
%{_mandir}/man1/autom4te.1.gz
%{_mandir}/man1/autoreconf.1.gz
%{_mandir}/man1/autoscan.1.gz
%{_mandir}/man1/autoupdate.1.gz
%{_mandir}/man1/config.guess.1.gz
%{_mandir}/man1/config.sub.1.gz
%{_mandir}/man1/ifnames.1.gz

%changelog
* Sat Oct 24 2015 James Hunt <james@niftylogiccom> 2.69-1
- Initial RPM package
