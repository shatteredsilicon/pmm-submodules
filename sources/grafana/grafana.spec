%define debug_package %{nil}

%if 0%{?rhel}
%define enable_fips_mode 1
%else
%define enable_fips_mode 0
%endif

%global grafana_arches %{lua: go_arches = {}
  for arch in rpm.expand("%{go_arches}"):gmatch("%S+") do
    go_arches[arch] = 1
  end
  for arch in rpm.expand("%{nodejs_arches}"):gmatch("%S+") do
    if go_arches[arch] then
      print(arch .. " ")
  end
end}

%global gomodulesmode               GO111MODULE=auto
%global gotestflags                 %{gotestflags} -tags=integration
%global esbuild_version             0.17.19
%global x_sys_version               c0bba94
%global google_wire_version         0.5.0
%global google_subcommands_version  1.2.0
%global x_tools_version             0.1.0
%global go_difflib_version          1.0.0
%global x_mod_version               0.3.0
%global wire_x_sys_version          b64e53b
%global x_xerrors_version           5ec99f8

Name:             grafana
Version:          10.2.3
Release:          3%{?dist}
Summary:          Metrics dashboard and graph editor
License:          AGPLv3
URL:              https://grafana.org

# Source0 contains the tagged upstream sources
Source0:          https://github.com/grafana/grafana/archive/v%{version}/%{name}-%{version}.tar.gz

# Source1 contains the esbuild sources
Source1:          https://github.com/evanw/esbuild/archive/v%{esbuild_version}/esbuild-v%{esbuild_version}.tar.gz

# Source2 contains the Go package golang.org/x/sys sources
Source2:          https://github.com/golang/sys/archive/%{x_sys_version}/sys-%{x_sys_version}.tar.gz

# Source3 contains the Go package github.com/google/wire sources
Source3:          https://github.com/google/wire/archive/v%{google_wire_version}/wire-v%{google_wire_version}.tar.gz

# Source4 contains the Go package github.com/google/subcommands sources
Source4:          https://github.com/google/subcommands/archive/v%{google_subcommands_version}/subcommands-v%{google_subcommands_version}.tar.gz

# Source5 contains the Go package golang.org/x/tools sources
Source5:          https://github.com/golang/tools/archive/v%{x_tools_version}/tools-v%{x_tools_version}.tar.gz

# Source6 contains the Go package github.com/pmezard/do-difflib sources
Source6:          https://github.com/pmezard/go-difflib/archive/v%{go_difflib_version}/go-difflib-v%{go_difflib_version}.tar.gz

# Source7 contains the Go package golang.org/x/mod sources
Source7:          https://github.com/golang/mod/archive/v%{x_mod_version}/mod-v%{x_mod_version}.tar.gz

# Source8 contains the Go package golang.org/x/sys sources for wire tool
Source8:          https://github.com/golang/sys/archive/%{wire_x_sys_version}/sys-%{wire_x_sys_version}.tar.gz

# Source9 contains the Go package golang.org/x/xerrors sources
Source9:          https://github.com/golang/xerrors/archive/%{x_xerrors_version}/xerrors-%{x_xerrors_version}.tar.gz

# Source10 contains the systemd-sysusers configuration
Source10:         grafana.sysusers

# Source11 contains configs for grafana
Source11:         grafana.ini

Patch1:           0001-disable-usage-of-slices-package.patch

Patch2:           0001-add-missing-packages-to-vendor.patch

# Intersection of go_arches and nodejs_arches
ExclusiveArch:    %{grafana_arches}

BuildRequires:    systemd
BuildRequires:    systemd-rpm-macros
BuildRequires:    golang >= 1.19
BuildRequires:    go-srpm-macros
BuildRequires:    go-rpm-macros

BuildRequires:    nodejs >= 1:16
BuildRequires:    yarnpkg

%if %{enable_fips_mode}
BuildRequires:    openssl-devel
%endif

%global           GRAFANA_USER %{name}
%global           GRAFANA_GROUP %{name}

# grafana-server service daemon uses systemd
%{?systemd_requires}
Requires(pre):    shadow-utils

# Grafana queries the mime database (through mime.TypeByExtension, in a unit test and at runtime)
BuildRequires:    shared-mime-info
Requires:         shared-mime-info

%if 0%{?fedora} || 0%{?rhel} > 7
Recommends: grafana-pcp
%endif

Obsoletes:        grafana-cloudwatch < 7.3.6-1
Obsoletes:        grafana-elasticsearch < 7.3.6-1
Obsoletes:        grafana-azure-monitor < 7.3.6-1
Obsoletes:        grafana-graphite < 7.3.6-1
Obsoletes:        grafana-influxdb < 7.3.6-1
Obsoletes:        grafana-loki < 7.3.6-1
Obsoletes:        grafana-mssql < 7.3.6-1
Obsoletes:        grafana-mysql < 7.3.6-1
Obsoletes:        grafana-opentsdb < 7.3.6-1
Obsoletes:        grafana-postgres < 7.3.6-1
Obsoletes:        grafana-prometheus < 7.3.6-1
Obsoletes:        grafana-stackdriver < 7.3.6-1
Provides:         grafana-cloudwatch = 7.3.6-1
Provides:         grafana-elasticsearch = 7.3.6-1
Provides:         grafana-azure-monitor = 7.3.6-1
Provides:         grafana-graphite = 7.3.6-1
Provides:         grafana-influxdb = 7.3.6-1
Provides:         grafana-loki = 7.3.6-1
Provides:         grafana-mssql = 7.3.6-1
Provides:         grafana-mysql = 7.3.6-1
Provides:         grafana-opentsdb = 7.3.6-1
Provides:         grafana-postgres = 7.3.6-1
Provides:         grafana-prometheus = 7.3.6-1
Provides:         grafana-stackdriver = 7.3.6-1

# vendored golang and node.js build dependencies
# this is for security purposes, if nodejs-foo ever needs an update,
# affected packages can be easily identified.
# Note: generated by the Makefile (see README.md)
Provides: bundled(golang(cloud.google.com/go/storage)) = 1.21.0
Provides: bundled(golang(cuelang.org/go)) = 0.4.3
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go)) = 59.3.0+incompatible
Provides: bundled(golang(github.com/Azure/go-autorest/autorest)) = 0.11.22
Provides: bundled(golang(github.com/BurntSushi/toml)) = 0.3.1
Provides: bundled(golang(github.com/Masterminds/semver)) = 1.5.0
Provides: bundled(golang(github.com/VividCortex/mysqlerr)) = 0.0.0-20170204212430.6c6b55f8796f
Provides: bundled(golang(github.com/aws/aws-sdk-go)) = 1.44.9
Provides: bundled(golang(github.com/beevik/etree)) = 1.1.0
Provides: bundled(golang(github.com/benbjohnson/clock)) = 1.1.0
Provides: bundled(golang(github.com/bradfitz/gomemcache)) = 0.0.0-20190913173617.a41fca850d0b
Provides: bundled(golang(github.com/centrifugal/centrifuge)) = 0.19.0
Provides: bundled(golang(github.com/cortexproject/cortex)) = 1.10.1-0.20211014125347.85c378182d0d
Provides: bundled(golang(github.com/davecgh/go-spew)) = 1.1.1
Provides: bundled(golang(github.com/denisenkom/go-mssqldb)) = 0.12.0
Provides: bundled(golang(github.com/dop251/goja)) = 0.0.0-20210804101310.32956a348b49
Provides: bundled(golang(github.com/fatih/color)) = 1.13.0
Provides: bundled(golang(github.com/gchaincl/sqlhooks)) = 1.3.0
Provides: bundled(golang(github.com/getsentry/sentry-go)) = 0.13.0
Provides: bundled(golang(github.com/go-kit/kit)) = 0.11.0
Provides: bundled(golang(github.com/go-openapi/strfmt)) = 0.20.2
Provides: bundled(golang(github.com/go-redis/redis/v8)) = 8.11.4
Provides: bundled(golang(github.com/go-sourcemap/sourcemap)) = 2.1.3+incompatible
Provides: bundled(golang(github.com/go-sql-driver/mysql)) = 1.6.0
Provides: bundled(golang(github.com/go-stack/stack)) = 1.8.0
Provides: bundled(golang(github.com/gobwas/glob)) = 0.2.3
Provides: bundled(golang(github.com/gofrs/uuid)) = 4.0.0+incompatible
Provides: bundled(golang(github.com/gogo/protobuf)) = 1.3.2
Provides: bundled(golang(github.com/golang/mock)) = 1.6.0
Provides: bundled(golang(github.com/golang/snappy)) = 0.0.4
Provides: bundled(golang(github.com/google/go-cmp)) = 0.5.8
Provides: bundled(golang(github.com/google/uuid)) = 1.3.0
Provides: bundled(golang(github.com/google/wire)) = 0.5.0
Provides: bundled(golang(github.com/gorilla/websocket)) = 1.4.2
Provides: bundled(golang(github.com/gosimple/slug)) = 1.9.0
Provides: bundled(golang(github.com/grafana/cuetsy)) = 0.0.1
Provides: bundled(golang(github.com/grafana/grafana-aws-sdk)) = 0.10.7
Provides: bundled(golang(github.com/grafana/grafana-azure-sdk-go)) = 1.3.0
Provides: bundled(golang(github.com/grafana/grafana-plugin-sdk-go)) = 0.138.0
Provides: bundled(golang(github.com/grafana/loki)) = 1.6.2-0.20211015002020.7832783b1caa
Provides: bundled(golang(github.com/grpc-ecosystem/go-grpc-middleware)) = 1.3.0
Provides: bundled(golang(github.com/hashicorp/go-hclog)) = 1.0.0
Provides: bundled(golang(github.com/hashicorp/go-plugin)) = 1.4.3
Provides: bundled(golang(github.com/hashicorp/go-version)) = 1.3.0
Provides: bundled(golang(github.com/influxdata/influxdb-client-go/v2)) = 2.6.0
Provides: bundled(golang(github.com/influxdata/line-protocol)) = 0.0.0-20210311194329.9aa0e372d097
Provides: bundled(golang(github.com/jmespath/go-jmespath)) = 0.4.0
Provides: bundled(golang(github.com/json-iterator/go)) = 1.1.12
Provides: bundled(golang(github.com/lib/pq)) = 1.10.4
Provides: bundled(golang(github.com/linkedin/goavro/v2)) = 2.10.0
Provides: bundled(golang(github.com/m3db/prometheus_remote_client_golang)) = 0.4.4
Provides: bundled(golang(github.com/magefile/mage)) = 1.13.0
Provides: bundled(golang(github.com/mattn/go-isatty)) = 0.0.14
Provides: bundled(golang(github.com/mattn/go-sqlite3)) = 1.14.7
Provides: bundled(golang(github.com/matttproud/golang_protobuf_extensions)) = 1.0.2-0.20181231171920.c182affec369
Provides: bundled(golang(github.com/mwitkow/go-conntrack)) = 0.0.0-20190716064945.2f068394615f
Provides: bundled(golang(github.com/ohler55/ojg)) = 1.12.9
Provides: bundled(golang(github.com/opentracing/opentracing-go)) = 1.2.0
Provides: bundled(golang(github.com/patrickmn/go-cache)) = 2.1.0+incompatible
Provides: bundled(golang(github.com/pkg/errors)) = 0.9.1
Provides: bundled(golang(github.com/prometheus/alertmanager)) = 0.23.1-0.20211116083607.e2a10119aaf7
Provides: bundled(golang(github.com/prometheus/client_golang)) = 1.12.1
Provides: bundled(golang(github.com/prometheus/client_model)) = 0.2.0
Provides: bundled(golang(github.com/prometheus/common)) = 0.32.1
Provides: bundled(golang(github.com/prometheus/prometheus)) = 1.8.2-0.20211011171444.354d8d2ecfac
Provides: bundled(golang(github.com/robfig/cron/v3)) = 3.0.1
Provides: bundled(golang(github.com/russellhaering/goxmldsig)) = 1.1.1
Provides: bundled(golang(github.com/stretchr/testify)) = 1.7.2
Provides: bundled(golang(github.com/teris-io/shortid)) = 0.0.0-20171029131806.771a37caa5cf
Provides: bundled(golang(github.com/ua-parser/uap-go)) = 0.0.0-20211112212520.00c877edfe0f
Provides: bundled(golang(github.com/uber/jaeger-client-go)) = 2.29.1+incompatible
Provides: bundled(golang(github.com/unknwon/com)) = 1.0.1
Provides: bundled(golang(github.com/urfave/cli/v2)) = 2.3.0
Provides: bundled(golang(github.com/vectordotdev/go-datemath)) = 0.1.1-0.20220323213446.f3954d0b18ae
Provides: bundled(golang(github.com/xorcare/pointer)) = 1.1.0
Provides: bundled(golang(github.com/yudai/gojsondiff)) = 1.0.0
Provides: bundled(golang(go.opentelemetry.io/collector)) = 0.31.0
Provides: bundled(golang(go.opentelemetry.io/collector/model)) = 0.31.0
Provides: bundled(golang(go.opentelemetry.io/otel)) = 1.6.3
Provides: bundled(golang(go.opentelemetry.io/otel/exporters/jaeger)) = 1.0.0
Provides: bundled(golang(go.opentelemetry.io/otel/sdk)) = 1.6.3
Provides: bundled(golang(go.opentelemetry.io/otel/trace)) = 1.6.3
Provides: bundled(golang(golang.org/x/crypto)) = 0.0.0-20220331220935.ae2d96664a29
Provides: bundled(golang(golang.org/x/exp)) = 0.0.0-20210220032938.85be41e4509f
Provides: bundled(golang(golang.org/x/oauth2)) = 0.0.0-20220309155454.6242fa91716a
Provides: bundled(golang(golang.org/x/sync)) = 0.0.0-20210220032951.036812b2e83c
Provides: bundled(golang(golang.org/x/time)) = 0.0.0-20220224211638.0e9765cccd65
Provides: bundled(golang(golang.org/x/tools)) = 0.1.10
Provides: bundled(golang(gonum.org/v1/gonum)) = 0.11.0
Provides: bundled(golang(google.golang.org/api)) = 0.74.0
Provides: bundled(golang(google.golang.org/grpc)) = 1.45.0
Provides: bundled(golang(google.golang.org/protobuf)) = 1.28.0
Provides: bundled(golang(gopkg.in/ini.v1)) = 1.66.2
Provides: bundled(golang(gopkg.in/ldap.v3)) = 3.1.0
Provides: bundled(golang(gopkg.in/mail.v2)) = 2.3.1
Provides: bundled(golang(gopkg.in/square/go-jose.v2)) = 2.5.1
Provides: bundled(golang(gopkg.in/yaml.v2)) = 2.4.0
Provides: bundled(golang(gopkg.in/yaml.v3)) = 3.0.1
Provides: bundled(golang(xorm.io/builder)) = 0.3.6
Provides: bundled(golang(xorm.io/core)) = 0.7.3
Provides: bundled(golang(xorm.io/xorm)) = 0.8.2
Provides: bundled(golang(github.com/andybalholm/brotli)) = 1.0.3
Provides: bundled(golang(github.com/go-kit/log)) = 0.1.0
Provides: bundled(golang(github.com/go-openapi/loads)) = 0.20.2
Provides: bundled(golang(github.com/go-openapi/spec)) = 0.20.4
Provides: bundled(golang(github.com/googleapis/gax-go/v2)) = 2.2.0
Provides: bundled(golang(github.com/grafana/grafana-google-sdk-go)) = 0.0.0-20211104130251.b190293eaf58
Provides: bundled(golang(github.com/hashicorp/golang-lru)) = 0.5.4
Provides: bundled(golang(github.com/segmentio/encoding)) = 0.3.2
Provides: bundled(golang(go.uber.org/atomic)) = 1.9.0
Provides: bundled(golang(golang.org/x/text)) = 0.3.7
Provides: bundled(golang(google.golang.org/genproto)) = 0.0.0-20220421151946.72621c1f0bd3
Provides: bundled(golang(cloud.google.com/go/kms)) = 1.4.0
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/azidentity)) = 0.13.2
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/keyvault/azkeys)) = 0.4.0
Provides: bundled(golang(github.com/Azure/go-autorest/autorest/adal)) = 0.9.17
Provides: bundled(golang(github.com/armon/go-radix)) = 1.0.0
Provides: bundled(golang(github.com/blugelabs/bluge)) = 0.1.9
Provides: bundled(golang(github.com/golang-migrate/migrate/v4)) = 4.7.0
Provides: bundled(golang(github.com/grafana/dskit)) = 0.0.0-20211011144203.3a88ec0b675f
Provides: bundled(golang(github.com/grafana/thema)) = 0.0.0-20220523183731.72aebd14e751
Provides: bundled(golang(github.com/laher/mergefs)) = 0.1.1
Provides: bundled(golang(go.etcd.io/etcd/api/v3)) = 3.5.4
Provides: bundled(golang(go.opentelemetry.io/contrib/propagators/jaeger)) = 1.6.0
Provides: bundled(golang(go.opentelemetry.io/otel/exporters/otlp/otlptrace)) = 1.6.3
Provides: bundled(golang(go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc)) = 1.6.3
Provides: bundled(golang(gocloud.dev)) = 0.25.0
Provides: bundled(npm(@babel/core)) = 7.12.9
Provides: bundled(npm(@babel/plugin-proposal-class-properties)) = 7.16.7
Provides: bundled(npm(@babel/plugin-proposal-nullish-coalescing-operator)) = 7.16.7
Provides: bundled(npm(@babel/plugin-proposal-object-rest-spread)) = 7.12.1
Provides: bundled(npm(@babel/plugin-proposal-optional-chaining)) = 7.16.7
Provides: bundled(npm(@babel/plugin-syntax-dynamic-import)) = 7.8.3
Provides: bundled(npm(@babel/plugin-transform-react-constant-elements)) = 7.17.6
Provides: bundled(npm(@babel/plugin-transform-runtime)) = 7.17.0
Provides: bundled(npm(@babel/plugin-transform-typescript)) = 7.16.7
Provides: bundled(npm(@babel/preset-env)) = 7.16.11
Provides: bundled(npm(@babel/preset-react)) = 7.16.7
Provides: bundled(npm(@babel/preset-typescript)) = 7.16.7
Provides: bundled(npm(@betterer/betterer)) = 5.3.5
Provides: bundled(npm(@betterer/cli)) = 5.3.5
Provides: bundled(npm(@betterer/eslint)) = 5.3.5
Provides: bundled(npm(@betterer/regexp)) = 5.3.5
Provides: bundled(npm(@braintree/sanitize-url)) = 6.0.0
Provides: bundled(npm(@cypress/webpack-preprocessor)) = 5.11.1
Provides: bundled(npm(@emotion/css)) = 10.0.27
Provides: bundled(npm(@emotion/eslint-plugin)) = 11.7.0
Provides: bundled(npm(@emotion/react)) = 11.9.0
Provides: bundled(npm(@grafana/api-documenter)) = 7.11.2
Provides: bundled(npm(@grafana/aws-sdk)) = 0.0.36
Provides: bundled(npm(@grafana/data)) = 0.0.0-use.local
Provides: bundled(npm(@grafana/e2e)) = 0.0.0-use.local
Provides: bundled(npm(@grafana/e2e-selectors)) = 0.0.0-use.local
Provides: bundled(npm(@grafana/eslint-config)) = 4.0.0
Provides: bundled(npm(@grafana/experimental)) = 0.0.2-canary.30
Provides: bundled(npm(@grafana/google-sdk)) = 0.0.3
Provides: bundled(npm(@grafana/lezer-logql)) = 0.0.12
Provides: bundled(npm(@grafana/runtime)) = 0.0.0-use.local
Provides: bundled(npm(@grafana/schema)) = 0.0.0-use.local
Provides: bundled(npm(@grafana/toolkit)) = 0.0.0-use.local
Provides: bundled(npm(@grafana/tsconfig)) = 1.2.0rc1
Provides: bundled(npm(@grafana/ui)) = 0.0.0-use.local
Provides: bundled(npm(@jaegertracing/jaeger-ui-components)) = 0.0.0-use.local
Provides: bundled(npm(@jest/core)) = 27.5.1
Provides: bundled(npm(@kusto/monaco-kusto)) = 5.1.3
Provides: bundled(npm(@lezer/common)) = 0.15.12
Provides: bundled(npm(@lezer/lr)) = 0.15.8
Provides: bundled(npm(@lingui/cli)) = 3.13.3
Provides: bundled(npm(@lingui/core)) = 3.13.3
Provides: bundled(npm(@lingui/macro)) = 3.12.1
Provides: bundled(npm(@lingui/react)) = 3.13.3
Provides: bundled(npm(@mdx-js/react)) = 1.6.22
Provides: bundled(npm(@microsoft/api-extractor)) = 7.24.1
Provides: bundled(npm(@mochajs/json-file-reporter)) = 1.3.0
Provides: bundled(npm(@monaco-editor/react)) = 4.3.1
Provides: bundled(npm(@opentelemetry/api)) = 1.1.0
Provides: bundled(npm(@opentelemetry/exporter-collector)) = 0.25.0
Provides: bundled(npm(@opentelemetry/semantic-conventions)) = 0.25.0
Provides: bundled(npm(@pmmmwh/react-refresh-webpack-plugin)) = 0.5.4
Provides: bundled(npm(@popperjs/core)) = 2.11.2
Provides: bundled(npm(@react-aria/button)) = 3.4.4
Provides: bundled(npm(@react-aria/dialog)) = 3.1.9
Provides: bundled(npm(@react-aria/focus)) = 3.5.5
Provides: bundled(npm(@react-aria/interactions)) = 3.8.4
Provides: bundled(npm(@react-aria/menu)) = 3.4.4
Provides: bundled(npm(@react-aria/overlays)) = 3.8.2
Provides: bundled(npm(@react-aria/utils)) = 3.12.0
Provides: bundled(npm(@react-stately/collections)) = 3.3.8
Provides: bundled(npm(@react-stately/menu)) = 3.2.7
Provides: bundled(npm(@react-stately/tree)) = 3.2.4
Provides: bundled(npm(@react-types/button)) = 3.4.5
Provides: bundled(npm(@react-types/menu)) = 3.5.3
Provides: bundled(npm(@react-types/overlays)) = 3.5.5
Provides: bundled(npm(@react-types/shared)) = 3.12.0
Provides: bundled(npm(@reduxjs/toolkit)) = 1.8.1
Provides: bundled(npm(@rollup/plugin-alias)) = 3.1.9
Provides: bundled(npm(@rollup/plugin-commonjs)) = 22.0.0
Provides: bundled(npm(@rollup/plugin-json)) = 4.1.0
Provides: bundled(npm(@rollup/plugin-node-resolve)) = 13.3.0
Provides: bundled(npm(@rtsao/plugin-proposal-class-properties)) = 7.0.1-patch.1
Provides: bundled(npm(@sentry/browser)) = 6.19.7
Provides: bundled(npm(@sentry/types)) = 6.19.7
Provides: bundled(npm(@sentry/utils)) = 6.19.7
Provides: bundled(npm(@storybook/addon-a11y)) = 6.4.21
Provides: bundled(npm(@storybook/addon-actions)) = 6.4.21
Provides: bundled(npm(@storybook/addon-docs)) = 6.4.21
Provides: bundled(npm(@storybook/addon-essentials)) = 6.4.21
Provides: bundled(npm(@storybook/addon-knobs)) = 6.4.0
Provides: bundled(npm(@storybook/addon-storysource)) = 6.4.21
Provides: bundled(npm(@storybook/addons)) = 6.4.21
Provides: bundled(npm(@storybook/api)) = 6.4.21
Provides: bundled(npm(@storybook/builder-webpack5)) = 6.4.21
Provides: bundled(npm(@storybook/components)) = 6.4.21
Provides: bundled(npm(@storybook/core-events)) = 6.4.21
Provides: bundled(npm(@storybook/manager-webpack5)) = 6.4.21
Provides: bundled(npm(@storybook/react)) = 6.4.21
Provides: bundled(npm(@storybook/theming)) = 6.4.21
Provides: bundled(npm(@swc/core)) = 1.2.187
Provides: bundled(npm(@swc/helpers)) = 0.3.13
Provides: bundled(npm(@testing-library/dom)) = 8.13.0
Provides: bundled(npm(@testing-library/jest-dom)) = 5.16.4
Provides: bundled(npm(@testing-library/react)) = 12.1.4
Provides: bundled(npm(@testing-library/react-hooks)) = 8.0.0
Provides: bundled(npm(@testing-library/user-event)) = 14.2.0
Provides: bundled(npm(@types/angular)) = 1.8.3
Provides: bundled(npm(@types/angular-route)) = 1.7.2
Provides: bundled(npm(@types/chrome-remote-interface)) = 0.31.4
Provides: bundled(npm(@types/classnames)) = 2.3.0
Provides: bundled(npm(@types/command-exists)) = 1.2.0
Provides: bundled(npm(@types/common-tags)) = 1.8.1
Provides: bundled(npm(@types/d3)) = 7.1.0
Provides: bundled(npm(@types/d3-force)) = 2.1.4
Provides: bundled(npm(@types/d3-interpolate)) = 1.4.2
Provides: bundled(npm(@types/d3-scale-chromatic)) = 1.3.1
Provides: bundled(npm(@types/debounce-promise)) = 3.1.4
Provides: bundled(npm(@types/deep-freeze)) = 0.1.2
Provides: bundled(npm(@types/enzyme)) = 3.10.10
Provides: bundled(npm(@types/enzyme-adapter-react-16)) = 1.0.6
Provides: bundled(npm(@types/eslint)) = 7.28.2
Provides: bundled(npm(@types/file-saver)) = 2.0.5
Provides: bundled(npm(@types/fs-extra)) = 8.1.2
Provides: bundled(npm(@types/google.analytics)) = 0.0.42
Provides: bundled(npm(@types/history)) = 4.7.9
Provides: bundled(npm(@types/hoist-non-react-statics)) = 3.3.1
Provides: bundled(npm(@types/inquirer)) = 8.2.1
Provides: bundled(npm(@types/is-hotkey)) = 0.1.7
Provides: bundled(npm(@types/jest)) = 26.0.15
Provides: bundled(npm(@types/jquery)) = 3.5.14
Provides: bundled(npm(@types/js-yaml)) = 4.0.5
Provides: bundled(npm(@types/jsurl)) = 1.2.30
Provides: bundled(npm(@types/lingui__macro)) = 3.0.0
Provides: bundled(npm(@types/lodash)) = 4.14.149
Provides: bundled(npm(@types/logfmt)) = 1.2.2
Provides: bundled(npm(@types/marked)) = 4.0.3
Provides: bundled(npm(@types/mock-raf)) = 1.0.3
Provides: bundled(npm(@types/mousetrap)) = 1.6.9
Provides: bundled(npm(@types/node)) = 12.20.24
Provides: bundled(npm(@types/papaparse)) = 5.3.2
Provides: bundled(npm(@types/pluralize)) = 0.0.29
Provides: bundled(npm(@types/prettier)) = 2.4.2
Provides: bundled(npm(@types/prismjs)) = 1.26.0
Provides: bundled(npm(@types/prop-types)) = 15.7.4
Provides: bundled(npm(@types/rc-time-picker)) = 3.4.1
Provides: bundled(npm(@types/react)) = 17.0.30
Provides: bundled(npm(@types/react-beautiful-dnd)) = 13.1.2
Provides: bundled(npm(@types/react-calendar)) = 3.5.1
Provides: bundled(npm(@types/react-color)) = 3.0.6
Provides: bundled(npm(@types/react-dev-utils)) = 9.0.10
Provides: bundled(npm(@types/react-dom)) = 17.0.10
Provides: bundled(npm(@types/react-grid-layout)) = 1.3.2
Provides: bundled(npm(@types/react-highlight-words)) = 0.16.4
Provides: bundled(npm(@types/react-icons)) = 2.2.7
Provides: bundled(npm(@types/react-loadable)) = 5.5.6
Provides: bundled(npm(@types/react-redux)) = 7.1.20
Provides: bundled(npm(@types/react-resizable)) = 3.0.0
Provides: bundled(npm(@types/react-router-dom)) = 5.3.3
Provides: bundled(npm(@types/react-table)) = 7.7.12
Provides: bundled(npm(@types/react-test-renderer)) = 17.0.1
Provides: bundled(npm(@types/react-transition-group)) = 4.4.4
Provides: bundled(npm(@types/react-virtualized-auto-sizer)) = 1.0.1
Provides: bundled(npm(@types/react-window)) = 1.8.5
Provides: bundled(npm(@types/react-window-infinite-loader)) = 1.0.6
Provides: bundled(npm(@types/redux-mock-store)) = 1.0.3
Provides: bundled(npm(@types/reselect)) = 2.2.0
Provides: bundled(npm(@types/rimraf)) = 3.0.2
Provides: bundled(npm(@types/semver)) = 7.3.9
Provides: bundled(npm(@types/sinon)) = 10.0.11
Provides: bundled(npm(@types/slate)) = 0.47.9
Provides: bundled(npm(@types/slate-plain-serializer)) = 0.7.2
Provides: bundled(npm(@types/slate-react)) = 0.22.9
Provides: bundled(npm(@types/systemjs)) = 0.20.8
Provides: bundled(npm(@types/testing-library__jest-dom)) = 5.14.1
Provides: bundled(npm(@types/testing-library__react-hooks)) = 3.4.1
Provides: bundled(npm(@types/tinycolor2)) = 1.4.3
Provides: bundled(npm(@types/tmp)) = 0.2.3
Provides: bundled(npm(@types/uuid)) = 8.3.3
Provides: bundled(npm(@typescript-eslint/eslint-plugin)) = 5.16.0
Provides: bundled(npm(@typescript-eslint/parser)) = 5.16.0
Provides: bundled(npm(@visx/event)) = 2.6.0
Provides: bundled(npm(@visx/gradient)) = 2.10.0
Provides: bundled(npm(@visx/group)) = 2.10.0
Provides: bundled(npm(@visx/scale)) = 2.2.2
Provides: bundled(npm(@visx/shape)) = 2.10.0
Provides: bundled(npm(@visx/tooltip)) = 2.10.0
Provides: bundled(npm(@welldone-software/why-did-you-render)) = 7.0.1
Provides: bundled(npm(@wojtekmaj/enzyme-adapter-react-17)) = 0.6.7
Provides: bundled(npm(angular)) = 1.8.3
Provides: bundled(npm(angular-bindonce)) = 0.3.1
Provides: bundled(npm(angular-route)) = 1.8.3
Provides: bundled(npm(angular-sanitize)) = 1.8.3
Provides: bundled(npm(ansicolor)) = 1.1.100
Provides: bundled(npm(app)) = 0.0.0-use.local
Provides: bundled(npm(autoprefixer)) = 9.8.8
Provides: bundled(npm(axios)) = 0.25.0
Provides: bundled(npm(babel-jest)) = 27.5.1
Provides: bundled(npm(babel-loader)) = 8.2.3
Provides: bundled(npm(babel-plugin-angularjs-annotate)) = 0.10.0
Provides: bundled(npm(babel-plugin-macros)) = 2.8.0
Provides: bundled(npm(baron)) = 3.0.3
Provides: bundled(npm(blink-diff)) = 1.0.13
Provides: bundled(npm(brace)) = 0.11.1
Provides: bundled(npm(calculate-size)) = 1.1.1
Provides: bundled(npm(centrifuge)) = 2.8.5
Provides: bundled(npm(chalk)) = 2.4.2
Provides: bundled(npm(chance)) = 1.1.8
Provides: bundled(npm(chrome-remote-interface)) = 0.31.2
Provides: bundled(npm(classnames)) = 2.3.1
Provides: bundled(npm(combokeys)) = 3.0.1
Provides: bundled(npm(comlink)) = 4.3.1
Provides: bundled(npm(command-exists)) = 1.2.9
Provides: bundled(npm(commander)) = 2.11.0
Provides: bundled(npm(common-tags)) = 1.8.0
Provides: bundled(npm(copy-to-clipboard)) = 3.3.1
Provides: bundled(npm(copy-webpack-plugin)) = 9.0.1
Provides: bundled(npm(core-js)) = 2.6.12
Provides: bundled(npm(css-loader)) = 3.6.0
Provides: bundled(npm(css-minimizer-webpack-plugin)) = 3.4.1
Provides: bundled(npm(csstype)) = 2.6.18
Provides: bundled(npm(cypress)) = 9.5.1
Provides: bundled(npm(cypress-file-upload)) = 5.0.8
Provides: bundled(npm(d3)) = 5.15.0
Provides: bundled(npm(d3-force)) = 1.2.1
Provides: bundled(npm(d3-interpolate)) = 1.4.0
Provides: bundled(npm(d3-scale-chromatic)) = 1.5.0
Provides: bundled(npm(dangerously-set-html-content)) = 1.0.9
Provides: bundled(npm(date-fns)) = 2.25.0
Provides: bundled(npm(debounce-promise)) = 3.1.2
Provides: bundled(npm(deep-freeze)) = 0.0.1
Provides: bundled(npm(devtools-protocol)) = 0.0.927104
Provides: bundled(npm(emotion)) = 10.0.27
Provides: bundled(npm(enzyme)) = 3.11.0
Provides: bundled(npm(enzyme-to-json)) = 3.6.2
Provides: bundled(npm(eslint)) = 8.11.0
Provides: bundled(npm(eslint-config-prettier)) = 8.5.0
Provides: bundled(npm(eslint-plugin-import)) = 2.26.0
Provides: bundled(npm(eslint-plugin-jest)) = 26.2.2
Provides: bundled(npm(eslint-plugin-jsdoc)) = 38.0.6
Provides: bundled(npm(eslint-plugin-lodash)) = 7.4.0
Provides: bundled(npm(eslint-plugin-react)) = 7.29.4
Provides: bundled(npm(eslint-plugin-react-hooks)) = 4.3.0
Provides: bundled(npm(eslint-webpack-plugin)) = 3.1.1
Provides: bundled(npm(eventemitter3)) = 4.0.7
Provides: bundled(npm(execa)) = 1.0.0
Provides: bundled(npm(expose-loader)) = 4.0.0
Provides: bundled(npm(fast-deep-equal)) = 3.1.3
Provides: bundled(npm(fast-json-patch)) = 3.1.1
Provides: bundled(npm(file-loader)) = 6.2.0
Provides: bundled(npm(file-saver)) = 2.0.5
Provides: bundled(npm(fork-ts-checker-webpack-plugin)) = 4.1.6
Provides: bundled(npm(fs-extra)) = 0.30.0
Provides: bundled(npm(fuzzy)) = 0.1.3
Provides: bundled(npm(glob)) = 7.2.0
Provides: bundled(npm(globby)) = 9.2.0
Provides: bundled(npm(history)) = 4.10.1
Provides: bundled(npm(hoist-non-react-statics)) = 3.3.2
Provides: bundled(npm(html-loader)) = 3.1.0
Provides: bundled(npm(html-webpack-plugin)) = 4.5.2
Provides: bundled(npm(http-server)) = 14.1.0
Provides: bundled(npm(husky)) = 8.0.1
Provides: bundled(npm(iconscout-unicons-tarball)) = 1.0.0
Provides: bundled(npm(immer)) = 9.0.7
Provides: bundled(npm(immutable)) = 3.8.2
Provides: bundled(npm(inquirer)) = 7.3.3
Provides: bundled(npm(is-hotkey)) = 0.1.4
Provides: bundled(npm(jest)) = 27.5.1
Provides: bundled(npm(jest-canvas-mock)) = 2.3.1
Provides: bundled(npm(jest-coverage-badges)) = 1.1.2
Provides: bundled(npm(jest-date-mock)) = 1.0.8
Provides: bundled(npm(jest-fail-on-console)) = 2.4.1
Provides: bundled(npm(jest-junit)) = 13.1.0
Provides: bundled(npm(jest-matcher-utils)) = 27.5.1
Provides: bundled(npm(jest-mock-console)) = 1.2.3
Provides: bundled(npm(jquery)) = 3.5.1
Provides: bundled(npm(js-yaml)) = 3.13.1
Provides: bundled(npm(json-markup)) = 1.1.3
Provides: bundled(npm(json-source-map)) = 0.6.1
Provides: bundled(npm(jsurl)) = 0.1.5
Provides: bundled(npm(kbar)) = 0.1.0b34
Provides: bundled(npm(lerna)) = 4.0.0
Provides: bundled(npm(less)) = 4.1.2
Provides: bundled(npm(less-loader)) = 10.2.0
Provides: bundled(npm(lezer-promql)) = 0.22.0
Provides: bundled(npm(lint-staged)) = 12.4.1
Provides: bundled(npm(lodash)) = 4.17.21
Provides: bundled(npm(logfmt)) = 1.3.2
Provides: bundled(npm(lru-cache)) = 5.1.1
Provides: bundled(npm(lru-memoize)) = 1.1.0
Provides: bundled(npm(marked)) = 4.0.16
Provides: bundled(npm(md5-file)) = 5.0.0
Provides: bundled(npm(memoize-one)) = 4.0.3
Provides: bundled(npm(mini-css-extract-plugin)) = 2.6.0
Provides: bundled(npm(mocha)) = 10.0.0
Provides: bundled(npm(mock-raf)) = 1.0.1
Provides: bundled(npm(moment)) = 2.29.4
Provides: bundled(npm(moment-timezone)) = 0.5.34
Provides: bundled(npm(monaco-editor)) = 0.31.1
Provides: bundled(npm(monaco-promql)) = 1.7.4
Provides: bundled(npm(mousetrap)) = 1.6.5
Provides: bundled(npm(mousetrap-global-bind)) = 1.1.0
Provides: bundled(npm(moveable)) = 0.29.8
Provides: bundled(npm(mutationobserver-shim)) = 0.3.7
Provides: bundled(npm(ngtemplate-loader)) = 2.1.0
Provides: bundled(npm(node-notifier)) = 10.0.1
Provides: bundled(npm(nodemon)) = 2.0.16
Provides: bundled(npm(ol)) = 6.14.1
Provides: bundled(npm(ora)) = 5.4.1
Provides: bundled(npm(papaparse)) = 5.3.1
Provides: bundled(npm(pixelmatch)) = 5.2.1
Provides: bundled(npm(pluralize)) = 8.0.0
Provides: bundled(npm(pngjs)) = 2.3.1
Provides: bundled(npm(postcss)) = 7.0.39
Provides: bundled(npm(postcss-flexbugs-fixes)) = 4.2.1
Provides: bundled(npm(postcss-loader)) = 4.3.0
Provides: bundled(npm(postcss-preset-env)) = 7.4.3
Provides: bundled(npm(postcss-reporter)) = 7.0.5
Provides: bundled(npm(postcss-scss)) = 4.0.2
Provides: bundled(npm(prettier)) = 2.3.0
Provides: bundled(npm(prismjs)) = 1.27.0
Provides: bundled(npm(process)) = 0.11.10
Provides: bundled(npm(prop-types)) = 15.7.2
Provides: bundled(npm(raw-loader)) = 4.0.2
Provides: bundled(npm(rc-cascader)) = 3.5.0
Provides: bundled(npm(rc-drawer)) = 4.4.3
Provides: bundled(npm(rc-slider)) = 9.7.5
Provides: bundled(npm(rc-time-picker)) = 3.7.3
Provides: bundled(npm(re-resizable)) = 6.9.9
Provides: bundled(npm(react)) = 17.0.1
Provides: bundled(npm(react-beautiful-dnd)) = 13.1.0
Provides: bundled(npm(react-calendar)) = 3.7.0
Provides: bundled(npm(react-colorful)) = 5.5.1
Provides: bundled(npm(react-custom-scrollbars-2)) = 4.4.0
Provides: bundled(npm(react-dev-utils)) = 12.0.0
Provides: bundled(npm(react-diff-viewer)) = 3.1.1
Provides: bundled(npm(react-docgen-typescript-loader)) = 3.7.2
Provides: bundled(npm(react-dom)) = 17.0.1
Provides: bundled(npm(react-draggable)) = 4.4.4
Provides: bundled(npm(react-dropzone)) = 12.0.4
Provides: bundled(npm(react-grid-layout)) = 1.3.4
Provides: bundled(npm(react-highlight-words)) = 0.18.0
Provides: bundled(npm(react-hook-form)) = 7.5.3
Provides: bundled(npm(react-icons)) = 2.2.7
Provides: bundled(npm(react-inlinesvg)) = 2.3.0
Provides: bundled(npm(react-loadable)) = 5.5.0
Provides: bundled(npm(react-moveable)) = 0.32.7
Provides: bundled(npm(react-popper)) = 2.2.5
Provides: bundled(npm(react-popper-tooltip)) = 3.1.1
Provides: bundled(npm(react-redux)) = 7.2.6
Provides: bundled(npm(react-refresh)) = 0.11.0
Provides: bundled(npm(react-resizable)) = 3.0.4
Provides: bundled(npm(react-reverse-portal)) = 2.1.0
Provides: bundled(npm(react-router-dom)) = 5.3.0
Provides: bundled(npm(react-select)) = 3.2.0
Provides: bundled(npm(react-select-event)) = 5.3.0
Provides: bundled(npm(react-split-pane)) = 0.1.92
Provides: bundled(npm(react-table)) = 7.8.0
Provides: bundled(npm(react-test-renderer)) = 17.0.2
Provides: bundled(npm(react-transition-group)) = 4.4.2
Provides: bundled(npm(react-use)) = 17.3.2
Provides: bundled(npm(react-virtualized-auto-sizer)) = 1.0.6
Provides: bundled(npm(react-window)) = 1.8.7
Provides: bundled(npm(react-window-infinite-loader)) = 1.0.7
Provides: bundled(npm(redux)) = 4.1.1
Provides: bundled(npm(redux-mock-store)) = 1.5.4
Provides: bundled(npm(redux-thunk)) = 2.4.1
Provides: bundled(npm(regenerator-runtime)) = 0.11.1
Provides: bundled(npm(replace-in-file-webpack-plugin)) = 1.0.6
Provides: bundled(npm(reselect)) = 4.1.0
Provides: bundled(npm(resolve-as-bin)) = 2.1.0
Provides: bundled(npm(rimraf)) = 2.7.1
Provides: bundled(npm(rollup)) = 2.74.1
Provides: bundled(npm(rollup-plugin-copy)) = 3.4.0
Provides: bundled(npm(rollup-plugin-sourcemaps)) = 0.6.3
Provides: bundled(npm(rollup-plugin-svg-import)) = 1.6.0
Provides: bundled(npm(rollup-plugin-terser)) = 7.0.2
Provides: bundled(npm(rst2html)) = 1.0.4
Provides: bundled(npm(rxjs)) = 6.6.7
Provides: bundled(npm(sass)) = 1.50.1
Provides: bundled(npm(sass-loader)) = 12.6.0
Provides: bundled(npm(search-query-parser)) = 1.6.0
Provides: bundled(npm(selecto)) = 1.16.2
Provides: bundled(npm(semver)) = 5.7.1
Provides: bundled(npm(simple-git)) = 3.7.1
Provides: bundled(npm(sinon)) = 14.0.0
Provides: bundled(npm(slate)) = 0.47.9
Provides: bundled(npm(slate-plain-serializer)) = 0.7.11
Provides: bundled(npm(slate-react)) = 0.22.10
Provides: bundled(npm(storybook-dark-mode)) = 1.1.0
Provides: bundled(npm(style-loader)) = 1.3.0
Provides: bundled(npm(stylelint)) = 14.8.2
Provides: bundled(npm(stylelint-config-prettier)) = 9.0.3
Provides: bundled(npm(stylelint-config-sass-guidelines)) = 9.0.1
Provides: bundled(npm(symbol-observable)) = 4.0.0
Provides: bundled(npm(systemjs)) = 0.20.19
Provides: bundled(npm(terser-webpack-plugin)) = 1.4.5
Provides: bundled(npm(test)) = 0.0.0-use.local
Provides: bundled(npm(testing-library-selector)) = 0.2.1
Provides: bundled(npm(tether-drop)) = 1.5.0
Provides: bundled(npm(tinycolor2)) = 1.4.2
Provides: bundled(npm(tracelib)) = 1.0.1
Provides: bundled(npm(ts-jest)) = 27.1.3
Provides: bundled(npm(ts-loader)) = 6.2.1
Provides: bundled(npm(ts-node)) = 9.1.1
Provides: bundled(npm(tslib)) = 1.14.1
Provides: bundled(npm(tween-functions)) = 1.2.0
Provides: bundled(npm(typescript)) = 4.5.5
Provides: bundled(npm(uplot)) = 1.6.22
Provides: bundled(npm(url-loader)) = 4.1.1
Provides: bundled(npm(uuid)) = 3.4.0
Provides: bundled(npm(vendor)) = 0.0.0-use.local
Provides: bundled(npm(visjs-network)) = 4.25.0
Provides: bundled(npm(wait-on)) = 6.0.1
Provides: bundled(npm(webpack)) = 4.46.0
Provides: bundled(npm(webpack-bundle-analyzer)) = 4.5.0
Provides: bundled(npm(webpack-cli)) = 4.9.2
Provides: bundled(npm(webpack-dev-server)) = 4.9.0
Provides: bundled(npm(webpack-filter-warnings-plugin)) = 1.2.1
Provides: bundled(npm(webpack-merge)) = 5.8.0
Provides: bundled(npm(whatwg-fetch)) = 3.6.2
Provides: bundled(npm(xss)) = 1.0.11
Provides: bundled(npm(yaml)) = 1.10.2


%description
Grafana is an open source, feature rich metrics dashboard and graph editor for
Graphite, InfluxDB & OpenTSDB.


%prep
%setup -q -T -D -b 0
%setup -q -T -D -b 1
%setup -q -T -D -b 2
%setup -q -T -D -b 3
%setup -q -T -D -b 4
%setup -q -T -D -b 5
%setup -q -T -D -b 6
%setup -q -T -D -b 7
%setup -q -T -D -b 8
%setup -q -T -D -b 9

%patch1 -p1
%patch2 -p1

%build
mkdir %{_builddir}/bin

# Build the esbuild tool

pushd %{_builddir}/esbuild-%{esbuild_version}
  mkdir -p vendor/golang.org/x
  ln -s %{_builddir}/sys-%{x_sys_version}* vendor/golang.org/x/sys
  go build -mod=vendor -o %{_builddir}/bin/esbuild ./cmd/esbuild
popd
export ESBUILD_BINARY_PATH="%{_builddir}/bin/esbuild"

# Build the wire tool

pushd %{_builddir}/wire-%{google_wire_version}
  mkdir -p vendor/github.com/{golang,google,pmezard}
  mkdir -p vendor/golang.org/x
  ln -s %{_builddir}/tools-%{x_tools_version} vendor/golang.org/x/tools
  ln -s %{_builddir}/mod-%{x_mod_version} vendor/golang.org/x/mod
  ln -s %{_builddir}/sys-%{wire_x_sys_version}* vendor/golang.org/x/sys
  ln -s %{_builddir}/xerrors-%{x_xerrors_version}* vendor/golang.org/x/xerrors
  ln -s %{_builddir}/subcommands-%{google_subcommands_version} vendor/github.com/google/subcommands
  ln -s %{_builddir}/go-difflib-%{go_difflib_version} vendor/github.com/pmezard/go-difflib

  go build -mod=vendor -o %{_builddir}/bin/wire ./cmd/wire
popd

# Build the frontend

pushd %{_builddir}/%{name}-%{version}
  # Webpack needs more than the default 4GB RAM
  export NODE_OPTIONS="${NODE_OPTIONS:-} --max_old_space_size=6144"

  yarn run build

  # Build the bundled plugins
  mkdir -p plugins-bundled/external
  yarn run plugins:build-bundled
  for plugin in plugins-bundled/internal/input-datasource; do
    mv $plugin $plugin.tmp
    mv $plugin.tmp/dist $plugin
    rm -rf $plugin.tmp
  done
  rm plugins-bundled/README.md plugins-bundled/.gitignore plugins-bundled/external.json
popd

# Build the backend

pushd %{_builddir}/%{name}-%{version}
  # required since RHEL 8.8 to fix the following error:
  # "imports crypto/boring: build constraints exclude all Go files in /usr/lib/golang/src/crypto/boring"
  # can be removed in a future Go release
  export GOEXPERIMENT=boringcrypto
  # see grafana-X.Y.Z/pkg/build/cmd.go
  export LDFLAGS="-s -w -X main.version=%{version} -X main.buildstamp=${SOURCE_DATE_EPOCH}"

  %{_builddir}/bin/wire gen -tags oss ./pkg/server ./pkg/cmd/grafana-cli/runner
  go build -ldflags "${LDFLAGS:-}" -o %{_builddir}/bin/grafana ./pkg/cmd/grafana
  go build -ldflags "${LDFLAGS:-}" -o %{_builddir}/bin/grafana-server ./pkg/cmd/grafana-server
popd

%install
# dirs, shared files, public html, webpack
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_datadir}/%{name}
cp -a conf public plugins-bundled %{buildroot}%{_datadir}/%{name}

# binaries
install -p -m 755 %{_builddir}/bin/%{name}-server %{buildroot}%{_sbindir}
install -p -m 755 %{_builddir}/bin/%{name} %{buildroot}%{_sbindir}

# config dirs
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_sysconfdir}/%{name}/provisioning
install -d %{buildroot}%{_sysconfdir}/%{name}/provisioning/access-control
install -d %{buildroot}%{_sysconfdir}/%{name}/provisioning/dashboards
install -d %{buildroot}%{_sysconfdir}/%{name}/provisioning/datasources
install -d %{buildroot}%{_sysconfdir}/%{name}/provisioning/notifiers
install -d %{buildroot}%{_sysconfdir}/%{name}/provisioning/plugins

# config defaults
install -p -m 640 %{SOURCE11} %{buildroot}%{_sysconfdir}/%{name}/grafana.ini
install -p -m 640 conf/ldap.toml %{buildroot}%{_sysconfdir}/%{name}/ldap.toml
install -p -m 644 conf/defaults.ini %{buildroot}%{_datadir}/%{name}/conf/defaults.ini
install -p -m 644 conf/sample.ini %{buildroot}%{_datadir}/%{name}/conf/sample.ini

# config database directory and plugins
install -d -m 750 %{buildroot}%{_sharedstatedir}/%{name}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{name}/plugins

# log directory
install -d %{buildroot}%{_localstatedir}/log/%{name}

# systemd service files
install -d %{buildroot}%{_unitdir} # only needed for manual rpmbuilds
install -p -m 644 packaging/rpm/systemd/grafana-server.service \
    %{buildroot}%{_unitdir}

# daemon run pid file config for using tmpfs
install -d %{buildroot}%{_tmpfilesdir}
echo "d %{_rundir}/%{name} 0755 %{GRAFANA_USER} %{GRAFANA_GROUP} -" \
    > %{buildroot}%{_tmpfilesdir}/%{name}.conf

# systemd-sysusers configuration
install -p -m 644 -D %{SOURCE10} %{buildroot}%{_sysusersdir}/%{name}.conf

%pre
%sysusers_create_compat %{SOURCE10}

%preun
%systemd_preun grafana-server.service

%post
%systemd_post grafana-server.service
# create grafana.db with secure permissions on new installations
# otherwise grafana-server is creating grafana.db on first start
# with world-readable permissions, which may leak encrypted datasource
# passwords to all users (if the secret_key in grafana.ini was not changed)

# https://bugzilla.redhat.com/show_bug.cgi?id=1805472
if [ "$1" = 1 ] && [ ! -f %{_sharedstatedir}/%{name}/grafana.db ]; then
    touch %{_sharedstatedir}/%{name}/grafana.db
fi

# apply secure permissions to grafana.db if it exists
# (may not exist on upgrades, because users can choose between sqlite/mysql/postgres)
if [ -f %{_sharedstatedir}/%{name}/grafana.db ]; then
    chown %{GRAFANA_USER}:%{GRAFANA_GROUP} %{_sharedstatedir}/%{name}/grafana.db
    chmod 640 %{_sharedstatedir}/%{name}/grafana.db
fi

# required for upgrades
chmod 640 %{_sysconfdir}/%{name}/grafana.ini
chmod 640 %{_sysconfdir}/%{name}/ldap.toml

%postun
%systemd_postun_with_restart grafana-server.service

%files
# binaries
%{_sbindir}/%{name}-server
%{_sbindir}/%{name}

# config files
%dir %{_sysconfdir}/%{name}
%attr(0755, root, %{GRAFANA_GROUP}) %dir %{_sysconfdir}/%{name}/provisioning
%attr(0755, root, %{GRAFANA_GROUP}) %dir %{_sysconfdir}/%{name}/provisioning/access-control
%attr(0755, root, %{GRAFANA_GROUP}) %dir %{_sysconfdir}/%{name}/provisioning/dashboards
%attr(0750, root, %{GRAFANA_GROUP}) %dir %{_sysconfdir}/%{name}/provisioning/datasources
%attr(0755, root, %{GRAFANA_GROUP}) %dir %{_sysconfdir}/%{name}/provisioning/notifiers
%attr(0755, root, %{GRAFANA_GROUP}) %dir %{_sysconfdir}/%{name}/provisioning/plugins
%attr(0640, root, %{GRAFANA_GROUP}) %config(noreplace) %{_sysconfdir}/%{name}/grafana.ini
%attr(0640, root, %{GRAFANA_GROUP}) %config(noreplace) %{_sysconfdir}/%{name}/ldap.toml

# config database directory and plugins
%attr(0750, %{GRAFANA_USER}, %{GRAFANA_GROUP}) %dir %{_sharedstatedir}/%{name}
%attr(-,    %{GRAFANA_USER}, %{GRAFANA_GROUP}) %dir %{_sharedstatedir}/%{name}/plugins

# shared directory and all files therein
%{_datadir}/%{name}

# systemd service file
%{_unitdir}/grafana-server.service

# Grafana configuration to dynamically create /run/grafana/grafana.pid on tmpfs
%{_tmpfilesdir}/%{name}.conf

# systemd-sysusers configuration file
%{_sysusersdir}/%{name}.conf

# log directory - grafana.log is created by grafana-server, and it does it's own log rotation
%attr(0755, %{GRAFANA_USER}, %{GRAFANA_GROUP}) %dir %{_localstatedir}/log/%{name}

# other docs and license
%license LICENSE LICENSING.md NOTICE.md
%doc CHANGELOG.md CODE_OF_CONDUCT.md CONTRIBUTING.md GOVERNANCE.md HALL_OF_FAME.md ISSUE_TRIAGE.md MAINTAINERS.md
%doc README.md ROADMAP.md SECURITY.md SUPPORT.md UPGRADING_DEPENDENCIES.md WORKFLOW.md


%changelog
* Mon Dec 11 2023 Jason Ng <oblitorum@gmail.com> 10.2.2-3
- Update Grafana to 10.2.2

* Fri Aug 04 2023 Jason Ng <oblitorum@gmail.com> 9.5.7-3
- Make it fit into SSM
- Update Grafana to 9.5.7

* Tue Nov 01 2022 Stan Cox <scox@redhat.com> 9.0.9-2
- resolve CVE-2022-39229 grafana: Using email as a username can prevent other users from signing in
- resolve CVE-2022-2880 CVE-2022-41715 grafana: various flaws

* Wed Sep 21 2022 Andreas Gerstmayr <agerstmayr@redhat.com> 9.0.9-1
- update to 9.0.9 tagged upstream community sources, see CHANGELOG
- resolve CVE-2022-35957 grafana: Escalation from admin to server admin when auth proxy is used (rhbz#2125530)

* Tue Sep 20 2022 Andreas Gerstmayr <agerstmayr@redhat.com> 9.0.8-2
- bump NVR

* Thu Sep 15 2022 Andreas Gerstmayr <agerstmayr@redhat.com> 9.0.8-1
- update to 9.0.8 tagged upstream community sources, see CHANGELOG
- do not list /usr/share/grafana/conf twice
- drop makefile in favor of create_bundles.sh script
- sync provides/obsoletes with CentOS versions
- drop husky patch

* Thu Aug 11 2022 Andreas Gerstmayr <agerstmayr@redhat.com> 7.5.15-3
- resolve CVE-2022-1962 golang: go/parser: stack exhaustion in all Parse* functions
- resolve CVE-2022-1705 golang: net/http: improper sanitization of Transfer-Encoding header
- resolve CVE-2022-32148 golang: net/http/httputil: NewSingleHostReverseProxy - omit X-Forwarded-For not working
- resolve CVE-2022-30631 golang: compress/gzip: stack exhaustion in Reader.Read
- resolve CVE-2022-30630 golang: io/fs: stack exhaustion in Glob
- resolve CVE-2022-30632 golang: path/filepath: stack exhaustion in Glob
- resolve CVE-2022-30635 golang: encoding/gob: stack exhaustion in Decoder.Decode
- resolve CVE-2022-28131 golang: encoding/xml: stack exhaustion in Decoder.Skip
- resolve CVE-2022-30633 golang: encoding/xml: stack exhaustion in Unmarshal

* Tue Jul 26 2022 Andreas Gerstmayr <agerstmayr@redhat.com> 7.5.15-2
- resolve CVE-2022-31107 grafana: OAuth account takeover

* Fri Apr 22 2022 Andreas Gerstmayr <agerstmayr@redhat.com> 7.5.15-1
- update to 7.5.15 tagged upstream community sources, see CHANGELOG
- resolve CVE-2022-21673 grafana: Forward OAuth Identity Token can allow users to access some data sources
- resolve CVE-2022-21702 grafana: XSS vulnerability in data source handling
- resolve CVE-2022-21703 grafana: CSRF vulnerability can lead to privilege escalation
- resolve CVE-2022-21713 grafana: IDOR vulnerability can lead to information disclosure
- resolve CVE-2021-23648 sanitize-url: XSS
- resolve CVE-2022-21698 prometheus/client_golang: Denial of service using InstrumentHandlerCounter
- declare Node.js dependencies of subpackages
- make vendor and webpack tarballs reproducible

* Tue Jan 18 2022 Andreas Gerstmayr <agerstmayr@redhat.com> 7.5.11-3
- use HMAC-SHA-256 instead of SHA-1 to generate password reset tokens
- update FIPS tests in check phase

* Thu Dec 16 2021 Andreas Gerstmayr <agerstmayr@redhat.com> 7.5.11-2
- resolve CVE-2021-44716 golang: net/http: limit growth of header canonicalization cache
- resolve CVE-2021-43813 grafana: directory traversal vulnerability for *.md files

* Mon Oct 11 2021 Andreas Gerstmayr <agerstmayr@redhat.com> 7.5.11-1
- update to 7.5.11 tagged upstream community sources, see CHANGELOG
- resolve CVE-2021-39226

* Thu Sep 30 2021 Andreas Gerstmayr <agerstmayr@redhat.com> 7.5.10-1
- update to 7.5.10 tagged upstream community sources, see CHANGELOG

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 7.5.9-3
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Thu Jul 08 2021 Andreas Gerstmayr <agerstmayr@redhat.com> 7.5.9-2
- remove unused dependency property-information
- always include FIPS patch in SRPM

* Fri Jun 25 2021 Andreas Gerstmayr <agerstmayr@redhat.com> 7.5.9-1
- update to 7.5.9 tagged upstream community sources, see CHANGELOG

* Tue Jun 22 2021 Mohan Boddu <mboddu@redhat.com> - 7.5.8-2
- Rebuilt for RHEL 9 BETA for openssl 3.0
  Related: rhbz#1971065

* Mon Jun 21 2021 Andreas Gerstmayr <agerstmayr@redhat.com> 7.5.8-1
- update to 7.5.8 tagged upstream community sources, see CHANGELOG
- remove unused dependencies selfsigned, http-signature and gofpdf

* Fri Jun 11 2021 Andreas Gerstmayr <agerstmayr@redhat.com> 7.5.7-2
- remove unused cryptographic implementations
- use cryptographic functions from OpenSSL if FIPS mode is enabled

* Tue May 25 2021 Andreas Gerstmayr <agerstmayr@redhat.com> 7.5.7-1
- update to 7.5.7 tagged upstream community sources, see CHANGELOG

* Thu Apr 15 2021 Mohan Boddu <mboddu@redhat.com> - 7.3.6-4
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Andreas Gerstmayr <agerstmayr@redhat.com> 7.3.6-2
- change working dir to $GRAFANA_HOME in grafana-cli wrapper (fixes Red Hat BZ #1916083)
- add pcp-redis-datasource to allow_loading_unsigned_plugins config option

* Mon Dec 21 2020 Andreas Gerstmayr <agerstmayr@redhat.com> 7.3.6-1
- update to 7.3.6 tagged upstream community sources, see CHANGELOG
- remove dependency on SAML (not supported in the open source version of Grafana)

* Wed Nov 25 2020 Andreas Gerstmayr <agerstmayr@redhat.com> 7.3.4-1
- update to 7.3.4 tagged upstream community sources, see CHANGELOG

* Tue Nov 10 2020 Andreas Gerstmayr <agerstmayr@redhat.com> 7.3.1-1
- update to 7.3.1 tagged upstream community sources, see CHANGELOG
- optionally bundle node.js dependencies and build and test frontend as part of the specfile
- change default provisioning path to /etc/grafana/provisioning (changed in version 7.1.1-1)
- resolve https://bugzilla.redhat.com/show_bug.cgi?id=1843170

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-2
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 30 2020 Andreas Gerstmayr <agerstmayr@redhat.com> 7.1.1-1
- update to 7.1.1 tagged upstream community sources, see CHANGELOG
- merge all datasources into main grafana package
- bundle golang dependencies

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 05 2020 Andreas Gerstmayr <agerstmayr@redhat.com> 6.7.4-1
- update to 6.7.4 tagged upstream community sources, see CHANGELOG
- security fix for CVE-2020-13379

* Tue Apr 28 2020 Andreas Gerstmayr <agerstmayr@redhat.com> 6.7.3-1
- update to 6.7.3 tagged upstream community sources, see CHANGELOG
- add scripts to list Go dependencies and bundled npmjs dependencies
- set Grafana version in Grafana UI and grafana-cli --version
- declare README.md as documentation of datasource plugins
- create grafana.db on first installation (fixes RH BZ #1805472)
- change permissions of /var/lib/grafana to 750 (CVE-2020-12458)
- change permissions of /var/lib/grafana/grafana.db to 640 and
  user/group grafana:grafana (CVE-2020-12458)
- change permissions of grafana.ini and ldap.toml to 640 (CVE-2020-12459)

* Wed Feb 26 2020 Mark Goodwin <mgoodwin@redhat.com> 6.6.2-1
- added patch0 to set the version string correctly
- removed patch 004-xerrors.patch, it's now upstream
- added several patches for golang vendored vrs build dep differences
- added patch to move grafana-cli binary to libexec dir
- update to 6.6.2 tagged upstream community sources, see CHANGELOG

* Wed Nov 20 2019 Mark Goodwin <mgoodwin@redhat.com> 6.3.6-1
- add weak depenency on grafana-pcp
- add patch to mute shellcheck SC1090 for grafana-cli
- update to 6.3.6 upstream community sources, see CHANGELOG

* Thu Sep 05 2019 Mark Goodwin <mgoodwin@redhat.com> 6.3.5-1
- drop uaparser patch now it's upstream
- add xerrors patch, see https://github.com/golang/go/issues/32246
- use vendor sources on rawhide until modules are fully supported
- update to latest upstream community sources, see CHANGELOG

* Fri Aug 30 2019 Mark Goodwin <mgoodwin@redhat.com> 6.3.4-1
- include fix for CVE-2019-15043
- add patch for uaparser on 32bit systems
- update to latest upstream community sources, see CHANGELOG

* Wed Jul 31 2019 Mark Goodwin <mgoodwin@redhat.com> 6.2.5-1
- update to latest upstream community sources, see CHANGELOG

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 07 2019 Mark Goodwin <mgoodwin@redhat.com> 6.2.2-1
- split out some datasource plugins to sub-packages
- update to latest upstream community sources, see CHANGELOG

* Wed Jun 05 2019 Mark Goodwin <mgoodwin@redhat.com> 6.2.1-1
- update to latest upstream community sources, see CHANGELOG

* Fri May 24 2019 Mark Goodwin <mgoodwin@redhat.com> 6.2.0-1
- update to latest upstream community sources
- drop a couple of patches

* Wed May 08 2019 Mark Goodwin <mgoodwin@redhat.com> 6.1.6-2
- add conditional unbundle_vendor_sources macro

* Tue Apr 30 2019 Mark Goodwin <mgoodwin@redhat.com> 6.1.6-1
- update to latest upstream stable release 6.1.6, see CHANGELOG
- includes jQuery 3.4.0 security update

* Wed Apr 24 2019 Mark Goodwin <mgoodwin@redhat.com> 6.1.4-1
- update to latest upstream stable release 6.1.4, see CHANGELOG
- use gobuild and gochecks macros, eliminate arch symlinks
- re-enable grafana-debugsource package
- fix GRAFANA_GROUP typo
- fix more modes for brp-mangle-shebangs
- vendor source unbundling now done in prep after patches
- remove all rhel and fedora conditional guff

* Tue Apr 16 2019 Mark Goodwin <mgoodwin@redhat.com> 6.1.3-1
- update to latest upstream stable release 6.1.3, see CHANGELOG
- unbundle all vendor sources, replace with BuildRequires, see
  the long list of blocker BZs linked to BZ#1670656
- BuildRequires go-plugin >= v1.0.0 for grpc_broker (thanks eclipseo)
- tweak make_webpack to no longer use grunt, switch to prod build
- add ExclusiveArch lua script (thanks quantum.analyst)
- move db directory and plugins to /var/lib/grafana
- split out into 6 patches, ready for upstream PRs
- add check to run go tests for gating checks

* Thu Apr 04 2019 Mark Goodwin <mgoodwin@redhat.com> 6.1.0-1
- update to latest upstream stable release 6.1.0, see CHANGELOG

* Thu Mar 21 2019 Mark Goodwin <mgoodwin@redhat.com> 6.0.2-1
- bump to latest upstream stable release 6.0.2-1
- unbundle almost all remaining vendor code, see linked blockers in BZ#1670656

* Fri Mar 15 2019 Mark Goodwin <mgoodwin@redhat.com> 6.0.1-3
- bump to latest upstream stable release 6.0.1-1

* Thu Mar 14 2019 Mark Goodwin <mgoodwin@redhat.com> 6.0.1-2
- unbundle and add BuildRequires for golang-github-rainycape-unidecode-devel

* Thu Mar 07 2019 Mark Goodwin <mgoodwin@redhat.com> 6.0.1-1
- update to v6.0.1 upstream sources, tweak distro config, re-do patch
- simplify make_webpack.sh script (Elliott Sales de Andrade)
- vendor/github.com/go-ldap is now gone, so don't unbundle it

* Thu Mar 07 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-11
- tweak after latest feedback, bump to 5.4.3-11 (BZ 1670656)
- build debuginfo package again
- unbundle BuildRequires for golang-github-hashicorp-version-devel
- remove some unneeded development files
- remove macros from changelog and other rpmlint tweaks

* Fri Feb 22 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-10
- tweak spec for available and unavailable (bundled) golang packages

* Wed Feb 20 2019 Xavier Bachelot <xavier@bachelot.org> 5.4.3-9
- Remove extraneous slash (cosmetic)
- Create directories just before moving stuff in them
- Truncate long lines
- Group all golang stuff
- Simplify BuildRequires/bundled Provides
- Sort BuildRequires/bundled Provides
- Fix bundled go packages Provides

* Fri Feb 15 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-8
- add BuildRequires (and unbundle) vendor sources available in Fedora
- declare Provides for remaining (bundled) vendor go sources
- do not attempt to unbundle anything on RHEL < 7 or Fedora < 28

* Thu Feb 07 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-7
- further refinement for spec doc section from Xavier Bachelot
- disable debug_package to avoid empty debugsourcefiles.list

* Wed Feb 06 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-6
- further refinement following review by Xavier Bachelot

* Tue Feb 05 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-5
- further refinement following review by Xavier Bachelot

* Fri Feb 01 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-4
- further spec updates after packaging review
- reworked post-install scriplets

* Thu Jan 31 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-3
- tweak FHS patch, update spec after packaging review

* Wed Jan 30 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-2
- add patch to be standard FHS compliant, remove phantomjs
- update to v5.4.3 upstream community sources

* Wed Jan 09 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.2-1
- update to v5.4.2 upstream community sources

* Thu Oct 18 2018 Mark Goodwin <mgoodwin@redhat.com> 5.3.1-1
- update to v5.3.1 upstream community sources

* Tue Oct 02 2018 Mark Goodwin <mgoodwin@redhat.com> 5.2.5-1
- native RPM spec build with current tagged v5.2.5 sources
