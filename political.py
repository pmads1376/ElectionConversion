class Race:

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

class ComboRace(Race):

    def __init__(self, f, directory):
        self.f = f
        self.directory = directory
        super(ComboRace, self).__init__(self.f[:-6], self.f[-6:-4])
        self.candidates = self.get_candidates()

    def get_candidates(self):
        import csv
        import os

        non_candidates = ['Row Label', 'County']

        with open(os.path.join(self.directory, self.f), 'r') as results_file:
            results_read = csv.DictReader(results_file, delimiter=',')

            try:
                columns = results_read.next()
                # print (type(columns))
            except StopIteration:
                print(self.race_name)

            for value in columns:
                if value not in non_candidates:
                    self.candidates.append(value)