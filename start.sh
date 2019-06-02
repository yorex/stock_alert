export FLASK_APP=controller.py
export FLASK_ENV=development

nohup flask run --host=0.0.0.0 --port=5000 &
