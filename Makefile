build:
	@echo "Building Compiler"
	@python -m nuitka --standalone --onefile --warn-unusual-code --linux-onefile-icon=firescript.png --static-libpython=no --remove-output -o bin/firescript bin/firescript.py
	@echo "Building Interpreter"
	@cd interpreter && go build -o fscrun .
	@mv interpreter/fscrun bin/fscrun

test:
	@echo "Testing Compiler"
	@pytest --cov=compiler --cov-fail-under=85 --no-cov-on-fail compiler/tests/
	@printf "\n\n\n"
