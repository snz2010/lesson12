from flask import Flask, request, render_template
from settings import ANC_LIST

app = Flask(__name__)

anc_list = []


@app.route('/')  # главная страница "МЕНЮ"
def index():
    if app.config['online']:
        return render_template("index.html")
    else:
        return "<h2>Приложение поиска кандидатов не работает</h2>"


@app.route("/candidate/<int:num>")  # поиск по номеру
def candidate(num):
    if num is None:
        return "<h2>Введите параметр: номер соискателя</h2>"
    n = int(num)
    if n > 0 and n < len(ANC_LIST) + 1:
        name = ANC_LIST[n - 1]['name']
        position = ANC_LIST[n - 1]['position']
        skills = ANC_LIST[n - 1]['skills']
        picture = ANC_LIST[n - 1]['picture']
        age = str(ANC_LIST[n - 1]['age'])
        return render_template('candidate.html', candidate_name=name, candidate_position=position,
                               candidate_skills=skills, candidate_picture=picture, candidate_age=age)
    else:
        return "<h2>Кандидат с указанным номером не найден</h2>"


@app.route("/list/")  # все кандидаты
def page_list():
    return render_template("list.html", list=ANC_LIST)


@app.route("/search/")  # search?name=<x> для поиска по совпадению
def page_search():
    x = request.args.get("name")
    if x is None:
        return "<h2>Отсутствует параметр: <b>?name=ИмяКандидата</b></h2>"
    names_match = []
    for item in ANC_LIST:
        if not app.config['case-sensitive']:
            lower_name = x.lower()
            if lower_name in item['name'].lower():
                id_and_name = {}
                id_and_name['id'] = item['id']
                id_and_name['name'] = item['name']
                names_match.append(id_and_name)
        else:
            if x in item['name']:
                id_and_name = {}
                id_and_name['id'] = item['id']
                id_and_name['name'] = item['name']
                names_match.append(id_and_name)
    if len(names_match):
        return render_template("search.html", list=names_match, count=len(names_match))
    return "<h2>Совпадений не найдено</h2>"


@app.route("/skill/")  # для поиска по навыкам
def page_skills():
    skill = request.args.get("name")
    if skill is None:
        return "<h2>Отсутствует параметр поиска: навык</h2>"
    if app.config['limit']:
        limit = int(app.config['limit'])
    else:
        limit = 0
    names_match = []
    for item in ANC_LIST:
        lower_skill = skill.lower()
        if lower_skill in item['skills'].lower():
            names_match.append(item)
    if len(names_match):
        if limit == 0:
            return render_template("search.html", list=names_match, count=len(names_match))
        else:  # ограничения из конфигурации
            new_list = []
            ind = 0
            for item in names_match:
                if ind < limit:
                    new_list.append(item)
                    ind += 1
                else:
                    break
            return render_template("search.html", list=new_list, count=len(names_match), limit=limit)
