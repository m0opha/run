virtualenv .env
source .env/bin/activate
pip install pyinstaller
pyinstaller --onefile -i NONE -n run main.py
cp dist/run ~/bin

