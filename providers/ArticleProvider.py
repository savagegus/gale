#!/usr/bin/python

import os
import string
import datetime
import re
import lib.gist as gist
import lib.keywords as keywords

class ArticleProvider:
    def __init__(self):
        self.path = "articles"
        self.list = sorted(os.listdir(self.path), reverse=True)
        self.parser = {
            "title": "",
            "date": "",
            "tags": "",
            "slug": "",
            "old_url": "",
            "new_url": "",
            "content_type": ""}
        self.parsed_list = []
        self.tags = keywords.get_tags()
        for article in self.list:
            if os.path.isfile(self.path + "/" + article):
                self.parsed_list.append(self.parse_article(article, self.parser))


    def latest(self):
        return self.parse_article(self.list_one(), self.parser)

    def list_one(self):
        for item in self.list:
            if os.path.isfile(self.path + "/" + item):
                return item
        exit("couldn't find a file man")

    def fetch_one(self, new_url):
        dummy_article = self.parser
        dummy_article["body"] = "Not Found"
        dummy_article["title"] = "NotFound"
        dummy_article["date"] = "No Date"

        for article in self.parsed_list:
            if article["new_url"] == new_url:
                return article
        return dummy_article

    def rss_dates(self):
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        months = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
        for article in self.parsed_list:
            year, month, day = article["date"].split("/")
            pub_date = datetime.date(int(year), int(month), int(day))
            article["date"] = "%s, %s %s %s 00:00:01 GMT" % (days[pub_date.weekday()], pub_date.day, months[pub_date.month], pub_date.year)

    def atom_dates(self):
        for article in self.parsed_list:
            year, month, day = article["date"].split("/")
            pub_date = datetime.date(int(year), int(month), int(day))
            article["date"] = "%s-%s-%sT00:00:01Z" % (pub_date.year, pub_date.month, pub_date.day)

    def parse_article(self, article, parser):
        f = open(os.path.join(self.path, article))
        text = f.readlines()
        parsed_article = {}
        for line in text:
            for key in parser:
                if key + ': ' in line:
                    parsed_article[key] = line.replace(key + ': ','').replace('\n','')
        parsed_article["body"] = ''.join(text[8:]).decode('utf-8')
        parsed_article["body"] = self.parse_gists(parsed_article["body"])
        words = string.split(parsed_article["body"])
        parsed_article["word_count"] = len(words)
        for k in parser:
            if k not in parsed_article:
                parsed_article[k] = ""
        if parsed_article["tags"] == "":
            parsed_article["tags"] = " ".join(self.parse_keywords(parsed_article["body"], self.tags))
        return self.sanitize(parsed_article)

    def parse_gists(self, body):
        regex = re.compile("\{\% gist [0-9]* \%\}")
        results = regex.findall(body)
        for result in results:
            gist_id = result.decode('utf-8').split(" ")[-2]
            replacement_text = gist.render_gist(gist_id)
            body = body.replace(result, replacement_text)
        return body

    def parse_keywords(self, body, tags):
        return keywords.print_tags(body, tags)

    def sanitize(self, article):
        article = self.sanitize_new_url(article)
        return article

    @staticmethod
    def sanitize_new_url(article):
        if len(article["new_url"]) > 0:
            if article["new_url"][-1] != "/":
                article["new_url"] += "/"
            else:
                if article["date"] > 0 and article["title"] > 0:
                    article["new_url"] = article["date"] + "/" + article["title"].replace(" ", "-").replace("\"", "")
        return article
