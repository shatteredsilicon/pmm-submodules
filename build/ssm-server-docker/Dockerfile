FROM rockylinux:8

EXPOSE 80 443

WORKDIR /opt

RUN useradd -s /bin/false ssm
RUN yum -y install epel-release && yum -y --allowerasing install ansible sqlite rpm glibc-common clamav clamav-update rkhunter coreutils

RUN (rkhunter --update || true) && rkhunter --propupd

COPY RPMS /tmp/RPMS
COPY playbook-install.yml /opt/playbook-install.yml
RUN ansible-playbook -vvv -i 'localhost,' -c local /opt/playbook-install.yml

COPY playbook-init.yml /opt/playbook-init.yml
RUN ansible-playbook -vvv -i 'localhost,' -c local /opt/playbook-init.yml
RUN cp /usr/share/ssm-server/entrypoint.sh /opt/entrypoint.sh
RUN touch /.ssm-docker

RUN freshclam && clamscan -i -r --exclude-dir="^/sys/" /
RUN rkhunter --propupd uname && rkhunter --check --disable system_configs_syslog --disable avail_modules --disable passwd_changes --disable group_changes

CMD ["/opt/entrypoint.sh"]
