FROM rockylinux:9.2-minimal

RUN microdnf -y update && \
    microdnf -y install yum

RUN useradd builder -u 1000 -m

RUN \
	dnf install -y python3-pip git graphviz java wget &&\
	python3 -m pip install mkdocs

COPY plantuml /usr/local/bin/plantuml
COPY build /usr/local/bin/build

RUN \
	mkdir -p /opt/plantuml &&\
	wget -O /opt/plantuml/plantuml.jar https://downloads.sourceforge.net/project/plantuml/plantuml.jar &&\
	chmod +x /usr/local/bin/plantuml /usr/local/bin/build

VOLUME /home/builder/work

# Entrypoint runs as root to set up the system, then drops privs
USER root
COPY entrypoint /usr/local/sbin/entrypoint
RUN chmod 744 /usr/local/sbin/entrypoint
ENTRYPOINT ["/usr/local/sbin/entrypoint"]
CMD ["/usr/local/bin/build"]

WORKDIR /home/builder/work
