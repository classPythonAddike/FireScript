build:
	@echo "Building Parser"
	@python -m nuitka --standalone --onefile --warn-unusual-code --linux-onefile-icon=firescript.png --static-libpython=no --remove-output -o bin/firescript bin/firescript.py
