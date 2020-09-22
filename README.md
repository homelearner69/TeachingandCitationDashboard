# A Dashboard that monitors on academic staff in teachings and citations


The authentication of users was made through a sqlite3 database, using the `con` parameter with in the `config.txt` file.

The example comes with the a standard username `test` and password `test1` but you can add more users using the `add_remove_users.ipynb` jupyter notebook or the functions available in the `users_mgt.py`.

### Files description:
`add_remove_users.ipynb`: A jupyter notebook used to creating and removing users based on the functions created in users_mgt.py<br/>
`app.py`: The app main code<br/>
`config.py`: python script to initialize the configuration included in the `config.txt` file<br/>
`config.txt`: configuration file<br/>
`requirements.in`: input configuration file to be used together with pip-tools<br/>
`requirements.txt`: configuration file to be installed<br/>
`server.py`: the app initialization file<br/>
`users.db`: sqlite3 database with user information<br/>
`users_mgt.py`: helper file for the user management process<br/>
`scopusRetrieval.py`: Code to retrieve publication data from elsevier developer Author Retrieval API<br/>
`scopusRetrievalViews.py`: Alternative Code to retrieve publication data from elsevier developer Author Retrieval API<br/>

### Running an app locally

To run an app locally:

1. (optional) create and activate new virtualenv:

```
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

2. `pip install -r requirements.txt`
3. `flask run` or `python app.py`
4. open http://127.0.0.1:5000 in your browser or
5. `flask run --host=0.0.0.0` or `gunicorn --bind 0.0.0.0:8000 wsgi:application` to open for external connections

### Deployng to Heroku
1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Login to your heroku account: `heroku login`
3. Create the app: `heroku create`
4. Deploy to Heroku: `git push heroku master`
5. Access the app via the address provided by Heroku

