from random import randint
from datetime import datetime

from resources.dbcontext import DbContext
from resources.security import encrypt


def execute_sql(sql: str, parameters: dict):
    dbcontext: DbContext = DbContext(in_testing=True)
    try:
        dbcontext.start()
        result = dbcontext.execute(sql, parameters)
        dbcontext.commit()

        return result
    finally:
        dbcontext.finish()


def prepare_headers(jwt_token: str = None) -> dict:
    headers = {"Content-Type": "application/json"}
    if jwt_token is not None:
        headers["Authorization"] = f"Bearer {jwt_token}"

    return headers


def generate_users(amount_users: int = 1):
    clean_users(amount_users)
    sql: str = "INSERT INTO users(email, password, active) VALUES(:email, :password, :active)"
    for x in range(1, amount_users):
        execute_sql(sql, parameters={
            "email": f"{x}@iggle.com",
            "password": encrypt("123456"),
            "active": True if x % 2 == 0 else False
        })


def clean_users(amount_users):
    sql: str = "DELETE FROM users WHERE email = :email"
    for x in range(1, amount_users):
        execute_sql(sql, parameters={"email": f"{x}@iggle.com"})


def generate_application(name: str):
    clean_application(name)
    sql = "INSERT INTO public.applications"
    sql += " (name, real_name, model, description, active, created_at, created_by, updated_at, updated_by)"
    sql += " VALUES (:name, :real_name, :model, :description, :active, :created_at, :created_by, :updated_at, :updated_by)"
    parameters = {
        "name": name,
        "real_name": name,
        "model": randint(1, 3),
        "description": "BláBláBláBláBláBláBláBláBláBláBláBláBláBláBláBláBláBláBláBlá",
        "active": True,
        "created_at": datetime.now(),
        "created_by": 1,
        "updated_at": datetime.now(),
        "updated_by": 1,
    }
    execute_sql(sql, parameters)


def clean_application(name: str):
    sql = "DELETE FROM applications WHERE name = :name"
    if type(name) is list:
        for n in name:
            execute_sql(sql, {"name": n})
    else:
        execute_sql(sql, {"name": name})


def clean_feature(name: str):
    sql = "DELETE FROM application_features WHERE name = :name"
    if type(name) is list:
        for n in name:
            execute_sql(sql, {"name": n})
    else:
        execute_sql(sql, {"name": name})


def get_bigger_text():
    return """ 
        O que é Lorem Ipsum?
        Lorem Ipsum é simplesmente uma simulação de texto da indústria tipográfica e de impressos, e vem sendo utilizado 
        desde o século XVI, quando um impressor desconhecido pegou uma bandeja de tipos e os embaralhou para fazer um livro de 
        modelos de tipos. Lorem Ipsum sobreviveu não só a cinco séculos, como também ao salto para a editoração eletrônica, 
        permanecendo essencialmente inalterado. Se popularizou na década de 60, quando a Letraset lançou decalques contendo 
        passagens de Lorem Ipsum, e mais recentemente quando passou a ser integrado a softwares de editoração eletrônica 
        como Aldus PageMaker.
        Porque nós o usamos?
        É um fato conhecido de todos que um leitor se distrairá com o conteúdo de texto legível de uma página quando estiver 
        examinando sua diagramação. A vantagem de usar Lorem Ipsum é que ele tem uma distribuição normal de letras, ao contrário 
        de "Conteúdo aqui, conteúdo aqui", fazendo com que ele tenha uma aparência similar a de um texto legível. Muitos softwares de 
        publicação e editores de páginas na internet agora usam Lorem Ipsum como texto-modelo padrão, e uma rápida busca por 'lorem ipsum'
        mostra vários websites ainda em sua fase de construção. Várias versões novas surgiram ao longo dos anos, eventualmente 
        por acidente, e às vezes de propósito (injetando humor, e coisas do gênero).
        De onde ele vem?
        Ao contrário do que se acredita, Lorem Ipsum não é simplesmente um texto randômico. Com mais de 2000 anos, 
        suas raízes podem ser encontradas em uma obra de literatura latina clássica datada de 45 AC. Richard McClintock, 
        um professor de latim do Hampden-Sydney College na Virginia, pesquisou uma das mais obscuras palavras em latim, 
        consectetur, oriunda de uma passagem de Lorem Ipsum, e, procurando por entre citações da palavra na literatura clássica, 
        descobriu a sua indubitável origem. Lorem Ipsum vem das seções 1.10.32 e 1.10.33 do "de Finibus Bonorum et Malorum" 
        (Os Extremos do Bem e do Mal), de Cícero, escrito em 45 AC. Este livro é um tratado de teoria da ética muito popular 
        na época da Renascença. A primeira linha de Lorem Ipsum, "Lorem Ipsum dolor sit amet..." vem de uma linha na seção 1.10.32.
        O trecho padrão original de Lorem Ipsum, usado desde o século XVI, está reproduzido abaixo para os interessados. 
        Seções 1.10.32 e 1.10.33 de "de Finibus Bonorum et Malorum" de Cicero também foram reproduzidas abaixo em sua forma exata 
        original, acompanhada das versões para o inglês da tradução feita por H. Rackham em 1914.
    """
