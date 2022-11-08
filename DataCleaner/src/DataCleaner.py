import json
import re

from re_tools import drop_day_week_and_year
from my_tools import split_by_stop_word
import constants as const


class DataCleaner:
    def __init__(self, file_name):
        self.has_empty = {}
        with open(file_name, "r") as f:
            self.json_list = json.load(f)
            f.close()
        self.pop_job_description()
        self.check_for_missing_entry()
        self.delete_empty_entry()
        self.parse_title()
        self.parse_location()
        self.parse_qualification()
        self.save_as_json(file_name)

    def get_len(self):
        return len(self.json_list)

    def pop_job_description(self):
        n = self.get_len()
        for i in range(n):
            self.json_list[i].pop("jobDescription")

    def check_for_missing_entry(self):
        n = self.get_len()
        for i in range(n):
            for k in self.json_list[i]:
                if self.json_list[i][k] == "":
                    self.has_empty[i] = self.json_list[i]
                    break
        return self.has_empty

    def delete_empty_entry(self):
        for i in self.has_empty:
            self.json_list.pop(i)

    def parse_title(self):
        n = self.get_len()
        for i in range(n):
            titles = self.json_list[i]["title"]
            titles = re.sub("\(.*?\)", "", titles)
            titles = titles.split(",")
            titles = [t.replace("-", "").lstrip().rstrip() for t in titles]
            self.json_list[i]["Title"] = {}
            titles_len = len(titles)
            self.json_list[i]["Title"]["title1"] = titles[0]
            if titles_len >= 2:
                self.json_list[i]["Title"]["title2"] = titles[1]
            if titles_len >= 3:
                self.json_list[i]["Title"]["title3"] = titles[2]
            self.json_list[i].pop("title")

    def parse_location(self):
        n = self.get_len()
        for i in range(n):
            locations = self.json_list[i]["inOfficeLocation"]
            locations = locations.replace("In-office locations: ", "")
            locations = locations.split(";")
            locations = [loc.strip().replace(" ", "").rstrip(".") for loc in locations]
            locations = [loc.split(",") for loc in locations]
            for loc in locations:
                self.json_list[i]["Location"] = []
                loc_entry = {}
                loc_len = len(loc)
                loc_entry['Country'] = loc[-1]
                if loc_len >= 2:
                    loc_entry["State"] = loc[-2]
                if loc_len >= 3:
                    loc_entry["City"] = loc[-3]
                self.json_list[i]["Location"].append(loc_entry)
            self.json_list[i].pop("inOfficeLocation")
            # print(locations[:2])

    def parse_qualification(self):
        # sw = stop_words()
        n = self.get_len()
        for i in range(n):
            min_quas = self.json_list[i]["minQua"]
            prefer_quas = self.json_list[i]["preferQua"]
            self.json_list[i]["Degree"] = {
                "level": [],
                "field": []
            }
            self.json_list[i]["YOE"] = []
            self.json_list[i]["Experiences"] = []
            self.json_list[i]["ProgrammingSkills"] = []
            for mq in min_quas:
                mq = drop_day_week_and_year(mq)
                mq = split_by_stop_word(mq)
                self.parse_degree_yoe_progskills(mq, i)

            for pq in prefer_quas:
                pq = drop_day_week_and_year(pq)
                pq = split_by_stop_word(pq)
                self.parse_degree_yoe_progskills(pq, i)
            self.json_list[i].pop("minQua")
            self.json_list[i].pop("preferQua")

    def parse_degree_yoe_progskills(self, data, i):
        if "bachelor" in data or "master" in data or "phd" in data:
            for w in data:
                if w == "bachelor" or w == "master" or w == "phd":
                    self.json_list[i]["Degree"]["level"].append(w)
                else:
                    self.json_list[i]["Degree"]["field"].append(w)
        else:
            for w in data:
                if "year" in w:
                    self.json_list[i]["YOE"].append(w)
                else:
                    if w in const.NAMES:
                        self.json_list[i]["ProgrammingSkills"].append(w)
                    else:
                        self.json_list[i]["Experiences"].append(w)

    def save_as_json(self, file_name):
        with open(f'{file_name}_CLEANED', "w") as out:
            json.dump(self.json_list, out)
