VENV           = venv
VENV_PYTHON    = $(VENV)/bin/python
SYSTEM_PYTHON  = $(or $(shell which python3), $(shell which python))
# If virtualenv exists, use it. If not, find python using PATH
PYTHON         = $(or $(wildcard $(VENV_PYTHON)), $(SYSTEM_PYTHON))

db: HPCs.db
.SILENT: HPCs.db
HPCs.db: 
	echo "Constructing 'HPCs.db'"
	echo

	$(PYTHON) db.py sql/constructing/create_tables.sql
	$(PYTHON) scraping/top500.py ./scraping/

	$(PYTHON) db.py sql/constructing/node_details.sql
	$(PYTHON) db.py sql/constructing/update_total_nodes.sql
	echo
	echo "Inserted node details"

.SILENT: rebuild_db
.PHONY: rebuild_db
rebuild_db: 
	rm HPCs.db
	make HPCs.db