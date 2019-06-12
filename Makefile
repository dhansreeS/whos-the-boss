# run make app
app: load_data clean_data train_model evaluate_model create_table start_app

# load data to S3 or to local - configured to local
load_data: run.py config/config.yml src/load_data.py
	python3 run.py load

# clean data and load processed files to s3 or local - configured to local
clean_data: run.py config/config.yml src/clean_data.py
	python3 run.py process

# train model and load/save to s3 or local - configured to local
train_model: src/train_model.py config/config.yml run.py
	python3 run.py train

# evaluate model and load metrics to S3 or local - configured to local
evaluate_model: src/evaluate_model.py config/config.yml run.py
	python run.py evaluate

# create a database for user input - configured to sqlite local
create_table: config/config.yml run.py src/data_model.py
	python run.py createSqlite

# run app - configured to local (check flask_config.py to change)
start_app: app/app.py config/flask_config.py run.py
	python run.py app


