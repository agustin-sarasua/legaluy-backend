APP_NAME = legaluy-backend
APP_VERSION = 0.0.6

AWS_ECR_ACCOUNT_ID = 695251250319
AWS_ECR_REGION = us-east-1
AWS_ECR_REPO = my-ecr-repo

PYTHON_VERSION = 3.11

TAG ?= $(APP_VERSION)

.PHONY: docker/build docker/push docker/run docker/test

# Set the name of the virtual environment
VENV_NAME = .venv

# Setup Targets
venv:
	python$(PYTHON_VERSION) -m venv $(VENV_NAME)

# Install packages from requirements.txt
install:
	. $(VENV_NAME)/bin/activate && pip install -r requirements.txt

# Target to setup the virtual environment
setup: venv install	

.PHONY: run
run:
	python app/main.py

docker/build:
	docker build -t $(APP_NAME):$(APP_VERSION) .

docker/push: docker/build
	aws ecr get-login-password --region $(AWS_ECR_REGION) | docker login --username AWS --password-stdin $(AWS_ECR_ACCOUNT_ID).dkr.ecr.$(AWS_ECR_REGION).amazonaws.com
	docker tag $(APP_NAME):$(APP_VERSION) $(AWS_ECR_ACCOUNT_ID).dkr.ecr.$(AWS_ECR_REGION).amazonaws.com/$(AWS_ECR_REPO):$(TAG)
	docker push $(AWS_ECR_ACCOUNT_ID).dkr.ecr.$(AWS_ECR_REGION).amazonaws.com/$(AWS_ECR_REPO):$(TAG)

docker/run:
	docker run -p 9000:80 $(APP_NAME):$(APP_VERSION)
# 	docker run -p 80:80 695251250319.dkr.ecr.us-east-1.amazonaws.com/my-ecr-repo:0.0.2
