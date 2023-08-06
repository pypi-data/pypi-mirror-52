from sqlalchemy.orm import sessionmaker
from tagcounter.DB.models.domain import engine, Base, Domain


class DomainRepo:
    def __init__(self):
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def add_domain(self, domain):
        self.session.add(domain)
        self.session.commit()

    def get_domain_by_name(self, name):
        domain = self.session.query(Domain).filter(Domain.name == name).first()
        return domain
