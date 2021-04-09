from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileStorage
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import Email, EqualTo, DataRequired, Length
from comunidade.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired('Preencha este campo.'), Length(3, 15, 'Seu username tem que ter entre 3 à 15 caracteres.')])
    email = StringField('E-mail', validators=[DataRequired('Preencha este campo.'), Email('Digite um endereço de e-mail válido.')])
    senha = PasswordField('Senha', validators=[DataRequired('Preencha este campo.'), Length(8, 20, 'Sua senha tem que ter entre 8 à 20 caracteres.')])
    confirmar_senha = PasswordField('Confirme a senha', validators=[DataRequired('Confirme sua senha.'), EqualTo('senha', 'Este campo tem que ser igual à sua senha.')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        if Usuario.query.filter_by(email=email.data).first():
            raise ValidationError('Já existe uma conta com esse endereço de e-mail.')


class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired('Preencha este campo.'), Email('Digite um endereço de e-mail válido.')])
    senha = PasswordField('Senha', validators=[DataRequired('Preencha este campo.'), Length(8, 20, 'Senha inválida, sua senha tem entre 8 à 20 caracateres.')])
    lembrar_login = BooleanField('Lembrar Login')
    botao_submit_login = SubmitField('Fazer Login')


class FormEditarPerfil(FlaskForm):
    email = StringField('Email', validators=[Email('Digite um endereço de e-mail válido.')])
    username = StringField('Nome de usuário', validators=[Length(3, 15, 'Seu username tem que ter entre 3 à 15 caracteres.')])
    foto_perfil = FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg', 'png'], 'O arquivo não tem uma extensão aprovada: jpg, png.')])
    curso_excel = BooleanField('Excel')
    curso_python = BooleanField('Python')
    curso_sql = BooleanField('SQL')
    curso_powerbi = BooleanField('Power Bi')
    curso_html = BooleanField('HTML')
    curso_css = BooleanField('CSS')
    botao_submit_salvar = SubmitField('Salvar')

    def validate_email(self, email):
        if current_user.email != email.data:
            if Usuario.query.filter_by(email=email.data).first():
                raise ValidationError('Já existe uma conta com esse endereço de e-mail.')


class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired('Preencha este campo.'), Length(2, 140, 'O título do post tem que ter entre 2 à 140 caracteres.')])
    corpo = TextAreaField('Corpo do Post', validators=[DataRequired('Preencha este campo.'), Length(50, 50000, 'O corpo do post tem que ter entre 50 à 50000 caracteres.')])
    botao_submit = SubmitField('Criar Post')


