# ssm-submodules

## Requirements

- ```git``` shipped with RHEL 8
- ```rpmbuild``` shipped with RHEL 8
- ```spectool``` shipped with RHEL 8
- [mock](https://github.com/rpm-software-management/mock)
- ```golang v1.17``` shipped with RHEL 8
- [dep](https://github.com/golang/dep)
- ```nodejs v14``` shipped with RHEL 8
- [yarn](https://yarnpkg.com/)
- [Nancy](https://github.com/sonatype-nexus-community/nancy) (for checking vulnerabilities of Golang packages)
- [jq](https://stedolan.github.io/jq/) (for parsing vulnerabilities)

## Setup

### setup mock

- Create file `/etc/mock/templates/ssm-8.tpl` and put following content into this file.

```shell
config_opts['dnf.conf'] += """

[ssm]
name=SSM
baseurl=https://dl.shatteredsilicon.net/$releasever/ssm/RPMS/$basearch/
gpgcheck=1
enabled=1
gpgkey=https://dl.shatteredsilicon.net/$releasever/ssm/RPM-GPG-KEY-SSM-EL8

[ssm-source]
name=SSM Source RPMs
baseurl=https://dl.shatteredsilicon.net/$releasever/ssm/SRPMS
gpgcheck=1
enabled=0
gpgkey=https://dl.shatteredsilicon.net/$releasever/ssm/RPM-GPG-KEY-SSM-EL8

[ssm-debug]
name=SSM
baseurl=https://dl.shatteredsilicon.net/$releasever/ssm/debug/$basearch/
gpgcheck=1
enabled=0
gpgkey=https://dl.shatteredsilicon.net/$releasever/ssm/RPM-GPG-KEY-SSM-EL8

"""
```

- Use command ```uname -m``` to show your host architecture, for example
```console
sh-4.4# uname -m
aarch64
```

- Create file `/etc/mock/ssm-8-[your host architecture].cfg` and put following content into this file, replace all ```aarch64``` below with you host architecture first.

```shell
include('templates/rocky-8.tpl')
include('templates/epel-8.tpl')
include('templates/ssm-8.tpl')

config_opts['root'] = 'ssm-8-aarch64'
config_opts['description'] = 'SSM 8'
config_opts['target_arch'] = 'aarch64'
config_opts['legal_host_arches'] = ['aarch64']
config_opts['module_enable'] = ['nodejs:14']
```

## Build

### rpmbuild docker image

Run following command to build rpmbuild docker image.

```bash
make rpmbuild-docker
```

An docker image called `shatteredsilicon/rpmbuild` will be created once this command succeed.

### SRPMS

Run following command to generate srpms, and go to folder `result/SRPMS` to look for generated .src.rpm packages.

```bash
make srpms [package list]
```

e.g.

```bash
# This will create .src.rpm for all packages
make srpms

# This will create .src.rpm for package 'ssm-client', 'ssm-managed' and 'grfana'
make srpms packages="ssm-client ssm-managed grafana"

# This will create .src.rpm for package 'ssm-client' only
make srpms packages="ssm-client"
```

> **note**: if you do not want to generate vulnerability logs, you can add `ENV_DEV=1` before the command to skip it

### RPMS

Run following command to generate rpms by mock, and go to folder `result/RPMS` to look for generated .rpm packages.

```bash
make rpms [package list]
```

e.g.

```bash
# This will create .rpm for all packages
make rpms

# This will create .rpm for package 'ssm-client', 'ssm-managed' and 'grfana'
make rpms packages="ssm-client ssm-managed grafana"

# This will create .rpm for package 'ssm-client' only
make rpms packages="ssm-client"
```

This command will also generate .src.rpm in `results/SRPMS`.

> **note**: if you do not want to generate vulnerability logs, you can add `ENV_DEV=1` before the command to skip it

### SSM server docker image

Run following command to build SSM server docker image. 

```bash
make server
```

An docker image called `shatteredsilicon/ssm-server-fb` will be created once this command succeed. The `tag` of this docker image is defined in file `VERSION` in the root of this project.

This command will also generate .src.rpm in `results/SRPMS` and .rpm in `results/RPMS`.

> **note**: if you do not want to generate vulnerability logs, you can add `ENV_DEV=1` before the command to skip it

### Clean

Run following command to clean generated files and temporary files.

```bash
make clean
```

### Show latest vulnerabilities

After you run ```make srpms```/```make rpms```/```make server```, it will also create files indicate those latest vulnerabilities that are found, they are placed under folder ```logs/vulnerability-diffs/```, in ```JSON``` format. You can use command ```make show-vulnerabilities``` to display them. For example

```console
sh-4.4# make show-vulnerabilities
./build/bin/show-vulnerabilities
---------------------------------------mongodb_exporter---------------------------------------
[
 	{
		"id": "CVE-2022-21698",
		"path": "pkg:golang/github.com/prometheus/client_golang@v1.1.0",
		"title": "[CVE-2022-21698] CWE-400: Uncontrolled Resource Consumption ('Resource Exhaustion')",
		"desc": "client_golang is the instrumentation library for Go applications in Prometheus, and the promhttp package in client_golang provides tooling around HTTP servers and clients. In client_golang prior to version 1.11.1, HTTP server is susceptible to a Denial of Service through unbounded cardinality, and potential memory exhaustion, when handling requests with non-standard HTTP methods. In order to be affected, an instrumented software must use any of `promhttp.InstrumentHandler*` middleware except `RequestsInFlight`; not filter any specific methods (e.g GET) before middleware; pass metric with `method` label name to our middleware; and not have any firewall/LB/proxy that filters away requests with unknown `method`. client_golang version 1.11.1 contains a patch for this issue. Several workarounds are available, including removing the `method` label name from counter/gauge used in the InstrumentHandler; turning off affected promhttp handlers; adding custom middleware before promhttp handler that will sanitize the request method given by Go http.Request; and using a reverse proxy or web application firewall, configured to only allow a limited set of methods.",
		"cvss_score": "7.5",
		"ref": "https://ossindex.sonatype.org/vulnerability/CVE-2022-21698?component-type=golang&component-name=github.com%2Fprometheus%2Fclient_golang&utm_source=nancy-client&utm_medium=integration&utm_content=1.0.37"
	}
]


---------------------------------------mysqld_exporter---------------------------------------
[
 	{
		"id": "CVE-2022-21698",
		"path": "pkg:golang/github.com/prometheus/client_golang@v1.1.0",
		"title": "[CVE-2022-21698] CWE-400: Uncontrolled Resource Consumption ('Resource Exhaustion')",
		"desc": "client_golang is the instrumentation library for Go applications in Prometheus, and the promhttp package in client_golang provides tooling around HTTP servers and clients. In client_golang prior to version 1.11.1, HTTP server is susceptible to a Denial of Service through unbounded cardinality, and potential memory exhaustion, when handling requests with non-standard HTTP methods. In order to be affected, an instrumented software must use any of `promhttp.InstrumentHandler*` middleware except `RequestsInFlight`; not filter any specific methods (e.g GET) before middleware; pass metric with `method` label name to our middleware; and not have any firewall/LB/proxy that filters away requests with unknown `method`. client_golang version 1.11.1 contains a patch for this issue. Several workarounds are available, including removing the `method` label name from counter/gauge used in the InstrumentHandler; turning off affected promhttp handlers; adding custom middleware before promhttp handler that will sanitize the request method given by Go http.Request; and using a reverse proxy or web application firewall, configured to only allow a limited set of methods.",
		"cvss_score": "7.5",
		"ref": "https://ossindex.sonatype.org/vulnerability/CVE-2022-21698?component-type=golang&component-name=github.com%2Fprometheus%2Fclient_golang&utm_source=nancy-client&utm_medium=integration&utm_content=1.0.37"
	}
]


sh-4.4# 
```

## How does the building work

First of all, all commands start with ```make``` are defined in ```Makefile```, and the main building commands are ```make srpms```, ```make rpms```. They are chained in this way ```make rpms -> make srpms```, just like how it defined in ```Makefile```:

```
srpms: submodules
	./build/bin/build-srpms $(packages)

rpms: submodules srpms
	./build/bin/build-rpms $(packages)
```

### Process of ```make srpms```

1. ##### Pulling the latest commit/tag of git submodules

    Submodules are placed under `sources/`, each submodule points to an git repo, and the branches of those submodules are defined in file `.gitmodules`. There are also some `non-git` directories under `sources/`, it will just leave them.

    After this, it will walk through all packages defined in variable `packages` in file `build/bin/vars` and process below steps for each package.

2. ##### Determining which version to use in `.spec` file

    Each directory under `sources/` has a `.spec` file in it (except for subpackages of `ssm-client`, `qan-agent`, `mysqld_exporter` etc), it will go to the correct subdirectory under `sources/` and check if current directory is a `git` directory.

    If current directory is a `git` directory, it uses this command

    ```bash
    git tag -l --sort=-version:refname "v*" --merged | head -n 1
    ```

    to get the latest `tag` on current branch and use this `tag` as the version in `.spec` file.

    If current directory isn't a `git` directory, then it means the version is already defined in `.spec` file.

    Finally it copies the `.spec` file to folder `tmp/rpmbuild/SPECS`.

    PS: After the version is determined, it also check if a `%{name}-%{version}-%{release}.src.rpm` file exists in `results/SRPMS`, if it exists it will stop processing below steps.

3. ##### Downloading 3rd-party sources defined in `.spec` with `spectool`

    Some 3rd-party package sources need to be downloaded, it will run this command
    
    ```bash
    spectool -C ${tmp_dir}/rpmbuild/SOURCES/ -g ${tmp_dir}/rpmbuild/SPECS/${package}.spec
    ```

    to pull those sources into `tmp/rpmbuild/SOURCES`

4. ##### Pulling dependencies of package

    If it is a 3rd-party package, e.g. `grafana`, `percona-toolkit`, extract the source tarball downloaded by `spectool` first.

    If a `yarn.lock` file exists, then it runs `yarn` to pull node modules into `node_modules`.

    If a `Gopkg.lock` file exists, then it runs `GO111MODULE=off dep ensure` to pull dependencies into `vendor`.

    If a `go.sum` file exists, then it runs `GO111MODULE=on go mod vendor` to pull dependencies into `vendor`.

    If a `package-lock.json` file exists, then it runs `npm install` to pull node modules into `node_modules`.

    Note there is a special package `ssm-client` which includes many subpackages in it. When pulling dependencies for it, it will pull dependencies each subpackage in a loop.
    
    ##### 4.5 Check latest vulnerabilities

    The best time to check the vulnerabilities is now. It will check if it is a `node` project or a `golang` project.

    If it's a `node` project, it uses `yarn` to check the vulnerabilities. If it is a `golang` project, it uses `nancy` to check the vulnerabilities.
    
    Then it checks the old vulnerabilities with lock file first, and then renames the lock file to another name, generates a new lock file, and check the latest vulnerabilities. Then compares the lates vulnerabilities and the old vulnerabilities, write result into `logs/vulnerability-diffs/`.

    Finally restore the old lock file before it pulls the dependencies.

5. ##### Building tarball

    After the dependencies are pulled, it compress the directory into a `.tar.gz` tarball and copy it to `tmp/rpmbuild/SOURCES`.

    When building tarball for `ssm-client`, it builds tarball for each subpackage first, and then compress those tarballs into a big tarball.

6. ##### Building src.rpm

    After the `.spec` is ready, the `tarball` is ready, finally it runs
    
    ```bash
    rpmbuild -bs --define "debug_package %{nil}" --define "_topdir ${tmp_dir}/rpmbuild" ${tmp_dir}/rpmbuild/SPECS/${package}.spec
    ```

    to build the `src.rpm` and then copies it into `results/SRPMS/`.

### Process of ```make rpms```

1. ##### Runing the `make srpms` first

    To build `.rpm` packages, it requires the `.src.rpm` exists in `result/SRPMS/` first. So it should run `make srpms` to produce those `.src.rpm` packages.

    See [Process of 'make srpms'](#process-of-make-srpms)

2. ##### Building `.rpm` with `mock`

    After the `.src.rpm` is built, it runs

    ```bash
    mock -r ssm-8-$(rpm --eval "%{_arch}") --resultdir ${rpm_dir} --rebuild ${srpm_dir}/${package}-${version}*.src.rpm
    ```

    to build `.rpm` package and put it into `results/RPMS`.


# See also

- ##### [Fixed vulnerabilities](docs/fixed-vulnerabilities.md)
