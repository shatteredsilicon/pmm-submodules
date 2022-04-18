%define debug_package   %{nil}
%define _GOPATH         %{_builddir}/go

%global provider                github
%global provider_tld            com
%global project                 percona
%global repo                    percona-toolkit
%global import_path             %{provider}.%{provider_tld}/%{project}/%{repo}
%global percona_toolkit_version 3.3.1

Name:           %{repo}
Summary:        Percona Toolkit
Version:        %{percona_toolkit_version}
Release:        2%{?dist}
License:        GPL-2.0
Vendor:         Percona LLC
URL:            https://percona.com
Source0:        https://%{import_path}/archive/v%{percona_toolkit_version}/%{repo}-v%{percona_toolkit_version}.tar.gz
Source1:        percona-toolkit-vendor-v%{percona_toolkit_version}.tar.gz
BuildRequires:  golang

%description
Percona Toolkit

%prep
%setup -q -n %{name}-%{percona_toolkit_version}
%setup -q -T -D -a 1 -n %{repo}-%{version}

%build
mkdir -p %{_GOPATH}/bin
export GOPATH=%{_GOPATH}

go build ./src/go/pt-mongodb-summary
%{__cp} pt-mongodb-summary %{_GOPATH}/bin
%{__cp} bin/pt-mysql-summary %{_GOPATH}/bin
%{__cp} bin/pt-summary %{_GOPATH}/bin
%{__cp} bin/pt-visual-explain %{_GOPATH}/bin

strip %{_GOPATH}/bin/* || true

%install
install -m 0755 -d $RPM_BUILD_ROOT/usr/sbin
install -m 0755 -d $RPM_BUILD_ROOT/opt/ss/qan-agent/bin
install -m 0755 %{_GOPATH}/bin/pt-summary $RPM_BUILD_ROOT/opt/ss/qan-agent/bin/
install -m 0755 %{_GOPATH}/bin/pt-mysql-summary $RPM_BUILD_ROOT/opt/ss/qan-agent/bin/
install -m 0755 %{_GOPATH}/bin/pt-mongodb-summary $RPM_BUILD_ROOT/opt/ss/qan-agent/bin/
install -m 0755 %{_GOPATH}/bin/pt-visual-explain $RPM_BUILD_ROOT/usr/sbin/

%clean
rm -rf $RPM_BUILD_ROOT

%postun
# uninstall
if [ "$1" = "0" ]; then
    rm -rf /opt/ss/qan-agent/bin/pt-*
    echo "Uninstall complete."
fi

%files
%dir /opt/ss/qan-agent/bin
/opt/ss/qan-agent/bin/pt-*
/usr/sbin/pt-visual-explain
