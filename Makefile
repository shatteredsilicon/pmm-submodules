all: client server

submodules:
	git submodule update --init --remote

server: submodules
	./build/bin/build-server

rpmbuild-docker: submodules
	./build/bin/build-rpmbuild-docker

clean:
	rm -rf tmp results
