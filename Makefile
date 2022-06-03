.Phony start

run:
	uvicorn app.main:app
run.debug:
	uvicorn app.main:app --reload