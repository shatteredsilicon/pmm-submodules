%global debug_package       %{nil}
%global provider            github
%global provider_tld        com
%global project             grafana
%global repo                grafana
# https://github.com/grafana/grafana
%global import_path         %{provider}.%{provider_tld}/%{project}/%{repo}
%global commit              v5.4.5
%global shortcommit         %(c=%{commit}; echo ${c:0:7})
%global node_sass_version   4.14.1

%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%endif

Name:           %{repo}
Version:        5.4.5
Release:        2%{?dist}
Summary:        Grafana is an open source, feature rich metrics dashboard and graph editor
License:        ASL 2.0
URL:            https://%{import_path}
Source0:        https://%{import_path}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Source1:        https://github.com/sass/node-sass/archive/v%{node_sass_version}/node-sass-v%{node_sass_version}.tar.gz
Source2:        grafana-node_modules-v5.4.5.tar.gz
Source3:        grafana-server.service
Source4:        ssm-favicon.ico
Source5:        node-sass-node_modules-v%{node_sass_version}.tar.gz
Patch0:         grafana-5.4.5-share-panel.patch
Patch1:         grafana-5.1.3-refresh-auth.patch
Patch2:         grafana-5.4.5-change-icon.patch
Patch3:         0001-NPM-audit-fix.patch

BuildRequires:  phantomjs
BuildRequires:  golang >= 1.7.3
BuildRequires:  python2-devel
BuildRequires:  nodejs fontconfig
BuildRequires:  gcc-c++ make
BuildRequires:  nodejs-devel

%if 0%{?fedora} || 0%{?rhel} == 7
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif

Requires:       fontconfig freetype urw-fonts

%description
Grafana is an open source, feature rich metrics dashboard and graph editor for
Graphite, InfluxDB & OpenTSDB.

%prep
%setup -q
%setup -q -T -D -a 1 -n %{repo}-%{version}
%setup -q -T -D -a 5 -n %{repo}-%{version}/node-sass-%{node_sass_version}
%setup -q -T -D -a 2 -n %{repo}-%{version}
%patch0 -p 1
%patch1 -p 1
%patch2 -p 0
%patch3 -p 1

rm -rf Godeps

%build
export GO111MODULE=off
chmod -R a+rw node_modules

pushd node-sass-%{node_sass_version}
    ln -s %{_includedir}/node/* src/libsass/include/
    node scripts/build -f --nodedir="%{_includedir}/node"
popd
sass_path=$(find $(pwd)/node-sass-%{node_sass_version}/vendor -name "*binding*.node" -type f | head -1)
rm -rf node_modules/node-sass
cp -r node-sass-%{node_sass_version} node_modules/node-sass
npm rebuild node-sass --sass-binary-path="${sass_path}"

mkdir -p _build/src
mv vendor/google.golang.org _build/src/
mv vendor/cloud.google.com _build/src/
mv vendor/github.com _build/src/
mv vendor/golang.org _build/src/
mv vendor/gopkg.in   _build/src/

mkdir -p ./_build/src/github.com/grafana
ln -s $(pwd) ./_build/src/github.com/grafana/grafana
export GOPATH=$(pwd)/_build:%{gopath}

export LDFLAGS="$LDFLAGS -X main.version=%{version} -X main.commit=%{shortcommit} -X main.buildstamp=$(date '+%s') "
%gobuild -o ./bin/grafana-server ./pkg/cmd/grafana-server
%gobuild -o ./bin/grafana-cli ./pkg/cmd/grafana-cli
/usr/bin/node --max-old-space-size=4500 ./node_modules/grunt-cli/bin/grunt --verbose --pkgVer=%{version} --phjsToRelease=/bin/phantomjs release

%install
install -d -p %{buildroot}%{_datadir}/%{repo}
cp -rpav tmp/conf %{buildroot}%{_datadir}/%{repo}
cp -rpav tmp/public %{buildroot}%{_datadir}/%{repo}
cp -rpav tmp/scripts %{buildroot}%{_datadir}/%{repo}
cp -rpav tmp/tools %{buildroot}%{_datadir}/%{repo}

if [ -d tmp/bin ]; then
 cp -rpav bin/* tmp/bin/
else
 mkdir -p tmp/bin
 cp -rpav bin/* tmp/bin/
fi

install -m 644 %{SOURCE4} %{buildroot}/usr/share/grafana/public/img/ssm-favicon.ico

install -d -p %{buildroot}%{_sbindir}
cp tmp/bin/%{repo}-server %{buildroot}%{_sbindir}/
install -d -p %{buildroot}%{_bindir}
cp tmp/bin/%{repo}-cli %{buildroot}%{_bindir}/

install -d -p %{buildroot}%{_sysconfdir}/%{repo}
cp tmp/conf/sample.ini %{buildroot}%{_sysconfdir}/%{repo}/grafana.ini
mv tmp/conf/ldap.toml %{buildroot}%{_sysconfdir}/%{repo}/

%if 0%{?fedora} || 0%{?rhel} == 7
mkdir -p %{buildroot}/usr/lib/systemd/system
install -p -m 0644 %{SOURCE3} %{buildroot}/usr/lib/systemd/system/
%else
mkdir -p %{buildroot}%{_initddir}/
install -p -m 0644 packaging/rpm/init.d/grafana-server %{buildroot}%{_initddir}/
%endif

install -d -p %{buildroot}%{_sharedstatedir}/%{repo}
install -d -p %{buildroot}/var/log/%{repo}

%check
export GO111MODULE=off
export GOPATH=$(pwd)/_build:%{gopath}
#go test ./pkg/api -vet=off
#go test ./pkg/bus -vet=off
#go test ./pkg/components/apikeygen -vet=off
#go test ./pkg/components/renderer
#go test ./pkg/events
#go test ./pkg/models
#go test ./pkg/plugins
#go test ./pkg/services/sqlstore
#go test ./pkg/services/sqlstore/migrations
#go test ./pkg/setting
#go test ./pkg/util

%files
%defattr(-, grafana, grafana, -)
%{_datadir}/%{repo}
%doc *.md
%doc docs
%attr(0755, root, root) %{_sbindir}/%{repo}-server
%attr(0755, root, root) %{_bindir}/%{repo}-cli
%{_sysconfdir}/%{repo}/grafana.ini
%{_sysconfdir}/%{repo}/ldap.toml
%if 0%{?fedora} || 0%{?rhel} == 7
%attr(-, root, root) /usr/lib/systemd/system/grafana-server.service
%else
%attr(-, root, root) %{_initddir}/grafana-server
%endif
#attr(-, root, root) %{_sysconfdir}/sysconfig/grafana-server
%dir %{_sharedstatedir}/%{repo}
%dir /var/log/%{repo}

%pre
getent group grafana >/dev/null || groupadd -r grafana
getent passwd grafana >/dev/null || \
    useradd -r -g grafana -d /etc/grafana -s /sbin/nologin \
    -c "Grafana Dashboard" grafana
exit 0

%post
%systemd_post grafana.service

%preun
%systemd_preun grafana.service

%postun
%systemd_postun grafana.service

%changelog
* Fri Feb 14 2020 Vadim Yalovets <vadim.yalovets@percona.com> - 5.4.5-2
- PMM-5339 Some charts are not fully visible

* Mon Sep 30 2019 Vadim Yalovets <vadim.yalovets@percona.com> - 5.4.5-1
- PMM-4596 CVE-2019-15043 Investigations and fixes

* Wed Nov 14 2018 Vadim Yalovets <vadim.yalovets@percona.com> - 5.1.3-7
- PMM-3257 Apply Patch from Grafana 5.3.3 to latest PMM version

* Mon Nov 5 2018 Nurlan Moldomurov <nurlan.moldomurov@percona.com> - 5.1.3-5
- PMM-2837 Fix image rendering

* Mon Oct 8 2018 Daria Lymanska <daria.lymanska@percona.com> - 5.1.3-4
- PMM-2880 add change-icon patch

* Mon Jun 18 2018 Mykola Marzhan <mykola.marzhan@percona.com> - 5.1.3-3
- PMM-2625 fix share-panel patch

* Mon Jun 18 2018 Mykola Marzhan <mykola.marzhan@percona.com> - 5.1.3-2
- PMM-2625 add share-panel patch

* Mon May 21 2018 Vadim Yalovets <vadim.yalovets@percona.com> - 5.1.3-1
- PMM-2561 update to 5.1.3

* Thu Mar 29 2018 Mykola Marzhan <mykola.marzhan@percona.com> - 5.0.4-1
- PMM-2319 update to 5.0.4

* Mon Jan  8 2018 Mykola Marzhan <mykola.marzhan@percona.com> - 4.6.3-1
- PMM-1895 update to 4.6.3

* Mon Nov  6 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.6.1-1
- PMM-1652 update to 4.6.1

* Tue Oct 31 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.6.0-1
- PMM-1652 update to 4.6.0

* Fri Oct  6 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.5.2-1
- PMM-1521 update to 4.5.2

* Tue Sep 19 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.4.3-2
- fix HOME variable in unit file

* Wed Aug  2 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.4.3-1
- PMM-1221 update to 4.4.3

* Wed Aug  2 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.4.2-1
- PMM-1221 update to 4.4.2

* Wed Jul 19 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.4.1-1
- PMM-1221 update to 4.4.1

* Thu Jul 13 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.3.2-2
- PMM-1208 install fontconfig freetype urw-fonts

* Thu Jun  1 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.3.2-1
- update to 4.3.2

* Wed Mar 29 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.2.0-2
- up to 4.2.0
- PMM-708 rollback tooltip position

* Tue Mar 14 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.1.2-1
- up to 4.1.2

* Thu Jan 26 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.1.1-1
- up to 4.1.1

* Thu Dec 29 2016 Mykola Marzhan <mykola.marzhan@percona.com> - 4.0.2-2
- use fixed grafana-server.service

* Thu Dec 15 2016 Mykola Marzhan <mykola.marzhan@percona.com> - 4.0.2-1
- up to 4.0.2

* Fri Jul 31 2015 Graeme Gillies <ggillies@redhat.com> - 2.0.2-3
- Unbundled phantomjs from grafana

* Tue Jul 28 2015 Lon Hohberger <lon@redhat.com> - 2.0.2-2
- Change ownership for grafana-server to root

* Tue Apr 14 2015 Graeme Gillies <ggillies@redhat.com> - 2.0.2-1
- First package for Fedora
