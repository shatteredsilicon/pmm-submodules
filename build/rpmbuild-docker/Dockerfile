FROM almalinux:8.7-minimal

RUN microdnf -y update && \
    microdnf -y install yum
RUN yum -y install epel-release
RUN dnf module enable -y nodejs:18
RUN yum -y --allowerasing install nodejs yum-utils rpmdevtools createrepo_c mock git golang \
        jq python2 make gcc-c++ rsync rkhunter coreutils

RUN npm install -g npm@latest

RUN useradd builder -u 1000 -m -G users,wheel,mock && \
    chmod 755 /home/builder
RUN (rkhunter --update || true) && rkhunter --propupd

#RUN curl --silent --location --output /etc/yum.repos.d/yarn.repo https://dl.yarnpkg.com/rpm/yarn.repo
#RUN yum -y install yarn

RUN \
	corepack enable &&\
	corepack prepare yarn@stable --activate

COPY ssm-8.tpl /etc/mock/templates/ssm-8.tpl

COPY ssm-8.cfg /etc/mock/ssm-8-.cfg

RUN \
	ARCH="$(rpm --eval "%{_arch}")" &&\
	sed "s/_ARCH_/${ARCH}/g" /etc/mock/ssm-8-.cfg > "/etc/mock/ssm-8-${ARCH}.cfg" &&\
	rm /etc/mock/ssm-8-.cfg

ENV GOPATH=/home/builder/go
RUN mkdir -p ${GOPATH}/src/github.com/golang
ADD dep ${GOPATH}/src/github.com/golang/dep
RUN GO111MODULE=off go install -ldflags="-X main.version=v0.5.4" ${GOPATH}/src/github.com/golang/dep/cmd/dep
RUN go install github.com/sonatype-nexus-community/nancy@latest
RUN chown -R builder:builder /home/builder

RUN rkhunter --propupd uname && rkhunter --check --disable system_configs_syslog --disable avail_modules --disable passwd_changes --disable group_changes

#Configure build time caches
ENV npm_config_cache=/mnt/cache/npm
ENV GOCACHE=/mnt/cache/go
ENV DEPCACHEDIR=/mnt/cache/dep
ENV NANCY_CACHE=/mnt/cache/nancy
ENV YARN_CACHE_FOLDER=/mnt/cache/yarn

RUN mkdir -p "${npm_config_cache}"
RUN mkdir -p "${GOCACHE}"
RUN mkdir -p "${DEPCACHEDIR}"
RUN mkdir -p "${NANCY_CACHE}"
RUN mkdir -p "${YARN_CACHE_FOLDER}"
RUN chown -R builder:builder /mnt/cache

RUN mkdir -p /mnt/tmp/mock && chown -R builder:builder /mnt/tmp/mock

VOLUME /mnt/cache
VOLUME /mnt/tmp

#USER builder

COPY entrypoint /usr/local/sbin/entrypoint
RUN chmod 744 /usr/local/sbin/entrypoint
ENTRYPOINT ["/usr/local/sbin/entrypoint"]

ENV FLAVOR=rpmbuild OS=rockylinux DIST=el8 PATH=$PATH:${GOPATH}/bin
WORKDIR /home/builder
