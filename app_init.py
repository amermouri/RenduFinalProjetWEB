from sqlalchemy import *
import hashlib

SALT = 'foo#BAR_{baz}^666'

def hashFor(password):
    salted = '%s @ %s' % (SALT, password)
    return hashlib.sha256(salted).hexdigest() 


# ............................................................................................... #
#creation de toutes les tables
db = create_engine('sqlite:///base.db', echo=True)
metadata = MetaData(db)

utilisateurs = Table('utilisateurs', metadata,
    Column('utilisateur_id', Integer, primary_key=True),
    Column('login', String, nullable=False),
    Column('nom', String(40)),
    Column('prenom', String(40), nullable=False),
    Column('annee', String(10)),
	Column('mail', String),
	Column('password_hash', String, nullable=False),
	Column('date_naissance', Integer),
    sqlite_autoincrement=True)


metadata.create_all(db)

connection = db.connect();

connection.execute(utilisateurs.insert().values(login='root', prenom='Administrateur', nom="Administrateur",password_hash=hashFor('root'), mail="master@worldwild-tc.fr", date_naissance="03/06/2015", annee="3TC"))

connection.close()
