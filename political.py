class Race(object):

    def __init__(self, race_name, county):
        self.race_name = race_name
        self.county = county

        self.candidates = []
        self.rows_to_write = {}

        # self.

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


class JoinedRace(Race):
    """docstring for JoinedRace"""
    def __init__(self, race_name, candidates, county, rows_to_write):
        super(JoinedRace, self).__init__(race_name[:-2], county)
        self.race_name = race_name
        self.candidates = candidates
        self.county = county

        self.rows = [rows_to_write]
        self.counties = []

    def __str__(self):
        return self.race_name
