# Consumer Affairs Challenge

## Instructions to run the project

1. Clone the repository and go in the repository:

    git clone git@github.com:jeacaveo/ppt_test1.git
    cd ppt_test1

2. Create the virtualenv:

    mkvirtualenv --python=/usr/bin/python3.4 ppt_test

3. Install the requirements:

    pip install -r requirements/dev.txt

4. Run the tests:

    python manage.py test

5. Run migrations:

    python manage.py migrate

6. Run the tests:

    - python manage.py test

7. Get the coverage report (from the project/repository root):

    - coverage run --source='.' manage.py test
    - coverage report

8. Run the application:

    python manage.py runserver
