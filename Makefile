# These can be overidden with env vars.
CLUSTER ?= nyu-devops

.SILENT:

.PHONY: help
help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: all
all: help

##@ Development

.PHONY: clean
clean:	## Removes all dangling docker images
	$(info Removing all dangling docker images..)
	docker image prune -f

.PHONY: venv
venv: ## Create a Python virtual environment
	$(info Creating Python 3 virtual environment...)
	poetry config virtualenvs.in-project true
	poetry shell

.PHONY: install
install: ## Install dependencies
	$(info Installing dependencies...)
	sudo poetry config virtualenvs.create false
	sudo poetry install

.PHONY: lint
lint: ## Run the linter
	$(info Running linting...)
	flake8 service tests --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 service tests --count --max-complexity=10 --max-line-length=127 --statistics
	pylint service tests --max-line-length=127

.PHONY: tests
test: ## Run the unit tests
	$(info Running tests...)
	pytest --pspec --cov=service --cov-fail-under=95

##@ Runtime

.PHONY: run
run: ## Run the service
	$(info Starting service...)
	honcho start

.PHONY: cluster
cluster: ## Create a K3D Kubernetes cluster with load balancer and registry
	$(info Creating Kubernetes cluster with a registry and 1 node...)
	k3d cluster create --agents 1 --registry-create cluster-registry:0.0.0.0:32000 --port '8080:80@loadbalancer'
	make build-docker
	make setup-cluster

.PHONY: cluster-rm
cluster-rm: ## Remove a K3D Kubernetes cluster
	$(info Removing Kubernetes cluster...)
	k3d cluster delete

.PHONY: deploy
deploy: ## Deploy the service on local Kubernetes
	$(info Deploying service locally...)
	kubectl apply -f k8s/pv.yaml
	kubectl apply -f k8s/postgresql.yaml
	kubectl apply -f k8s/deployment.yaml
	kubectl apply -f k8s/service.yaml
	kubectl apply -f k8s/ingress.yaml

.PHONY: build-docker
build-docker: ## Build the docker image and push it to the registry
	$(info Building the docker image and pushing it to the registry...)
	docker build -t recommendations:latest .
	sudo bash -c "echo '127.0.0.1    cluster-registry' >> /etc/hosts"
	docker tag recommendations:latest cluster-registry:32000/recommendations:latest
	docker push cluster-registry:32000/recommendations:latest

.PHONY: setup-cluster
setup-cluster: ## Setup the cluster and deploy the service
	$(info Creating the namespace for the resource...)
	kubectl create namespace recommendations-dev
	kubectl get ns
	kubectl config set-context --current --namespace recommendations-dev
	alias kns='kubectl config set-context --current --namespace'

.PHONY: deploy
depoy: ## Deploy the service on local Kubernetes
	$(info Deploying service locally...)
	kubectl apply -f k8s/
