FROM debian:buster-slim

RUN \
	useradd builder -u 1000 -m -G users && \
	chmod 755 /home/builder

RUN \	
	echo 'deb http://deb.debian.org/debian bullseye-backports main' > /etc/apt/sources.list.d/bullseye-backports.list &&\
	apt update && apt install -y golang-1.17 && \
	rm /etc/apt/sources.list.d/bullseye-backports.list && \
	apt update && apt install -y git rsync build-essential devscripts

ENV GOPATH=/home/builder/go
RUN mkdir -p ${GOPATH}/src/github.com/golang
ADD dep ${GOPATH}/src/github.com/golang/dep

ENV GOROOT=/usr/lib/go-1.17
ENV PATH=/usr/lib/go-1.17/bin:${GOPATH}/bin:$PATH
RUN GO111MODULE=off go install -ldflags="-X main.version=v0.5.4" ${GOPATH}/src/github.com/golang/dep/cmd/dep
RUN chown -R builder:builder /home/builder

USER root
COPY entrypoint /usr/local/sbin/entrypoint
RUN chmod 744 /usr/local/sbin/entrypoint
ENTRYPOINT ["/usr/local/sbin/entrypoint"]
