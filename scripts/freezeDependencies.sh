source .venv/bin/activate
pip freeze > requirements.txt
echo '--extra-index-url https://__token__:${ACCESS_TOKEN}@gitlab.com/api/v4/groups/63211292/-/packages/pypi/simple' >> requirements.txt
