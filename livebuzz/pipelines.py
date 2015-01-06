# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from models import Articles, db_connect, create_articles_table

class LivebuzzPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_articles_table(engine)
        self.Session = sessionmaker(bind = engine)

    def process_item(self, item, spider):
        session = self.Session()
        article = Articles(**item)

        try:
            session.add(article)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
