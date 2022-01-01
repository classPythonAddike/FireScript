build:
	@python -m nuitka --standalone --onefile --warn-unusual-code --linux-onefile-icon=$$HOME/AllFolders/wallpapers/wild.png --static-libpython=no --remove-output -o bin/fs-build bin/parse.py
