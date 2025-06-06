virtualenv .env
source .env/bin/activate
pip install colorama nuitka
python3 -m nuitka \
  --standalone \
  --onefile \
   --output-dir=dist \
  --remove-output \
  --follow-imports \
  --lto=yes \
  --clang \
  --jobs=6 \
  --assume-yes-for-downloads \
  run.py

deactivate