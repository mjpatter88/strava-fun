from bs4.element import Tag


class Activity:
    def __init__(self, entry: Tag) -> None:
        self.activity_id = entry.get("id")

        name_block = entry.find(attrs={"data-testid": "owners-name"})
        if not name_block:
            print(entry)
            return
        self.athlete_name = name_block.string
        self.athlete_id = name_block["href"].split("/")[-1]

        activity_block = entry.find(attrs={"data-testid": "activity_entry_container"})
        # print(activity_block)
        distance_span = activity_block.find("span", string="Distance")
        if distance_span:
            distance_block = distance_span.parent
            # The last child in the block contains the distance value
            distance_div = distance_block.contents[-1]
            self.distance = distance_div.contents[0]
            self.distance_unit = distance_div.contents[1].attrs['title']
        else:
            # print("Distance span not found")
            pass

        pace_span = activity_block.find("span", string="Pace")
        if pace_span:
            pace_block = pace_span.parent
            # The last child in the block contains the pace value
            pace_div = pace_block.contents[-1]
            self.pace = pace_div.contents[0]
            self.pace_unit = pace_div.contents[1].attrs['title']
        else:
            # print("Pace span not found")
            pass

        time_span = activity_block.find("span", string="Time")
        if time_span:
            time_block = time_span.parent
            # The last child in the block contains the time value
            time_div = time_block.contents[-1]
            self.time = time_div.contents[0]
            self.time_unit = time_div.contents[1].attrs['title']
        else:
            # print("Time span not found")
            pass

        # can find by the title under the svg with "testid: activity-icon"
        # reference how it is done here
        # https://github.com/terrettaz/strava-tools/blob/master/stravatools/scraper.py#L198
        self.type = "foo"
