# Prepare variables
ifeq ($(TMP),)
TMP = $(CURDIR)/tmp
endif

ifeq ($(VERSION),)
VERSION := $(shell git describe | sed -e "s/-\([0-9]*\).*/.post\1/")
endif

PACKAGE = daemonizer-$(VERSION)
ifndef USERNAME
    USERNAME = echo $$USER
endif
FILES = LICENSE* *.rst *.toml tox* setup.* \
		Makefile daemonizer.spec conftest.py \
		docs src test


# Define special targets
all: packages

# Temporary directory, include .fmf to prevent exploring tests there
tmp:
	mkdir -p $(TMP)/.fmf

# Build documentation, prepare man page ??

# RPM packaging
spec:
	sed -e s"|VER_GOES_HERE|$(VERSION)|" packaging/el9/daemonizer.spec > daemonizer.spec
source: spec
	mkdir -p $(TMP)/SOURCES
	mkdir -p $(TMP)/$(PACKAGE)
	cp -a $(FILES) $(TMP)/$(PACKAGE)
tarball: source
	cd $(TMP) && tar czf SOURCES/$(PACKAGE).tar.gz $(PACKAGE)
	@echo ./tmp/SOURCES/$(PACKAGE).tar.gz
version:
	@echo "$(VERSION)"
rpm: tarball
	rpmbuild --define '_topdir $(TMP)' -bb daemonizer.spec
srpm: tarball
	rpmbuild --define '_topdir $(TMP)' -bs daemonizer.spec
packages: rpm srpm

clean:
	rm -f daemonizer.spec
	rm -rf $(TMP)
	rm -rf .cache .pytest_cache
