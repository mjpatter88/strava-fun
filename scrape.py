from bs4 import BeautifulSoup

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
            # some feed entries aren't actually activites (like joining a challenge)
            if entry.find(attrs={"data-testid": "activity_entry_container"}):
                activities.append(Activity(entry))

    print(f"found: {len(activities)} activities")
    print(f"name: {activities[-1].athlete_name}, id: {activities[-1].athlete_id}")


def run_local():
    with open("Dashboard_Strava.html") as html_doc:
        soup = BeautifulSoup(html_doc, "html.parser")
    parse(soup)


def run_scrape():
    print("hello")


if __name__ == "__main__":
    run_local()
    # run_scrape()
