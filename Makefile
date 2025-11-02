.PHONY: help 
help: ## Show this help message
	@echo "Makefile commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

.PHONY: build 
build: ## Build the virtual environment
	@uv sync

.PHONY: run
run: ## Execute the program
	@uv run python3 -m main
