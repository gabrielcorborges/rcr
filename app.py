"""RestoLab — academia interativa de congruências em Streamlit."""

from __future__ import annotations

import math
import random
from datetime import date

import streamlit as st

from congruencias import (
    LESSONS,
    are_congruent,
    euclidean_division,
    generate_question,
    modular_inverse,
    residue_table,
    solve_linear_congruence,
)


st.set_page_config(page_title="RestoLab · Academia de Congruências", page_icon="🧮", layout="wide")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root{--ink:#15231d;--muted:#69756f;--paper:#f7f6ef;--green:#123d2e;--green2:#1e5b43;--lime:#cdf45e;--line:#dce0d7;--white:#fff;--orange:#ffad66}
.stApp{background:var(--paper);color:var(--ink)} html,body,[class*=css]{font-family:'DM Sans',sans-serif}
h1,h2,h3{font-family:'Space Grotesk',sans-serif!important;letter-spacing:-.035em} [data-testid=stHeader]{background:transparent}
[data-testid=stSidebar]{background:#ebeee4;border-right:1px solid #d8ddd2} [data-testid=stSidebar] .block-container{padding-top:1.6rem}
.block-container{max-width:1240px;padding-top:1.2rem;padding-bottom:4rem}.brand{font:700 1.18rem 'Space Grotesk';display:flex;align-items:center;gap:.65rem;margin-bottom:1rem}
.brand b{display:grid;place-items:center;width:34px;height:34px;background:var(--green);color:var(--lime);border-radius:10px}.tiny{font-size:.78rem;color:var(--muted)}
.hero{position:relative;overflow:hidden;background:var(--green);color:white;border-radius:28px;padding:3.5rem;margin:.5rem 0 1.1rem;min-height:300px}
.hero:after{content:'mod m';position:absolute;right:-1rem;bottom:-4.5rem;font:700 10rem 'Space Grotesk';color:rgba(205,244,94,.08);transform:rotate(-6deg)}
.hero h1{font-size:clamp(2.7rem,6vw,5.2rem);line-height:.96;color:white;max-width:800px;margin:.7rem 0 1.1rem}.hero p{color:#cbd9d1;font-size:1.07rem;line-height:1.6;max-width:610px}.lime{color:var(--lime)}
.tag{display:inline-block;border:1px solid rgba(255,255,255,.2);border-radius:999px;padding:.42rem .8rem;font-size:.72rem;font-weight:700;letter-spacing:.09em}.kicker{color:#52765f;font-size:.72rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase}
.section-head{margin:2.2rem 0 1rem}.section-head h1,.section-head h2{margin:.15rem 0;font-size:2.3rem}.section-head p{color:var(--muted);margin:.2rem 0}
.card{height:100%;background:white;border:1px solid var(--line);border-radius:18px;padding:1.3rem;box-shadow:0 5px 20px rgba(24,49,37,.035)}.card h3{margin:.55rem 0}.card p{color:var(--muted);line-height:1.55;font-size:.92rem}
.icon{font-size:1.45rem}.formula{background:#e9efcf;border:1px solid #dce7b6;color:#294632;border-radius:14px;padding:1.1rem;text-align:center;font:600 1.25rem 'Space Grotesk';margin:1rem 0}
.dark{background:#183329;color:white;border-radius:20px;padding:1.5rem}.dark h2,.dark h3{color:white;margin-top:.2rem}.dark p{color:#c6d4cd}.lesson-row{border-left:3px solid var(--lime);padding-left:1rem}
.level{font-size:.69rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#668043;background:#edf2dc;border-radius:999px;padding:.3rem .55rem}.rule{border-top:1px solid var(--line);margin:1rem 0}
.quiz{background:linear-gradient(135deg,#153b2d,#1d523d);color:white;border-radius:24px;padding:2rem}.quiz h2{font-size:2rem;color:white}.quiz p{color:#c7d6cf}.feedback{border-radius:14px;padding:1rem}
.clock{width:220px;height:220px;border:8px solid #234c3b;border-radius:50%;position:relative;margin:1rem auto;background:#fefefb;box-shadow:inset 0 0 0 2px #d9dfd5}.clock-num{position:absolute;transform:translate(-50%,-50%);font:700 .84rem 'Space Grotesk';color:#234c3b}.clock-center{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);background:var(--lime);border-radius:50%;padding:.85rem;font-weight:700}.table-cell{display:inline-grid;place-items:center;width:35px;height:35px;border:1px solid #d8ddd4;background:white;font-size:.8rem}.table-head{background:#173d2e;color:white;font-weight:700}
.badge{display:inline-flex;align-items:center;gap:.35rem;padding:.5rem .75rem;border-radius:10px;background:#edf1e4;color:#425b48;font-size:.82rem;font-weight:600;margin:.15rem}.road{display:flex;gap:.65rem;align-items:center;margin:.7rem 0}.road-dot{flex:0 0 38px;height:38px;border-radius:50%;display:grid;place-items:center;background:#dfe4d8;font-weight:700}.road-dot.done{background:var(--green);color:var(--lime)}
div[data-testid=stMetric]{background:white;border:1px solid var(--line);padding:1rem;border-radius:15px}div[data-testid=stButton] button{border-radius:10px;font-weight:700;min-height:2.65rem}div[data-testid=stButton] button[kind=primary]{background:var(--green);border-color:var(--green)}
.footer{border-top:1px solid var(--line);margin-top:4rem;padding-top:1.2rem;color:#79847e;font-size:.8rem;display:flex;justify-content:space-between}
@media(max-width:700px){.hero{padding:2rem 1.3rem;min-height:auto}.hero h1{font-size:2.75rem}.block-container{padding-left:1rem;padding-right:1rem}.clock{width:190px;height:190px}.footer{display:block}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

PAGES = ["Início", "Trilha de aulas", "Arena de prática", "Laboratório", "Relógio modular", "Tabelas", "Guia de bolso"]


def init_state() -> None:
    defaults = {
        "xp": 0, "streak": 0, "best_streak": 0, "answered": 0, "correct": 0,
        "difficulty": "Médio", "question": None, "feedback": None, "lesson_done": [],
        "question_seed": random.randint(0, 1_000_000), "daily_goal": 5,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    if st.session_state.question is None:
        st.session_state.question = generate_question(st.session_state.difficulty, st.session_state.question_seed)


def next_question() -> None:
    st.session_state.question_seed = random.randint(0, 1_000_000)
    st.session_state.question = generate_question(st.session_state.difficulty, st.session_state.question_seed)
    st.session_state.feedback = None


def check_answer(choice: int) -> None:
    if st.session_state.feedback is not None:
        return
    question = st.session_state.question
    st.session_state.answered += 1
    if choice == question.answer:
        bonus = {"Fácil": 10, "Médio": 15, "Difícil": 25}[question.difficulty]
        st.session_state.correct += 1
        st.session_state.streak += 1
        st.session_state.best_streak = max(st.session_state.best_streak, st.session_state.streak)
        st.session_state.xp += bonus
        st.session_state.feedback = (True, f"Mandou bem! +{bonus} XP")
    else:
        st.session_state.streak = 0
        st.session_state.feedback = (False, f"A resposta era {question.answer}. Continue: errar faz parte.")


def section_header(kicker: str, title: str, text: str) -> None:
    st.markdown(f'<div class="section-head"><span class="kicker">{kicker}</span><h1>{title}</h1><p>{text}</p></div>', unsafe_allow_html=True)


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown('<div class="brand"><b>%</b> RestoLab</div>', unsafe_allow_html=True)
        page = st.radio("Navegação", PAGES, label_visibility="collapsed")
        st.markdown("---")
        st.markdown("**Seu progresso**")
        st.progress(min(st.session_state.answered / st.session_state.daily_goal, 1.0), text=f"Meta diária · {min(st.session_state.answered, st.session_state.daily_goal)}/{st.session_state.daily_goal}")
        a, b = st.columns(2)
        a.metric("XP", st.session_state.xp)
        b.metric("🔥", st.session_state.streak)
        accuracy = round(100 * st.session_state.correct / st.session_state.answered) if st.session_state.answered else 0
        st.caption(f"Precisão: **{accuracy}%** · Recorde: **{st.session_state.best_streak}**")
        with st.expander("Configurar meta"):
            st.session_state.daily_goal = st.slider("Questões por dia", 3, 20, st.session_state.daily_goal)
        st.markdown('<p class="tiny">Progresso salvo durante esta sessão.</p>', unsafe_allow_html=True)
    return page


def home() -> None:
    st.markdown("""
    <section class="hero"><span class="tag">ACADEMIA DE CONGRUÊNCIAS · DO ZERO AO AVANÇADO</span>
    <h1>Faça as pazes com os <span class="lime">restos.</span></h1>
    <p>Uma jornada completa por divisão euclidiana, aritmética modular, potências, inversos e equações — com prática, experimentos e feedback imediato.</p></section>
    """, unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Pontos de experiência", st.session_state.xp)
    m2.metric("Questões resolvidas", st.session_state.answered)
    m3.metric("Melhor sequência", f"{st.session_state.best_streak} 🔥")
    m4.metric("Aulas concluídas", f"{len(st.session_state.lesson_done)}/{len(LESSONS)}")

    section_header("ROTA RECOMENDADA", "Sua jornada de domínio", "Aprenda, teste a intuição e avance para ferramentas poderosas.")
    left, right = st.columns([1.35, .65])
    with left:
        stages = [("1", "Fundamentos", "Resto, quociente e notação modular"), ("2", "Operações", "Somas, produtos e potências"), ("3", "Estratégia", "Ciclos, divisibilidade e redução"), ("4", "Domínio", "Inversos e equações modulares")]
        done = len(st.session_state.lesson_done)
        for index, (number, title, detail) in enumerate(stages):
            css = "road-dot done" if done >= index * 2 + 2 else "road-dot"
            st.markdown(f'<div class="road"><span class="{css}">{"✓" if "done" in css else number}</span><div><b>{title}</b><div class="tiny">{detail}</div></div></div>', unsafe_allow_html=True)
    with right:
        daily_seed = int(date.today().strftime("%Y%m%d"))
        challenge = generate_question("Difícil", daily_seed)
        st.markdown(f'<div class="dark"><span class="kicker" style="color:#cdf45e">DESAFIO DO DIA</span><h3>{challenge.prompt}</h3><p>{challenge.subtitle}</p><div class="lesson-row">Volte diariamente para um novo desafio.</div></div>', unsafe_allow_html=True)

    section_header("MAPA DO CONTEÚDO", "Tudo o que você vai dominar", "Oito módulos curtos, conectados e progressivos.")
    cols = st.columns(4)
    for index, lesson in enumerate(LESSONS):
        status = "Concluída ✓" if index in st.session_state.lesson_done else lesson["level"]
        cols[index % 4].markdown(f'<div class="card"><span class="icon">{lesson["icon"]}</span><h3>{lesson["title"]}</h3><span class="level">{status}</span><p>{lesson["summary"]}</p></div><br>', unsafe_allow_html=True)


def lessons_page() -> None:
    section_header("8 AULAS ESSENCIAIS", "Trilha de aulas", "Estude no seu ritmo. Cada aula traz conceito, exemplo e uma dica de prova.")
    selected = st.selectbox("Escolha a aula", range(len(LESSONS)), format_func=lambda i: f"{i+1}. {LESSONS[i]['title']}")
    lesson = LESSONS[selected]
    st.progress((selected + 1) / len(LESSONS), text=f"Módulo {selected + 1} de {len(LESSONS)}")
    left, right = st.columns([1.35, .65])
    with left:
        st.markdown(f'<div class="card"><span class="icon">{lesson["icon"]}</span> <span class="level">{lesson["level"]}</span><h2>{lesson["title"]}</h2><p style="font-size:1.04rem">{lesson["body"]}</p><div class="formula">{lesson["example"]}</div></div>', unsafe_allow_html=True)
        st.markdown("#### Fixe a ideia")
        if selected == 0:
            st.info("Experimente com números negativos: em Python, −17 = 5 × (−4) + 3. O resto canônico continua entre 0 e 4.")
        elif selected == 7:
            st.info("O algoritmo de Euclides estendido encontra x e y com ax + my = mdc(a,m). Quando o MDC é 1, x é o inverso de a.")
        else:
            st.info("Explique o exemplo em voz alta e crie outro com números diferentes. Recuperar a ideia da memória fixa mais do que reler.")
    with right:
        st.markdown(f'<div class="dark"><span class="kicker" style="color:#cdf45e">DICA DE OURO</span><h3>Guarde isto</h3><p>{lesson["tip"]}</p></div>', unsafe_allow_html=True)
        completed = selected in st.session_state.lesson_done
        if st.button("✓ Aula concluída" if completed else "Marcar como concluída", disabled=completed, type="primary", use_container_width=True):
            st.session_state.lesson_done.append(selected)
            st.session_state.xp += 20
            st.rerun()
        if selected < len(LESSONS) - 1:
            st.caption(f"A seguir: **{LESSONS[selected+1]['title']}**")


def practice_page() -> None:
    section_header("TREINO ADAPTATIVO", "Arena de prática", "Escolha o nível, resolva sem pressa e aprenda com cada explicação.")
    new_difficulty = st.segmented_control("Dificuldade", ["Fácil", "Médio", "Difícil"], default=st.session_state.difficulty)
    if new_difficulty and new_difficulty != st.session_state.difficulty:
        st.session_state.difficulty = new_difficulty
        next_question()
        st.rerun()
    question = st.session_state.question
    left, right = st.columns([1.4, .6])
    with left:
        st.markdown(f'<div class="quiz"><span class="tag">{question.topic.upper()} · {question.difficulty.upper()}</span><h2>{question.prompt}</h2><p>{question.subtitle}</p></div>', unsafe_allow_html=True)
        choices = st.columns(len(question.choices))
        for col, choice in zip(choices, question.choices):
            col.button(str(choice), key=f"ans_{st.session_state.question_seed}_{choice}", on_click=check_answer, args=(choice,), use_container_width=True)
        if st.session_state.feedback:
            good, message = st.session_state.feedback
            (st.success if good else st.error)(message)
            st.markdown(f"**Resolução:** {question.explanation}")
            if st.button("Próxima questão →", type="primary"):
                next_question()
                st.rerun()
    with right:
        st.markdown("#### Placar da sessão")
        st.metric("Sequência atual", st.session_state.streak)
        accuracy = round(100 * st.session_state.correct / st.session_state.answered) if st.session_state.answered else 0
        st.metric("Precisão", f"{accuracy}%")
        st.markdown('<div class="card"><b>Estratégia universal</b><p>1. Identifique o módulo.<br>2. Reduza cada número.<br>3. Opere com os restos.<br>4. Reduza novamente.</p></div>', unsafe_allow_html=True)


def laboratory_page() -> None:
    section_header("FERRAMENTAS", "Laboratório modular", "Investigue relações, inversos e equações. Cada resultado vem com uma justificativa.")
    compare, inverse, equation = st.tabs(["Comparar números", "Encontrar inverso", "Resolver ax ≡ b"])
    with compare:
        c1, c2, c3 = st.columns(3)
        a = int(c1.number_input("Número a", value=47, step=1, key="compare_a"))
        b = int(c2.number_input("Número b", value=5, step=1, key="compare_b"))
        m = int(c3.number_input("Módulo m", min_value=1, value=7, step=1, key="compare_m"))
        qa, ra = euclidean_division(a, m)
        qb, rb = euclidean_division(b, m)
        if are_congruent(a, b, m):
            st.success(f"Sim! {a} ≡ {b} (mod {m}). Os dois deixam resto {ra}.")
        else:
            st.warning(f"Não: {a} deixa resto {ra}, enquanto {b} deixa resto {rb}.")
        x, y, z = st.columns(3)
        x.metric("Resto de a", ra); y.metric("Resto de b", rb); z.metric("a − b", a - b)
        st.markdown(f'<div class="formula">{a} = {m} × ({qa}) + {ra} &nbsp;&nbsp; | &nbsp;&nbsp; {b} = {m} × ({qb}) + {rb}</div>', unsafe_allow_html=True)
    with inverse:
        c1, c2 = st.columns(2)
        a = int(c1.number_input("Número a", value=3, step=1, key="inv_a"))
        m = int(c2.number_input("Módulo m", min_value=2, value=7, step=1, key="inv_m"))
        inv = modular_inverse(a, m)
        if inv is None:
            st.error(f"{a} não tem inverso módulo {m}, pois mdc({a}, {m}) = {math.gcd(a, m)} ≠ 1.")
        else:
            st.success(f"O inverso é {inv}: {a} × {inv} = {a*inv} ≡ 1 (mod {m}).")
    with equation:
        c1, c2, c3 = st.columns(3)
        a = int(c1.number_input("Coeficiente a", value=4, step=1, key="eq_a"))
        b = int(c2.number_input("Resultado b", value=2, step=1, key="eq_b"))
        m = int(c3.number_input("Módulo m", min_value=2, max_value=500, value=6, step=1, key="eq_m"))
        solutions = solve_linear_congruence(a, b, m)
        if solutions:
            st.success(f"Soluções em 0 ≤ x < {m}: {', '.join(map(str, solutions))}")
            st.caption("Todas as soluções inteiras são congruentes a uma dessas classes módulo m.")
        else:
            st.error(f"Não há solução. O mdc({a}, {m}) = {math.gcd(a,m)} não divide {b}.")


def clock_page() -> None:
    section_header("INTUIÇÃO VISUAL", "Relógio modular", "Veja a contagem dar voltas e pousar em uma classe de resto.")
    c1, c2, c3 = st.columns(3)
    modulus = c1.slider("Quantidade de posições", 3, 16, 12)
    start = c2.slider("Posição inicial", 0, modulus - 1, min(3, modulus - 1))
    jumps = c3.slider("Avanço (aceita negativo)", -40, 80, 15)
    result = (start + jumps) % modulus
    nums = []
    for i in range(modulus):
        angle = 2 * math.pi * i / modulus - math.pi / 2
        left = 50 + 42 * math.cos(angle); top = 50 + 42 * math.sin(angle)
        nums.append(f'<span class="clock-num" style="left:{left}%;top:{top}%;color:{"#d36b28" if i == result else "#234c3b"}">{i}</span>')
    left, right = st.columns([.75, 1.25])
    left.markdown(f'<div class="clock">{"".join(nums)}<span class="clock-center">{result}</span></div>', unsafe_allow_html=True)
    right.markdown(f'<div class="dark"><span class="kicker" style="color:#cdf45e">PASSO A PASSO</span><h2>{start} + ({jumps}) ≡ {result} (mod {modulus})</h2><p>Partimos de {start}, avançamos {jumps} posições e terminamos em {result}. Voltas completas não alteram a posição final.</p><div class="lesson-row">{start + jumps} = {modulus} × ({(start+jumps)//modulus}) + {result}</div></div>', unsafe_allow_html=True)


def tables_page() -> None:
    section_header("PADRÕES À VISTA", "Tabelas de restos", "Explore a estrutura da soma e da multiplicação em diferentes módulos.")
    c1, c2 = st.columns(2)
    modulus = c1.slider("Módulo", 2, 12, 5, key="table_mod")
    operation = c2.segmented_control("Operação", ["+", "×"], default="+") or "+"
    table = residue_table(modulus, operation)
    header = f'<span class="table-cell table-head">{operation}</span>' + ''.join(f'<span class="table-cell table-head">{i}</span>' for i in range(modulus))
    rows = [header]
    for i, row in enumerate(table):
        rows.append(f'<span class="table-cell table-head">{i}</span>' + ''.join(f'<span class="table-cell">{value}</span>' for value in row))
    st.markdown(f'<div style="overflow:auto"><div style="width:{(modulus+1)*36}px">' + '<br>'.join(rows) + '</div></div>', unsafe_allow_html=True)
    if operation == "+":
        st.info("Cada linha é uma rotação da anterior. O zero de cada linha indica o inverso aditivo daquele elemento.")
    else:
        st.info("Procure linhas que contêm 1: a coluna onde ele aparece revela o inverso multiplicativo. Linhas repetidas denunciam divisores de zero.")


def pocket_guide() -> None:
    section_header("COLA HONESTA", "Guia de bolso", "Definições, propriedades, armadilhas e técnicas para consultar quando precisar.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="card"><span class="kicker">DEFINIÇÃO</span><h3>Congruência</h3><div class="formula">a ≡ b (mod m) ⇔ m ∣ (a − b)</div><p>Equivalente: a e b têm o mesmo resto por m.</p></div><br>
        <div class="card"><span class="kicker">PODE FAZER</span><h3>Operações seguras</h3><p>✓ Somar ou subtrair congruências<br>✓ Multiplicar congruências<br>✓ Elevar ambos os lados à mesma potência<br>✓ Trocar um número por seu resto</p></div><br>
        <div class="card"><span class="kicker">ALGORITMO</span><h3>Potências enormes</h3><p>1. Reduza a base.<br>2. Liste potências até repetir.<br>3. Ache o tamanho do ciclo.<br>4. Reduza o expoente pelo ciclo.</p></div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="card"><span class="kicker">CUIDADO</span><h3>Divisão não é automática</h3><p>De ac ≡ bc (mod m), só podemos cancelar c quando mdc(c,m)=1. Caso contrário, soluções podem desaparecer.</p><div class="formula">2x ≡ 2 (mod 6) → x ≡ 1 (mod 3)</div></div><br>
        <div class="card"><span class="kicker">ATALHOS</span><h3>Divisibilidade</h3><p><b>2:</b> último algarismo par<br><b>3 e 9:</b> soma dos algarismos<br><b>4:</b> últimos dois algarismos<br><b>5:</b> termina em 0 ou 5<br><b>11:</b> soma alternada</p></div><br>
        <div class="card"><span class="kicker">VOCABULÁRIO</span><h3>Leia como um matemático</h3><p><b>módulo:</b> tamanho do ciclo<br><b>classe:</b> números com mesmo resto<br><b>representante:</b> um número da classe<br><b>inverso:</b> elemento que produz 1</p></div>
        """, unsafe_allow_html=True)
    st.markdown("#### Conquistas da sessão")
    badges = [
        (st.session_state.answered >= 1, "🎯 Primeiro resto"),
        (st.session_state.correct >= 5, "🧠 Cinco acertos"),
        (st.session_state.best_streak >= 3, "🔥 Em chamas"),
        (len(st.session_state.lesson_done) >= 4, "📚 Meio caminho"),
        (len(st.session_state.lesson_done) == len(LESSONS), "🏆 Mestre modular"),
    ]
    st.markdown("".join(f'<span class="badge" style="opacity:{1 if unlocked else .35}">{label}{" ✓" if unlocked else " 🔒"}</span>' for unlocked, label in badges), unsafe_allow_html=True)


init_state()
page = render_sidebar()
{
    "Início": home,
    "Trilha de aulas": lessons_page,
    "Arena de prática": practice_page,
    "Laboratório": laboratory_page,
    "Relógio modular": clock_page,
    "Tabelas": tables_page,
    "Guia de bolso": pocket_guide,
}[page]()
st.markdown('<footer class="footer"><span>RestoLab · matemática que faz sentido</span><span>Aprenda → experimente → pratique → domine.</span></footer>', unsafe_allow_html=True)
