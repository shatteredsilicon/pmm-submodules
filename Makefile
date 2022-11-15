all: server

submodules:
	git submodule update --init --force
	git submodule foreach --recursive 'git clean -f -d'
	git submodule foreach --recursive 'git fetch origin --tags -f'

srpms: submodules
	./build/bin/build-srpms $(packages)

rpms: submodules
	./build/bin/build-rpms $(packages)

debs: submodules
	./build/bin/build-debs $(packages)

sdebs: submodules
	./build/bin/build-sdebs $(packages)

server: submodules
	./build/bin/build-server

rpmbuild-docker: submodules
	./build/bin/build-rpmbuild-docker

show-vulnerabilities:
	./build/bin/show-vulnerabilities

clean:
	rm -rf tmp results
