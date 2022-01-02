build:
	@echo "Building Parser"
	@python -m nuitka --standalone --onefile --warn-unusual-code --linux-onefile-icon=firescript.png --static-libpython=no --remove-output -o bin/firescript bin/firescript.py

test:
	@echo "Testing Parser"
	@pytest --cov=parser --cov-fail-under=85 --no-cov-on-fail parser/tests/
	@printf "\n\n\n"
