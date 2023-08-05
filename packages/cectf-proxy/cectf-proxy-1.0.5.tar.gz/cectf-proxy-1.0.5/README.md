# cectf-proxy

You need Python 3 and pip installed to set up this project.

Navigate to the project repository and run `./setup_workspace.sh`. This will set up the virtual environment, install the required python dependencies, and set up a default `instance/config.py` that points to the default `cectf-frontend` and `cectf-server` instances running on localhost.

Run `sudo run.sh` to launch the Flask server. It is configured to run the server on `http://127.0.0.1:80` (AKA `http://127.0.0.1`) by default, and so requires sudo access.

Configuration can be done by adding variables to `instance/config.py`.

TODO add some tests

For testing, first do `pip install pytest coverage`. Run `pip install -e .` to install the project in the local virtual environment (the `-e` ensures that it is updated as the project is modified). Run `pytest` to run all tests. Run `coverage run -m pytest` to generate a code coverage report. Run `coverage report` to get the report in the command line, or run `coverage html` to generate an interactive HTML page in `htmlcov/index.html`.
