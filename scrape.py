from bs4 import BeautifulSoup
import requests

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
    with open("Dashboard_Strava.html") as html_doc:
        soup = BeautifulSoup(html_doc, "html.parser")
    parse(soup)


def login(email:str, password:str, session:requests.Session):
    print(f"logging in as {email}.")
    # url = "https://www.strava.com/login"
    # response = session.get(url)
    # soup = BeautifulSoup(response.content, 'html.parser')
    # utf8 = soup.find_all('input',
    #                      {'name': 'utf8'})[0].get('value').encode('utf-8')
    # token = soup.find_all('input',
    #                       {'name': 'authenticity_token'})[0].get('value')
    login_data = {
        # 'utf8': utf8,
        # 'authenticity_token': token,
        # 'plan': "",
        'auth_version': 'v2',
        'remember_me': 'on',
        'email': email,
        'password': password
    }
    # print(login_data)
    HEADERS = {'User-Agent': 'strava-fun'}
    response = session.post("https://www.strava.com/session", data=login_data, headers=HEADERS)
    response.raise_for_status()
    print(response.history)
    print(response.history[0].text)
    with open("session.html", "w") as f:
        f.write(response.text)

    response = session.get("https://www.strava.com/dashboard", headers=HEADERS)
    response.raise_for_status()
    print(response.status_code)
    print(response.history)
    print(response.history[0].text)
    # print(response.text)
    with open("dashboard.html", "w") as f:
        f.write(response.text)
    # assert ("<h2>Activity Feed</h2>" in response.content)


def run_scrape():
    session = requests.Session()
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    login(email, password, session)


if __name__ == "__main__":
    run_local()
    # run_scrape()
