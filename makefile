INSTALL_PATH = $(HOME)/.javapytools
PATH_RESOURCE_FILE = $(HOME)/.profile
SCRIPT_NAME_ROOT = javimp
SCRIPT_NAME = $(SCRIPT_NAME_ROOT).py
ADDITIONAL_FILES = ./java_classes.list

.PHONY: help install addpath

help:
	@echo "Use 'make install' to install this in $(INSTALL_PATH)"
	@echo "Use 'make addpath' to add $(INSTALL_PATH) to your path"
	@echo "    (path will be exported in $(PATH_RESOURCE_FILE))"

install:
	mkdir -p $(INSTALL_PATH)
	cp ./$(SCRIPT_NAME_ROOT) $(ADDITIONAL_FILES) $(INSTALL_PATH)
	mv $(INSTALL_PATH)/$(SCRIPT_NAME) $(INSTALL_PATH)/$(SCRIPT_NAME_ROOT)
	chmod +x $(INSTALL_PATH)/$(SCRIPT_NAME_ROOT)

addpath:
	echo 'PATH="$(INSTALL_PATH):$$PATH"' >> $(PATH_RESOURCE_FILE)
