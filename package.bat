pyinstaller -D --paths venv/Lib/site-packages --icon=./logo.ico --add-data=plugins/*.json;plugins --add-data=./config.json;./ --add-data=venv/Lib/site-packages/ntwork/wc/helper_4.0.8.6027.dat;internal/ntwork/wc --hidden-import=contourpy app.py;
pause;