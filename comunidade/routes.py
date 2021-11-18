from flask import render_template, request, flash, redirect, url_for, abort
from comunidade import app, bcrypt
from comunidade.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from comunidade.models import Usuario, Post, db
from flask_login import login_user, logout_user, current_user, login_required

db.create_all()
db.session.commit()

@app.route('/')
def home():
    posts = Post.query.order_by(Post.id)
    return render_template('home.html', posts=posts)


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required
def usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_criarconta = FormCriarConta()
    form_login = FormLogin()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_login.data)
            flash(f'Login feito com sucesso no email: {form_login.email.data}', 'alert-success')
            parametro_url = request.args.get('next')
            if parametro_url:
                return redirect(parametro_url)
            else:
                return redirect(url_for('home'))
        else:
            flash('Falha no login, senha incorreta.', 'alert-info')
    # else:
    #     flash('Falha no login, email incorreto.', 'alert-danger')
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_crypt = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf8') # Decode para decodificar para ser inserida no banco de dados corretamente
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_crypt)
        db.session.add(usuario)
        db.session.commit()
        flash(f'Conta criada com sucesso para o email: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout feito com sucesso', 'alert-success')
    return redirect(url_for('home'))


@app.route('/post/criar', methods=['GET', "POST"])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        post.save_new_data()
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)


@app.route('/perfil')
@login_required
def meu_perfil():
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('meuperfil.html', foto_perfil=foto_perfil)


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            current_user.salvar_foto(form.foto_perfil.data)
        current_user.atualizar_cursos(form)
        db.session.commit()
        flash('Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('meu_perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
        checks = [check for check in form if 'curso_' in check.name]
        for check in checks:
            if check.label.text in current_user.cursos:
                check.data = True
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            db.session.commit()
            flash('Post Atualizado com sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        db.session.delete(post)
        db.session.commit()
        flash('Post excluído com sucesso!', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)
