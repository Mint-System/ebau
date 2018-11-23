SHELL:=/bin/sh

# http://clarkgrubb.com/makefile-style-guide#phony-targets

.DEFAULT_GOAL := help

GIT_USER=$(shell git config user.email)

.PHONY: help
help: ## Show the help messages
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -k 1,1 | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: js
js:
	npm run build --prefix ./php/public


.PHONY: js-watch
js-watch:
	npm run watch --prefix ./kt_uri/configuration/public


.PHONY: css
css: ## Create the css files from the sass files
	@cd camac/configuration/public/css/; make css


.PHONY: css-watch
css-watch: ## Watch the sass files and create the css when they change
	@cd camac/configuration/public/css/; make watch


.PHONY: install-api-doc
install-api-doc: ## installs the api doc generator tool
	npm i -g apidoc


.PHONY: generate-api-doc
generate-api-doc: ## generates documentation for the i-web portal API
	apidoc -i kt_uri/configuration/Custom/modules/portal/controllers/ -o doc/
	@echo "Documentation was saved in /doc folder."


.PHONY: clear-cache ## Clear the memcache
clear-cache:
	@docker-compose exec php php -d xdebug.remote_enable=off /var/www/camac/cronjob/clear-cache.php

.PHONY: dumpconfig ## Dump the configuration tables
dumpconfig:
	@docker-compose exec django python manage.py dumpconfig


.PHONY: dumpdata ## Dump the data tables
dumpdata:
	docker-compose exec django /app/manage.py dumpcamacdata

.PHONY: loadconfig ## Load config.json
loadconfig:
	@docker-compose exec django python manage.py loadconfig

.PHONY: dbshell ## Start a psql shell
dbshell:
	@docker-compose exec db psql -Ucamac


######### Changes from eBau Bern #########

.PHONY: mergeconfig
mergeconfig: ## Merge config.json
	git mergetool --tool=jsondiff
	make sequencenamespace

.PHONY: migrate
migrate:  ## Migrate schema
	docker-compose exec django /app/manage.py migrate
	make sequencenamespace

.PHONY: grunt-build
grunt-build: ## Grunt build
	docker-compose exec web sh -c "cd configuration/public && npm run build"

.PHONY: grunt-watch
grunt-watch: ## Grunt watch
	docker-compose exec web sh -c "cd configuration/public && npm run build && npm run watch"

.PHONY: makemigrations
makemigrations: ## Create schema migrations
	docker-compose exec django /app/manage.py makemigrations

.PHONY: flush
flush:	## Flush database
	@docker-compose exec django /app/manage.py flush

# Directory for DB snapshots
.PHONY: _db_snapshots_dir
_db_snapshots_dir:
	@mkdir -p db_snapshots

.PHONY: db_snapshot
db_snapshot: _db_snapshots_dir  ## Make a snapshot of the current state of the database
	@docker-compose exec db  pg_dump -Ucamac -c > db_snapshots/$(shell date -Iseconds).sql

.PHONY: db_restore
db_restore:  ## Restore latest DB snapshot created with `make db_snapshot`
	@mkdir -p db_snapshots
	@echo "restoring from $(SNAPSHOT)"
	@docker-compose exec -T db psql -Ucamac < $(SNAPSHOT) > /dev/null

.PHONY: sequencenamespace
sequencenamespace:  ## Set the Sequence namespace for a given user. GIT_USER is detected from your git repository.
	@docker-compose exec django make sequencenamespace GIT_USER=$(GIT_USER)

.PHONY: log
log: ## Show logs of web container
	@docker-compose logs --follow php

.PHONY: clearcache
clearcache: ## Clear cache
	@docker-compose exec php php /var/www/camac/cronjob/clear-cache.php

.PHONY: install
install: composer-install npm-install bower-install ## Run install commands

.PHONY: test
test: ## Run backend tests
	@docker-compose exec django make test

.PHONY: composer-install
composer-install: ## Install php dependencies
	docker-compose exec web composer install -d /var/www/camac
	docker-compose exec web composer install -d /var/www/configuration

.PHONY: npm-install
npm-install: ## Install js dependencies
	docker-compose exec web npm install --prefix /var/www/configuration/public

.PHONY: bower-install
bower-install: ## Install frontend dependencies
	docker-compose exec web bash -c "cd /var/www/configuration/public && bower install --allow-root"

.PHONY: dev
dev: loadconfig install grunt-watch ## Loads config, installs dependencies and continuously rebuilds CSS/JS when files change
