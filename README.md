# e6-blogs
> API Server to store user's blogs.

## Requirements
`python>=3.10`
`pip>=22.0.2`
`sqlite3>=3.30.0`


## Deployment
```bash
$ git clone https://github.com/gouravtulsani/e6data.git
$ cd e6data
e6data $ python -m venv venv  # create virtualenv
e6data $ source venv/bin/activate  # activate virtualenv
e6data $ pip install -r requirements.txt  # install required packanges
e6data $ sqlite3 instance/blogs.db < e6blogs/schema.sql  # DB Migrations
```

### To start the development server

```bash
e6data $ cd ./e6blogs  # move inside project directory
e6blogs $ export FLASK_APP=__init__.py
e6blogs $ flask run --debug
```
> To check API Docs visit [api-docs here](http://localhost:5000/apidocs/)

## Testing
```bash
# `run_test` script uses pytest, it also takes care of setting up and cleaning of test db.
e6data $ ./run_test  # to run tests.
```

