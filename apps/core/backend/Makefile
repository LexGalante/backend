.PHONY:
    help run test lint

help:
    @echo "make run"
    @echo "     running application"
    @echo "make test"
    @echo "     execute pytest"
    @echo "make lint"
    @echo "     execute flake8"

run:
    uvicorn src.main:app --reload

test:
    pytest

lint:
    flake8



