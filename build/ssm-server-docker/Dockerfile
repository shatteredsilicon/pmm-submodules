FROM rockylinux:9.3-minimal AS builder

EXPOSE 80 443

WORKDIR /opt

# exclude MariaDB in appstream repo
RUN sed -i "/\[appstream\]/a exclude=mariadb*,galera*,boost-program-options" /etc/yum.repos.d/rocky.repo

RUN microdnf -y update && \
    microdnf -y install epel-release && \
    microdnf -y install --nodocs --noplugins --best shadow-utils rkhunter && \
    microdnf -y clean all

RUN useradd -s /bin/false ssm
RUN (rkhunter --update || true) && rkhunter --propupd

ARG ssm_version=ssm_version
ENV SSM_VERSION=$ssm_version

COPY RPMS /tmp/RPMS
COPY playbook-install.yml /opt/playbook-install.yml
COPY playbook-init.yml /opt/playbook-init.yml

RUN microdnf -y install --nodocs --noplugins --best ansible-core sqlite && \
    ansible-galaxy collection install community.general community.mysql && \
    ansible-playbook -vvv -i 'localhost,' -c local /opt/playbook-install.yml && \
    ansible-playbook -vvv -i 'localhost,' -c local /opt/playbook-init.yml && \
    microdnf -y remove ansible-core && microdnf -y clean all

RUN cp /usr/share/ssm-server/entrypoint.sh /opt/entrypoint.sh
RUN find / -type f ! -path "/proc/*" ! -path "/dev/*" ! -path "/sys/*" ! -path "/var/lib/mysql/*" ! -path "/var/lib/rkhunter/*" ! -path "/var/lib/grafana/*" ! -path "/var/log/*" ! -path "/root/*" ! -path "/home/*" ! -path "/tmp/*" ! -path "/opt/prometheus/*" ! -path "/run/*.pid" ! -path "/usr/lib/fontconfig/cache/*" ! -path "/var/lib/dnf/*" ! -path "/var/lib/rpm/*" ! -path "/var/spool/mail/*" ! -path "/usr/share/mime/*" | xargs -n1 -I {} sh -c "rpm -qf '{}' | grep -oP '(?<=file ).*(?= is not owned by any package)' >> /var/log/ssm-server-orphan-files.log || true"
RUN rpm -qa | xargs -n1 -I {} sh -c "rpm --verify '{}' >> /var/log/ssm-server-rpm-verify.log || true"
RUN rkhunter --propupd uname && (rkhunter --check --novl --rwo --noappend-log --ns --disable system_configs_syslog --disable avail_modules --disable passwd_changes --disable group_changes > /var/log/ssm-server-rkhunter.log || true)

FROM scratch

COPY --from=builder / /

CMD ["/opt/entrypoint.sh"]