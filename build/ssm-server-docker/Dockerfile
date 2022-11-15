FROM rockylinux:8-minimal

EXPOSE 80 443

WORKDIR /opt

RUN microdnf -y update && \
    microdnf -y install epel-release && \
    microdnf -y install --nodocs --noplugins --best shadow-utils rkhunter && \
    microdnf -y clean all

RUN useradd -s /bin/false ssm
RUN (rkhunter --update || true) && rkhunter --propupd

COPY RPMS /tmp/RPMS
COPY playbook-install.yml /opt/playbook-install.yml
COPY playbook-init.yml /opt/playbook-init.yml

RUN microdnf -y install --nodocs --noplugins --best yum && \
    yum -y install ansible sqlite && \
    ansible-playbook -vvv -i 'localhost,' -c local /opt/playbook-install.yml && \
    ansible-playbook -vvv -i 'localhost,' -c local /opt/playbook-init.yml && \
    yum autoremove && yum -y clean all

RUN cp /usr/share/ssm-server/entrypoint.sh /opt/entrypoint.sh

RUN rkhunter --propupd uname && rkhunter --check --disable system_configs_syslog --disable avail_modules --disable passwd_changes --disable group_changes

CMD ["/opt/entrypoint.sh"]