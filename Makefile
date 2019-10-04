PROJECT=btracker
SUBPROJECT=$(PROJECT)-service
VERSION?=commit_$(shell git rev-parse --short HEAD)

export VERSION

build-only:
	docker-compose -f docker-compose.yml build

build: build-only tag

%-tag:
	docker tag $*:$(VERSION) $*:latest
	docker tag $*:$(VERSION) jvaltersson/btracker/$*:$(VERSION)
	docker tag $*:$(VERSION) jvaltersson/btracker/$*:latest

tag: $(SUBPROJECTS:%=%-tag)

%-push:
	docker push $*:$(VERSION) jvaltersson/btracker/$*:$(VERSION)
	docker push $*:$(VERSION) jvaltersson/btracker/$*:latest

push-deploy: $(SUBPROJECTS:%=%-push)
