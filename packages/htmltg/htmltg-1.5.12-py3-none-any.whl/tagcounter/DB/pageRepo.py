from sqlalchemy.orm import sessionmaker
from tagcounter.DB.models.domain import engine, Base
from tagcounter.DB.models.page import Page


class PageRepo:
    def __init__(self):
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def add_page(self, page):
        self.session.add(page)
        self.session.commit()

    def get_page_by_domain_id_and_url(self, domain_id, url):
        page = self.session.query(Page).filter(Page.domain_id == domain_id, Page.url == url).first()
        return page

    def get_pages_by_domain_id(self, domain_id):
        pages = self.session.query(Page).filter(Page.domain_id == domain_id)
        return pages
