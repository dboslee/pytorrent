# pytorrent
This should work with python 3.6 and up

## Dev setup
1. Fork and clone the repo
   ```
   git clone https://github.com/{username}/pytorrent.git
   ```
2. Setup python virtual environment
   ```
   cd pytorrent
   virtualenv env
   source env/bin/activate
   ```
3. Install dev dependencies
   ```
   pip install -r dev-requirements.txt
   ```

## Contribution Guide
   
   Run tests and linting before submitting a PR
   ```
   python -m unittest discover -s ./test
   flake8
   ```