# ............................................................................................... #

from flask  import *
from sqlalchemy import *
from markdown import markdown
from math import fabs
import os, hashlib
import urllib  
import datetime
from time import strftime
from sqlalchemy.ext.automap import automap_base
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from werkzeug import secure_filename




# ............................................................................................... #
SALT = 'foo#BAR_{baz}^666'
UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.secret_key = os.urandom(256)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ............................................................................................... #
#creation de toutes les tables
db = create_engine('sqlite:///base.db', echo=True)
metadata = MetaData(db)

utilisateurs = Table('utilisateurs', metadata,
    Column('utilisateur_id', Integer, primary_key=True),
    Column('login', String, nullable=False),
    Column('nom', String(40)),
    Column('prenom', String(40)),
    Column('annee', String(10)),
	Column('mail', String),
	Column('password_hash', String, nullable=False),
	Column('date_naissance', Integer),
    sqlite_autoincrement=True)
   

fichier = Table('fichier', metadata, 
          Column('fichier_id',Integer, primary_key=True),
          Column('nom', String(40)),
          Column('annee', String(10)), 
          Column('cours', String(10)), 
          Column('type_fich', String(10)),
          )

metadata.create_all(db)


# ............................................................................................... #

def hashFor(password):
    salted = '%s @ %s' % (SALT, password)
    return hashlib.sha256(salted).hexdigest()   
    
def authenticate(login, password):
  connection = db.connect()
  print login, password
  
  try:
    if connection.execute(select([utilisateurs.c.login]).where(utilisateurs.c.login == login)).fetchone() != None:
      if connection.execute(select([utilisateurs]).where(and_(utilisateurs.c.login == login, utilisateurs.c.password_hash == hashFor(password)))).fetchone() != None:
        return (True, "Login Success")
      else:
        return (False, "Mauvais mot de passe !")
    else:
      return (False, "Impossible de trouver l'utilisateur !")
  finally:
    connection.close()

def generate_token(pseudo,expiration=600):
  s= Serializer(app.config['SECRET_KEY'],expires_in = expiration)
  tok = s.dumps({'login':pseudo})
  return tok

def verify_auth_token(token):
  s=Serializer(app.config['SECRET_KEY'])
  try:
    userData = s.loads(token)
    user = userData['login']
    return user
  except SignatureExpired:
    return None
  except BadSignature:
    return None

def signUp(login, nom, prenom, annee, mail, motDePasse, date_naissance):
  connection = db.connect()
  try:
    if connection.execute(select([utilisateurs.c.login]).where(utilisateurs.c.login == login)).fetchone() is None:
      connection.execute(utilisateurs.insert().values(login=login, nom=nom, prenom=prenom,annee=annee, mail=mail, password_hash=hashFor(motDePasse),date_naissance=date_naissance))
      return True
    else:
      return False
  finally:
    connection.close()
    
def retrieveProfile(username):
  connection = db.connect()
  try:
    if connection.execute(select([utilisateurs.c.login]).where(utilisateurs.c.login == username)).fetchone() != None: 
      for row in connection.execute(select([utilisateurs.c.nom, utilisateurs.c.prenom, utilisateurs.c.annee, utilisateurs.c.mail, utilisateurs.c.date_naissance]).where(and_(utilisateurs.c.login == username))):
        return row
    else :
      return None
  finally :
    connection.close()

def retrieveFile(an,mat):
  connection = db.connect()
  try:
    select([fichier.c.nom]).where(and_(fichier.c.annee == an, fichier.c.cours == mat))
    usr = connection.execute(select([fichier.c.nom]).where(and_(fichier.c.annee == an, fichier.c.cours == mat))).fetchall()
    return usr
  finally:
    connection.close()
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# ............................................................................................... #

@app.route('/')
def index():
  return redirect('static/index.html')


  
@app.route('/login', methods=['POST'])
def login():
  content = request.get_json(force=True)
  print content
  print content['login']
  res = authenticate(content['login'], content['motDePasse'])
  if res[0]:  
    token = generate_token(content['login'])
    return json.dumps({'success':True, 'token' : token.decode('ascii')})
  else:     
    return json.dumps({'success':False, 'result':res[1]})

@app.route('/users', methods=['POST'])
def user():
  content = request.get_json(force=True)
  tok = content['Token']
  user = verify_auth_token(tok)
  if user != None :
    return json.dumps({'username':user})
  else :
    return redirect('/')
    
@app.route('/validate', methods=['POST'])
def validerToken():
  content = request.get_json(force=True)
  res = verify_auth_token(content['token'])
  if res is None:
    return json.dumps({'success':False})
  else:
    return json.dumps({'success':True}) 

@app.route('/signUp', methods=['POST'])
def signup():
  content = request.get_json(force=True)
  print content
  res = signUp(content['login'], content['nom'], content['prenom'], content['annee'], content['mail'], content['motDePasse'], content['date_naissance'])
  if res :
    tok=generate_token(content['login'])  
    return json.dumps({'success':True,'token' : tok.decode('ascii')})
  else :
    return json.dumps({'success':False})
    
@app.route('/profile', methods=['POST'])
def profile():
  content = request.get_json(force=True)
  tok = content['Token']
  user = verify_auth_token(tok)
  if user != None :
    res = retrieveProfile(user)
    print res
    return json.dumps({'nom':res[0],'prenom':res[1],'annee':res[2],'mail':res[3],'date_naissance':res[4]})
  else :
    return redirect('/')
 
@app.route('/upload', methods=['POST'])
def upload():
    mm = request.form['year']
    pp = request.form['course']
    ll = request.form['type']
    connection = db.connect()
    connection.execute(fichier.insert().values(annee=mm, cours=pp, type_fich=ll))
    connection.close();
    return json.dumps({'mm':mm, 'pp':pp ,'ll':ll })


@app.route('/static/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            connection = db.connect()
            connection.execute((fichier.update().values(nom = filename)).where(and_(fichier.c.annee == request.form['mm'], fichier.c.cours == request.form['pp'],fichier.c.type_fich == request.form['ll'])))
            connection.close();
            return redirect(url_for('uploaded_file',filename=filename))
        else:
          connection = db.connect()
          filename = secure_filename(file.filename)
          connection.execute((fichier.update().values(nom = filename)).where(and_(fichier.c.annee == request.form['mm'], fichier.c.cours == request.form['pp'],fichier.c.type_fich == request.form['ll'])))
          connection.execute(fichier.delete().where(and_(fichier.c.nom == filename)))
          connection.close();
          return redirect('/static/upload.html')
                                    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
                               
from werkzeug import SharedDataMiddleware
app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['UPLOAD_FOLDER']
})

    
@app.route('/download/<annee>/<matiere>')
def download(annee,matiere):
  res = retrieveFile(annee,matiere)
  l = []
  for r in res:
    l.append({'name':r[0]})
  return json.dumps(l)



# ............................................................................................... #
if __name__ == '__main__':
	app.run(debug=True, use_reloader=False)
