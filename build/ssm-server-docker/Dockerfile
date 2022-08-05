FROM rockylinux:8

EXPOSE 80 443

WORKDIR /opt

RUN useradd -s /bin/false ssm
RUN yum -y install epel-release && yum -y install ansible sqlite

COPY RPMS /tmp/RPMS
COPY playbook-install.yml /opt/playbook-install.yml
RUN ansible-playbook -vvv -i 'localhost,' -c local /opt/playbook-install.yml

COPY playbook-init.yml /opt/playbook-init.yml
RUN ansible-playbook -vvv -i 'localhost,' -c local /opt/playbook-init.yml
RUN cp /usr/share/ssm-server/entrypoint.sh /opt/entrypoint.sh
RUN touch /.ssm-docker

CMD ["/opt/entrypoint.sh"]
