from comunidade import app, login_manager, pasta_raiz
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from PIL import Image
from datetime import datetime
import pytz
import secrets
import os

db = SQLAlchemy(app)

@login_manager.user_loader
def carregar_usuario(user_id):
    return Usuario.query.get(int(user_id))


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    senha = db.Column(db.String, nullable=False)
    foto_perfil = db.Column(db.String, default='default.jpg')
    posts = db.relationship('Post', backref='autor', lazy=True)
    cursos = db.Column(db.String, default='Não informado', nullable=False)

    def contar_posts(self):
        return len(self.posts)

    def _apagar_foto(self):
        if self.foto_perfil == 'default.jpg':
            pass
        else:
            nome_imagem = self.foto_perfil
            caminho_completo = os.path.join(pasta_raiz, 'static/fotos_perfil', nome_imagem)
            os.remove(caminho_completo)
            self.foto_perfil = 'default.jpg'

    def salvar_foto(self, imagem):
        # Colocando codigo no nome da imagem
        codigo = secrets.token_hex(8)
        nome, extensao = os.path.splitext(imagem.filename)
        nome_arquivo = (nome + codigo + extensao)
        caminho_completo = os.path.join(pasta_raiz, 'static/fotos_perfil', nome_arquivo)

        # Redimensionando a imagem
        basewidth = 480
        imagem_reduzida = Image.open(imagem)
        wpercent = (basewidth / float(imagem_reduzida.size[0]))
        hsize = int((float(imagem_reduzida.size[1]) * float(wpercent)))
        imagem_reduzida = imagem_reduzida.resize((basewidth, hsize), Image.ANTIALIAS)
        # size = (640, 480)
        # imagem_reduzida = Image.open(imagem)
        # imagem_reduzida.thumbnail(size)
        imagem_reduzida.save(caminho_completo)
        # Editando no banco de dados
        self._apagar_foto()
        self.foto_perfil = nome_arquivo

    def atualizar_cursos(self, form_cursos):
        lista_cursos = [campo.label.text for campo in form_cursos if 'curso_' in campo.name and campo.data]
        self.cursos = ';'.join(lista_cursos)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    titulo = db.Column(db.String, nullable=False)
    corpo = db.Column(db.Text, nullable=False)
    data_publicacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def save_new_data(self):
        self.data_publicacao = datetime.now(pytz.timezone('Brazil/East'))
