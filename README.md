# Consumer Affairs Challenge

## Instructions to run the project (*nix systems)

1. Clone the repository and go in the repository:

    git clone git@github.com:jeacaveo/ca_challenge.git
    cd ca_challenge

2. Create the virtualenv:

    mkvirtualenv --python=/usr/bin/python3.4 ca_challenge

3. Install the requirements:

    pip install -r requirements/dev.txt

4. Run the tests:

    python manage.py test

5. Get the coverage report (from the project/repository root):

    coverage run --source='.' manage.py test
    coverage report

6. Run migrations:

    python manage.py migrate

7. Run the application:

    python manage.py runserver

8. Go to admin portal:

    http://127.0.0.1:8000/admin/

    Credentials: admin/admin or user1/user1 or user2/user2.


## API

### /api/token/auth/

    Method: POST
    Payload: {"username": "XXXX", "password": "XXXX"}
    Response: {"token": "XXXX.XXXX.XXXX"}

### /api/reviews/

    Method: GET
    Headers: content-type: application/json
             authorization: JWT token
    Params: nested=true (optional)

### /api/reviews/

    Method: POST
    Headers: content-type: application/json
             authorization: JWT token
    Payload: {"rating": 5, "title": "XXXX", "summary": "XXXX", "company": 1}

### Initial data (IDs for each one in parenthesis)

    Users: admin (1), user1 (2), user2 (3)
    Companies: Company X (1)
    Reviews: Review by User 1 (1), Review by User 2 (2)
