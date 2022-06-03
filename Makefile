.PHONY: run

run:
	uvicorn app.main:app

run.debug:
	uvicorn app.main:app --reload