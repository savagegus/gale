#!/usr/bin/python

import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import datetime
import PyRSS2Gen

import sys
sys.path.append("providers")

from ArticleProvider import ArticleProvider
from PageProvider import PageProvider

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("templates/about.html", title="index")

class BlogHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.a = ArticleProvider()

	def get(self):
		self.render("templates/index.html", title="index", items=self.a.parsed_list)

class RssHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.a = ArticleProvider()

	def get(self):
		self.set_header("Content-Type", "application/rss+xml")
		self.a.atom_dates()
		self.render("templates/index.xml", title="unsure.org blog feed", url="http://unsure.org", author="Matthew Finlayson", email="matt@unsure.org", items=self.a.parsed_list)

class ArticleHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.a = ArticleProvider()

	def get(self, new_url):
		article = self.a.fetch_one(new_url)
		if not article: raise tornado.web.HTTPError(404)
		self.render("templates/article.html", title=article["title"], item=article)

class PageHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.a = PageProvider()

	def get(self, new_url):
		page = self.a.fetch_one(new_url)
		if not article: raise tornado.web.HTTPError(404)
		self.render("templates/article.html", title=page["title"], item=page)

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": True,
}

application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/blog/", BlogHandler),
	(r"/blog/feed/", RssHandler),
	(r"/about/", MainHandler),
	(r"/projects/", MainHandler),
	(r"/blog/([0-9]+/[0-9]+/[0-9]+/[-a-z0-9,]+/)", ArticleHandler),
], **settings)

if __name__ == "__main__":
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
