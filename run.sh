virtualenv .env
source .env/bin/activate
pip install colorama nuitka
python3 -m nuitka \
  --standalone \
  --onefile \
  --remove-output \
  --follow-imports \
  --lto=yes \
  --clang \
  --jobs=3 \
  --assume-yes-for-downloads \
  run.py

cp run.bin ~/bin/run
deactivate
