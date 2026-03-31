from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from models import Activity


def parse(soup):
    feed = soup.find("div", class_="feature-feed")
    print(len(feed.contents))
    # first_entry = feed.contents[0].contents[0]
    # activity = Activity(first_entry)
    # print(f"name: {activity.athlete_name}, id: {activity.athlete_id}")
    activities = []
    for child in feed.contents:
        if child.contents:
            entry = child.contents[0]
            # some feed entries aren't actually activities (like joining a challenge)
            if entry.find(attrs={"data-testid": "activity_entry_container"}):
                activities.append(Activity(entry))

    print(f"found: {len(activities)} activities")
    print("\n**** Last Activity *****")
    last_activity = activities[-1]
    print(f"name: {last_activity.athlete_name}, id: {last_activity.athlete_id}")
    print(f"distance: {last_activity.distance} {last_activity.distance_unit}")
    print(f"time: {last_activity.time} {last_activity.time_unit}")
    print(f"pace: {last_activity.pace} {last_activity.pace_unit}")


def run_local():
    try:
        with open("dashboard.html") as html_doc:
            soup = BeautifulSoup(html_doc, "html.parser")
    except FileNotFoundError:
        print("No dashboard.html found. Please run scrape first.")
        exit()
    parse(soup)

def run_scrape():
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    with sync_playwright() as p:
        # browser = p.chromium.launch()
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.goto("https://www.strava.com/login")

        # accept cookies
        page.get_by_role("button", name="OK").click()

        # enter email and click
        page.get_by_role("textbox", name="Email").fill(email)
        page.get_by_role("button", name="Log in").click()

        # use a password
        page.get_by_role("button", name="Use password instead").click()
        page.get_by_role("textbox", name="Password").fill(password)
        page.get_by_role("button", name="Log in").click()

        # Make sure we redirect to the dashboard
        page.wait_for_url("**/dashboard")

        # Reload the dashboard with 50 entries
        page.goto("https://www.strava.com/dashboard?num_entries=50")
        page.wait_for_timeout(10000)

        # for testing/development purposes, write the html to a file to minimize scraping
        with open("dashboard.html", "w") as f:
            f.write(page.content())
        browser.close()


if __name__ == "__main__":
    run_local()
    # Uncomment the following line to login and scrape strava
    # run_scrape()
