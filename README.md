# dt-self-service
 Self Service Portal for Dynatrace

 This branch focuses on adapting the frontend work to backend scripts through Django

## How To Install
- Install Python 3.8.1 from Python Website
    - During install, ensure pip is being installed
    - During install, allow Python directory to be added to PATH
- Open PowerShell or Git Bash and navigate to this directory
- Run "python -m pip install pipenv"
- Run "python -m pipenv install". This will install all dependencies from the Pipfile to a virtual python environment
- Install the seperate backend git project (contact Aaron or George for more information)
- Create ".env" file the root of this project and add backend project path to the PYTHONPATH. <br/>
    This will look like 'PYTHONPATH="C:\\Users\\User\\Documents\\Dynatrace\\dynatrace-fire-team"'

## How to Run
- Run "python -m pipenv shell"
- Run "python manage.py runserver"
