# strava-fun
Have fun with strava data

## Run local
* First follow the "Run Scrape" step to get a scrape.
* Then update commented out line in scrape.py main to `run_local()`.
* `poetry run python scrape.py`

## Run Scrape
* `poetry run playwright install chromium`
* Update commented out line in scrape.py main to `run_scrape()`.
* `poetry run python scrape.py`

## Run tests
* `poetry run pytest`
* `poetry run ptw .`

## Things to do
* Parse activity type
* Get activity details (including geometry)
