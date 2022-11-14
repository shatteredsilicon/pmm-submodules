%define debug_package   %{nil}
%define _GOPATH         %{_builddir}/go

%global provider                github
%global provider_tld            com
%global project                 percona
%global repo                    percona-toolkit
%global import_path             %{provider}.%{provider_tld}/%{project}/%{repo}
%global percona_toolkit_version 3.4.0

Name:           %{repo}-ssm-minimal
Summary:        Percona Toolkit (SSM Minimal)
Version:        %{percona_toolkit_version}
Release:        1%{?dist}
License:        GPL-2.0
Vendor:         Percona LLC
URL:            https://percona.com
Source0:        https://%{import_path}/archive/%{percona_toolkit_version}/%{repo}-%{percona_toolkit_version}.tar.gz
BuildRequires:  golang

%description
Percona Toolkit (SSM Minimal)

%prep
%setup -q -n %{repo}-%{percona_toolkit_version}

%build
mkdir -p %{_GOPATH}/bin
export GOPATH=%{_GOPATH}

go build -ldflags="-s -w" ./src/go/pt-mongodb-summary
%{__cp} pt-mongodb-summary %{_GOPATH}/bin
%{__cp} bin/pt-mysql-summary %{_GOPATH}/bin
%{__cp} bin/pt-summary %{_GOPATH}/bin
%{__cp} bin/pt-visual-explain %{_GOPATH}/bin

strip %{_GOPATH}/bin/* || true

%install
install -m 0755 -d $RPM_BUILD_ROOT/usr/bin
install -m 0755 %{_GOPATH}/bin/pt-summary $RPM_BUILD_ROOT/usr/bin/
install -m 0755 %{_GOPATH}/bin/pt-mysql-summary $RPM_BUILD_ROOT/usr/bin/
install -m 0755 %{_GOPATH}/bin/pt-mongodb-summary $RPM_BUILD_ROOT/usr/bin/
install -m 0755 %{_GOPATH}/bin/pt-visual-explain $RPM_BUILD_ROOT/usr/bin/

%clean
rm -rf $RPM_BUILD_ROOT

%postun
# uninstall
if [ "$1" = "0" ]; then
    rm -f /usr/bin/pt-summary
    rm -f /usr/bin/pt-mysql-summary
    rm -f /usr/bin/pt-mongodb-summary
    rm -f /usr/bin/pt-visual-explain
    echo "Uninstall complete."
fi

%files
/usr/bin/pt-summary
/usr/bin/pt-mysql-summary
/usr/bin/pt-mongodb-summary
/usr/bin/pt-visual-explain
