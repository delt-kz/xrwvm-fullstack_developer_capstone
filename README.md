# fullstack_developer_capstone

Best Cars dealership portal for the IBM Full Stack Application Development Capstone Project.

The dealership, team profiles and contact details are fictional classroom examples.


## Architecture
React is served by Django. Django uses SQLite for users and vehicle models, a Node/Express + MongoDB API for dealerships and reviews, and a Flask/NLTK VADER microservice for sentiment. Course sample data and all demonstration reviews are educational examples, not records of real purchases.

## Run locally
1. In `server/frontend`, run `npm ci` and `npm run build`.
2. Install `server/requirements.txt`, then run `python server/manage.py migrate` and `python server/manage.py seed_cars`.
3. Start MongoDB and the Node service using `docker compose up -d mongo_db api sentiment`.
4. Run `python server/manage.py createsuperuser` to create your own development administrator.
5. Run `python server/manage.py runserver 127.0.0.1:8000` and open http://127.0.0.1:8000/.

Alternatively, `docker compose up --build` builds all four services. The development database volume retains MongoDB data. Django's container SQLite database is ephemeral; mount persistent storage before using it beyond a classroom demonstration.

## Verification
`python server/manage.py test djangoapp` tests authentication, registration conflicts, review authorization/identity, filtering and vehicle response shape. GitHub Actions also checks migrations, Node syntax and the production React build. Actual runtime evidence is collected separately; test doubles are used only in unit tests.

## Development scope
This is a classroom demonstration. Never use real customer data or production credentials. The sample Django development secret and DEBUG mode are not suitable for a production deployment.
