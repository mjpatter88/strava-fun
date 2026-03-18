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
        print(activity_block)

        self.distance = "foo"
        self.time = "foo"
        self.pace = "foo"

        # can find by the title under the svg with "testid: activity-icon"
        self.type = "foo"
