from flask import Blueprint
from flask import render_template
from providers.ArticleProvider import ArticleProvider
import lib.keywords as keywords


blog = Blueprint('blog', __name__)

a = ArticleProvider()


@blog.route('/')
def index():
    for key, value in a.latest().iteritems():
        print key, value
    return render_template("index.html", title="index", items=a.parsed_list)


@blog.route('/<year>/<month>/<day>/<title>/')
def fancy(year, month, day, title):
    new_url = "%s/%s/%s/%s/" % (year, month, day, title)
    article = a.fetch_one(new_url)
    #links = keywords.get_links(article["tags"].split())
    #print links
    #return render_template("article.html", title=article["title"], item=article, links=links)
    return render_template("article.html", title=article["title"], item=article)
