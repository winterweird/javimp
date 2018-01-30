INSTALL_PATH = $(HOME)/.javimp
PATH_RESOURCE_FILE = $(HOME)/.profile

.PHONY: help install addpath

help:
	@echo "Use 'make install' to install this in $(INSTALL_PATH)"
	@echo "Use 'make addpath' to add $(INSTALL_PATH) to your path"
	@echo "    (path will be exported in $(PATH_RESOURCE_FILE))"

install:
	mkdir -p $(INSTALL_PATH)
	cp ./javimp.py ./java_classes.list $(INSTALL_PATH)
	mv $(INSTALL_PATH)/javimp.py $(INSTALL_PATH)/javimp
	chmod +x $(INSTALL_PATH)/javimp

addpath:
	echo 'PATH="$(INSTALL_PATH):$$PATH"' >> $(HOME)/.profile
