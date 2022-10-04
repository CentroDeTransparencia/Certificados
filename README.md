# Certificados02

These are the instructions to deploy the project into [Heroku](https://www.heroku.com/). 

Get in the directory where the code and the PDFs reside, initialise git and create a virtual environment:
```bash
git init
virtualenv venv
```
Now, to use the virtualenv:
```bash
source venv/bin/activate
```
Install dependencies:
``` pip install dash
pip install plotly
pip install gunicorn
```
Rename the python file, and create the other necessary files:
```bash
mv downapp.py app.py
touch .gitignore
vim .gitignore
```
add the following contents
```bash
venv
*.pyc
.DS_Store
.env
```
Then
```bash
touch Procfile
vim Procfile
```
add the following contents
```bash
web: gunicorn app:server
```
Then to consolidate the dependencies into a file:
```bash
pip freeze > requirements.txt
vim app.py
```
change the lines @ the end to
```bash
if __name__ == '__main__':
    app.run_server(debug=True) 
```
Finally
```bash
heroku create downloads02
git push heroku main
git add .
git commit -m 'Initial app boilerplate'
git push heroku master
heroku ps:scale web=1
heroku open
```
last instruction is to see the project online

This was based on the [Heroku for Sharing Public Dash Apps for Free](https://dash.plotly.com/deployment) tutorial.
