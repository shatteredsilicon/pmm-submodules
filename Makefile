all: server

submodules:
	git submodule update --init --remote --force
	git submodule foreach --recursive 'git clean -f -d'
	git submodule foreach --recursive 'git fetch origin --tags -f'

srpms: submodules
	./build/bin/build-srpms $(packages)

rpms: submodules srpms
	./build/bin/build-rpms $(packages)

server: submodules rpms
	./build/bin/build-server

rpmbuild-docker: submodules
	./build/bin/build-rpmbuild-docker

show-vulnerabilities:
	./build/bin/show-vulnerabilities

clean:
	rm -rf tmp results
