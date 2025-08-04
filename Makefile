.PHONY: backend/integration
backend/integration:
	cd backend; \
	source venv/bin/activate; \
	python -m pytest inttests/

.PHONY: backend/unittests
backend/unittests:
	cd backend; \
	source venv/bin/activate; \
	python -m unittest test.DA.test_bindist; \
	python -m unittest test.DA.test_kcalc; \
	python -m unittest test.DA.test_psat_calc; \
	python -m unittest test.DC.test_antoine_data_scraper; \
	python -m unittest test.DC.test_tbl_antoine;
