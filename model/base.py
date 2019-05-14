from db import DB

class Base(DB.Model):
    __abstract__ = True

    def save_to_db(self):
        DB.session.add(self)
        DB.session.commit()

    def delete_from_db(self):
        DB.session.delete(self)
        DB.session.commit()

