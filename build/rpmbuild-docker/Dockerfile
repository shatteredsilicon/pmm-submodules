FROM rockylinux:8-minimal

RUN microdnf -y update && \
    microdnf -y install yum
RUN yum -y install epel-release
RUN dnf module enable -y nodejs:14
RUN yum -y --allowerasing install nodejs yum-utils rpmdevtools createrepo_c mock git golang \
        jq python2 make gcc-c++ rsync rkhunter coreutils

RUN useradd builder -u 1000 -m -G users,wheel,mock && \
    chmod 755 /home/builder
RUN (rkhunter --update || true) && rkhunter --propupd

RUN curl --silent --location https://dl.yarnpkg.com/rpm/yarn.repo | tee /etc/yum.repos.d/yarn.repo
RUN yum -y install yarn

RUN echo $' \n\
config_opts[\'dnf.conf\'] += """ \n\
[phantomjs] \n\
name = Repo for phantomjs \n\
baseurl = https://ftp.redsleeve.org/pub/misc/phantomjs/$basearch/ \n\
gpgcheck = 0 \n\
enabled = 1 \n\
""" \n\
' > /etc/mock/templates/ssm-8.tpl

RUN echo $' \n\
include(\'templates/rocky-8.tpl\') \n\
include(\'templates/epel-8.tpl\') \n\
include(\'templates/ssm-8.tpl\') \n\
\n\
config_opts[\'root\'] = \'ssm-8-'$(rpm --eval "%{_arch}")$'\' \n\
config_opts[\'description\'] = \'SSM 8\' \n\
config_opts[\'target_arch\'] = \''$(rpm --eval "%{_arch}")$'\' \n\
config_opts[\'legal_host_arches\'] = [\''$(rpm --eval "%{_arch}")$'\'] \n\
config_opts[\'module_enable\'] = [\'nodejs:14\'] \n\
' > /etc/mock/ssm-8-$(rpm --eval "%{_arch}").cfg

ENV GOPATH=/home/builder/go
RUN mkdir -p ${GOPATH}/src/github.com/golang
ADD dep ${GOPATH}/src/github.com/golang/dep
RUN GO111MODULE=off go install -ldflags="-X main.version=v0.5.4" ${GOPATH}/src/github.com/golang/dep/cmd/dep
RUN go install github.com/sonatype-nexus-community/nancy@latest
RUN chown -R builder:builder /home/builder

RUN rkhunter --propupd uname && rkhunter --check --disable system_configs_syslog --disable avail_modules --disable passwd_changes --disable group_changes

USER builder
ENV FLAVOR=rpmbuild OS=rockylinux DIST=el8 PATH=$PATH:${GOPATH}/bin
WORKDIR /home/builder
