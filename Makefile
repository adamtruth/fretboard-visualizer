MAKEFILE_DIR := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))

.PHONY: help
help: ## Show this help message
	@echo "Makefile commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'


.PHONY: run
run: ## Execute the program
	@uv run python3 -m main

.PHONY: gui
gui: ## Execute the program
	@uv run python3 -m gui

.PHONY: pic
pic: ## Execute the program
	@uv run python3 -m pic

.PHONY: example
example: ## Execute the program
	@uv run python3 -m example_gui
