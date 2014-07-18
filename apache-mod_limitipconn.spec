%define		mod_name	limitipconn
%define 	apxs		%{_sbindir}/apxs
Summary:	Apache module: Limit simultaneous connections by an IP address
Name:		apache-mod_%{mod_name}
Version:	0.24
Release:	1
License:	Apache
Group:		Networking/Daemons
Source0:	http://dominia.org/djao/limit/mod_limitipconn-%{version}.tar.bz2
# Source0-md5:	5cf6ddc6743931afef26c03de851279b
Source1:	apache.conf
URL:		http://dominia.org/djao/limitipconn2.html
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.0
BuildRequires:	rpmbuild(macros) >= 1.228
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
The mod_limitipconn module lets you enforce limits on the number of
simultaneous downloads allowed from a single IP address. You can also
control which MIME types are affected by the limits.

This module will not function unless mod_status is loaded and the
"ExtendedStatus On" directive is set.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{apxs} -c mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}
install -p .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
