class Race:
    candidates = []

    def __init__(self, race_name, county):
        self.race_name = race_name
        self.county = county
        self.rows_to_write = []

    def __eq__(self, other):
        return (
            self.race_name == other.race_name and
            self.county == other.county
        )

    def __ne__(self, other):
        return(
            self.race_name != other.race_name and
            self.count != other.county
        )

    def __str__(self):
        return self.race_name + " " + self.county
