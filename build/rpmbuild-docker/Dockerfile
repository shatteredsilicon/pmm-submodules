FROM rockylinux:8

RUN yum -y install epel-release nodejs
RUN curl --silent --location https://dl.yarnpkg.com/rpm/yarn.repo | tee /etc/yum.repos.d/yarn.repo
RUN yum -y install yum-utils rpmdevtools createrepo_c mock git golang yarn

RUN echo $' \n\
config_opts[\'dnf.conf\'] += """ \n\
[ssm] \n\
name=SSM \n\
baseurl=https://dl.shatteredsilicon.net/$releasever/ssm/RPMS/$basearch/ \n\
gpgcheck=1 \n\
enabled=1 \n\
gpgkey=https://dl.shatteredsilicon.net/$releasever/ssm/RPM-GPG-KEY-SSM-EL8 \n\
 \n\
[ssm-source] \n\
name=SSM Source RPMs \n\
baseurl=https://dl.shatteredsilicon.net/$releasever/ssm/SRPMS \n\
gpgcheck=1 \n\
enabled=0 \n\
gpgkey=https://dl.shatteredsilicon.net/$releasever/ssm/RPM-GPG-KEY-SSM-EL8 \n\
 \n\
[ssm-debug] \n\
name=SSM \n\
baseurl=https://dl.shatteredsilicon.net/$releasever/ssm/debug/$basearch/ \n\
gpgcheck=1 \n\
enabled=0 \n\
gpgkey=https://dl.shatteredsilicon.net/$releasever/ssm/RPM-GPG-KEY-SSM-EL8 \n\
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
config_opts[\'legal_host_arches\'] = (\''$(rpm --eval "%{_arch}")$'\',) \n\
' > /etc/mock/ssm-8-$(rpm --eval "%{_arch}").cfg

RUN useradd builder -u 1000 -m -G users,wheel,mock && \
    chmod 755 /home/builder && \
    chown -R builder:builder /home/builder
USER builder

ENV GOPATH=/home/builder/go
RUN mkdir -p ${GOPATH}/src/github.com/golang
ADD dep ${GOPATH}/src/github.com/golang/dep
RUN GO111MODULE=off go install -ldflags="-X main.version=v0.5.4" ${GOPATH}/src/github.com/golang/dep/cmd/dep
ENV PATH=$PATH:${GOPATH}/bin

ENV FLAVOR=rpmbuild OS=rockylinux DIST=el8
WORKDIR /home/builder
