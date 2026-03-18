import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
from filelock import FileLock

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Java — Condicionais e Seleção",
    page_icon="☕",
    layout="wide"
)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

CSV_PATH = DATA_DIR / "feedback_java_condicionais_v2.csv"
JSONL_PATH = DATA_DIR / "feedback_java_condicionais_v2.jsonl"
LOCK_PATH = DATA_DIR / "feedback_java_condicionais_v2.lock"

STATUS_OPTS = ["✅ Feito", "❌ Não consegui"]
DIF_OPTS = ["Fácil", "Médio", "Difícil"]
HELP_OPTS = ["Não", "Sim"]

TEACHER_PASS = st.secrets.get("app", {}).get("teacher_password", "")

LEVEL_COLORS = {
    "Fácil": "#E8F5E9",
    "Médio": "#FFF8E1",
    "Difícil": "#FBE9E7",
    "Ultra difícil": "#F3E5F5"
}

# =========================
# EXERCÍCIOS
# =========================
EXS = [
    {
        "id": "Ex 1",
        "title": "Verificar se dois números reais são iguais",
        "level": "Fácil",
        "prompt": (
            "Escreva um programa em Java que faça a leitura de dois números reais e "
            "verifique se eles são iguais. Se forem, o programa deve mostrar uma "
            "mensagem ao usuário informando isso. Caso contrário, o programa apenas termina."
        )
    },
    {
        "id": "Ex 2",
        "title": "Comparar dois números inteiros",
        "level": "Fácil",
        "prompt": (
            "Escreva um programa em Java que faça a leitura de 2 números inteiros. "
            "Caso o primeiro seja maior do que o segundo, o programa imprime "
            "“primeiro maior do que o segundo”. Caso contrário, o programa imprime "
            "“segundo maior do que o primeiro”."
        )
    },
    {
        "id": "Ex 3",
        "title": "Mostrar o maior número ou igualdade",
        "level": "Fácil",
        "prompt": (
            "Escreva um programa em Java que peça ao usuário dois números, obtenha os "
            "valores e então imprima o maior número seguido das palavras “é o maior”. "
            "Se os números forem iguais, imprima a mensagem “Estes números são iguais”."
        )
    },
    {
        "id": "Ex 4",
        "title": "Soma, média, produto, menor e maior de três inteiros",
        "level": "Difícil",
        "prompt": (
            "Escreva um programa em Java que leia três números inteiros a partir do teclado "
            "e imprima a soma, a média, o produto, o menor e o maior desses números.(utilizando if)"
        )
    },
    {
        "id": "Ex 5",
        "title": "Saque em conta bancária",
        "level": "Médio",
        "prompt": (
            "Escreva um programa em Java que leia dois valores reais. O primeiro valor é o "
            "saldo de uma conta bancária e o segundo é um valor que o usuário deseja sacar "
            "desta conta. Caso seja possível efetuar o saque (ou seja, o saldo não fique "
            "negativo), o programa deve mostrar o saldo remanescente. Caso contrário, deve "
            "informar o usuário que não foi possível realizar o saque."
        )
    },
    {
        "id": "Ex 6",
        "title": "Compra de roupa com opções de pagamento",
        "level": "Difícil",
        "prompt": (
            "Faça um programa em Java que leia um valor real, representando o valor de uma "
            "peça de roupa. A seguir, o programa deve ler um inteiro (0, 1 ou 2), os quais "
            "representam as seguintes opções:\n\n"
            "0 – Compra à vista\n"
            "1 – Compra parcelada no cartão\n"
            "2 – Crediário\n\n"
            "Na opção 0, o programa deve calcular quanto custa a peça de roupa com 10% de desconto.\n"
            "Na opção 1, o programa deve perguntar ao usuário quantas parcelas deseja utilizar "
            "e exibir o valor da parcela.\n"
            "Na opção 2, o usuário pagará juros de 10% sobre o valor total. O programa deve ler "
            "o número de parcelas desejado e exibir o valor de cada parcela, calculado sobre o valor com juros.\n"
            "Caso o usuário digite alguma opção diferente de 0, 1 ou 2, o programa deve informar "
            "“opção inválida” e terminar."
        )
    },
    {
        "id": "Ex 7",
        "title": "Par ou ímpar e positivo ou negativo",
        "level": "Médio",
        "prompt": (
            "Escreva um programa em Java que leia um número inteiro e informe:\n"
            "- se ele é par ou ímpar\n"
            "- e se ele é positivo, negativo ou zero.\n\n"
            "O programa deve exibir as duas classificações."
        )
    },
    {
        "id": "Ex 8",
        "title": "Maior de três números",
        "level": "Médio",
        "prompt": (
            "Escreva um programa em Java que leia três números inteiros e mostre qual deles "
            "é o maior. Caso existam valores iguais entre os maiores, o programa pode informar "
            "que há empate entre os maiores."
        )
    },
    {
        "id": "Ex 9",
        "title": "Classificação por faixa etária",
        "level": "Médio",
        "prompt": (
            "Escreva um programa em Java que leia a idade de uma pessoa e classifique-a em uma "
            "das seguintes categorias:\n"
            "- Criança: 0 a 12 anos\n"
            "- Adolescente: 13 a 17 anos\n"
            "- Adulto: 18 a 59 anos\n"
            "- Idoso: 60 anos ou mais\n\n"
            "Caso a idade seja negativa, o programa deve informar “idade inválida”."
        )
    },
    {
        "id": "Ex 10",
        "title": "Cálculo de IMC com classificação",
        "level": "Difícil",
        "prompt": (
            "Escreva um programa em Java que leia o peso (em kg) e a altura (em metros) de uma "
            "pessoa, calcule o IMC e exiba também a sua classificação:\n"
            "- Abaixo do peso: IMC < 18.5\n"
            "- Peso normal: 18.5 <= IMC < 25\n"
            "- Sobrepeso: 25 <= IMC < 30\n"
            "- Obesidade: IMC >= 30"
        )
    },
    {
        "id": "Ex 11",
        "title": "Aprovação do aluno com recuperação",
        "level": "Difícil",
        "prompt": (
            "Escreva um programa em Java que leia duas notas de um aluno. Calcule a média.\n"
            "- Se a média for maior ou igual a 7, informe “Aprovado”.\n"
            "- Se a média for menor que 4, informe “Reprovado”.\n"
            "- Caso contrário, informe “Recuperação”.\n\n"
            "Se o aluno ficar em recuperação, o programa deve ler a nota da recuperação e "
            "calcular a nova média entre a média inicial e a nota da recuperação. "
            "Se essa nova média for maior ou igual a 5, informe “Aprovado após recuperação”; "
            "caso contrário, informe “Reprovado após recuperação”."
        )
    },
    {
        "id": "Ex 12",
        "title": "Calculadora com switch",
        "level": "Difícil",
        "prompt": (
            "Escreva um programa em Java que leia dois números reais e depois uma operação "
            "desejada pelo usuário (+, -, * ou /). Utilize uma estrutura de seleção para "
            "calcular e exibir o resultado.\n\n"
            "Regras:\n"
            "- Caso a operação seja inválida, informe “operação inválida”.\n"
            "- Caso o usuário tente dividir por zero, informe “não é possível dividir por zero”."
        )
    },
    {
        "id": "Ex 13",
        "title": "Tarifa de estacionamento por faixa e tempo",
        "level": "Ultra difícil",
        "prompt": (
            "Escreva um programa em Java que leia o número de horas que um veículo permaneceu "
            "em um estacionamento e o tipo do veículo:\n"
            "1 - Moto\n"
            "2 - Carro\n"
            "3 - Caminhonete\n\n"
            "Tabela de cobrança:\n"
            "- Até 2 horas: Moto = R$ 5/h, Carro = R$ 8/h, Caminhonete = R$ 10/h\n"
            "- De 3 a 5 horas: Moto = R$ 4/h, Carro = R$ 7/h, Caminhonete = R$ 9/h\n"
            "- Acima de 5 horas: Moto = R$ 3/h, Carro = R$ 6/h, Caminhonete = R$ 8/h\n\n"
            "O programa deve calcular e exibir o valor total a pagar.\n"
            "Caso o tipo de veículo seja inválido ou a quantidade de horas seja menor ou igual a zero, "
            "o programa deve informar “dados inválidos”."
        )
    },
    {
        "id": "Ex 14",
        "title": "Reajuste salarial por faixa e tempo de empresa",
        "level": "Ultra difícil",
        "prompt": (
            "Escreva um programa em Java que leia o salário atual de um funcionário e a quantidade "
            "de anos que ele trabalha na empresa.\n\n"
            "Regras de reajuste:\n"
            "- Salário até R$ 2000,00: reajuste base de 12%\n"
            "- Salário acima de R$ 2000,00 até R$ 5000,00: reajuste base de 8%\n"
            "- Salário acima de R$ 5000,00: reajuste base de 5%\n\n"
            "Bônus por tempo de empresa:\n"
            "- Menos de 3 anos: sem bônus\n"
            "- De 3 a 10 anos: +2%\n"
            "- Acima de 10 anos: +5%\n\n"
            "O programa deve calcular e exibir o novo salário com o reajuste total.\n"
            "Se algum valor informado for inválido, exiba “dados inválidos”."
        )
    },
    {
        "id": "Ex 15",
        "title": "Conta de energia com bandeira tarifária",
        "level": "Ultra difícil",
        "prompt": (
            "Escreva um programa em Java que leia o consumo mensal de energia elétrica em kWh "
            "e o tipo de bandeira tarifária:\n"
            "1 - Verde\n"
            "2 - Amarela\n"
            "3 - Vermelha\n\n"
            "Valor base por faixa de consumo:\n"
            "- Até 100 kWh: R$ 0,50 por kWh\n"
            "- De 101 a 200 kWh: R$ 0,70 por kWh\n"
            "- Acima de 200 kWh: R$ 0,90 por kWh\n\n"
            "Adicionais da bandeira:\n"
            "- Verde: sem adicional\n"
            "- Amarela: +R$ 15,00\n"
            "- Vermelha: +R$ 30,00\n\n"
            "O programa deve calcular e exibir o valor final da conta.\n"
            "Caso o consumo seja inválido ou a bandeira não exista, o programa deve informar “dados inválidos”."
        )
    },
    {
        "id": "Ex 16",
        "title": "Sistema de venda com cupom e frete",
        "level": "Ultra difícil",
        "prompt": (
            "Escreva um programa em Java que leia:\n"
            "- o valor total de uma compra\n"
            "- o tipo de cliente: 1 = comum, 2 = premium\n"
            "- se possui cupom de desconto: S ou N\n\n"
            "Regras:\n"
            "- Cliente comum: sem desconto fixo\n"
            "- Cliente premium: 10% de desconto\n"
            "- Se tiver cupom (S), aplicar mais 5% de desconto sobre o valor já ajustado\n"
            "- Se o valor final da compra for menor que R$ 100,00, cobrar frete de R$ 20,00\n"
            "- Caso contrário, frete grátis\n\n"
            "O programa deve exibir:\n"
            "- valor original\n"
            "- valor após descontos\n"
            "- valor do frete\n"
            "- valor final a pagar\n\n"
            "Caso algum dado seja inválido, exiba “dados inválidos”."
        )
    },
]

LEVELS = ["Fácil", "Médio", "Difícil", "Ultra difícil"]

# =========================
# ESTILO
# =========================
st.markdown("""
<style>
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}
.exercise-card {
    border-radius: 16px;
    padding: 18px 20px;
    margin-bottom: 12px;
    border: 1px solid rgba(49, 51, 63, 0.15);
}
.exercise-title {
    font-size: 1.15rem;
    font-weight: 700;
    margin-bottom: 6px;
}
.exercise-meta {
    font-size: 0.92rem;
    margin-bottom: 10px;
    opacity: 0.85;
}
.small-note {
    font-size: 0.9rem;
    opacity: 0.8;
}
</style>
""", unsafe_allow_html=True)

# =========================
# PERSISTÊNCIA
# =========================
def append_submission(row: dict):
    with FileLock(str(LOCK_PATH)):
        with open(JSONL_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

        df_new = pd.DataFrame([row])
        if CSV_PATH.exists():
            df_old = pd.read_csv(CSV_PATH)
            df = pd.concat([df_old, df_new], ignore_index=True)
        else:
            df = df_new

        df.to_csv(CSV_PATH, index=False)


def load_df() -> pd.DataFrame:
    if not CSV_PATH.exists():
        return pd.DataFrame(columns=[
            "timestamp",
            "student_names",
            "exercise_id",
            "exercise_title",
            "exercise_level",
            "status",
            "difficulty",
            "needed_help",
            "comment",
            "java_code"
        ])
    return pd.read_csv(CSV_PATH)


# =========================
# AUTH PROFESSOR
# =========================
def teacher_is_enabled() -> bool:
    return bool(TEACHER_PASS)


def teacher_is_logged() -> bool:
    return st.session_state.get("teacher_ok", False) is True


def teacher_login_ui():
    st.sidebar.subheader("🔐 Professor")

    if not teacher_is_enabled():
        st.sidebar.info("Modo professor desativado.")
        return

    if "teacher_ok" not in st.session_state:
        st.session_state["teacher_ok"] = False

    if teacher_is_logged():
        st.sidebar.success("Logado ✅")
        if st.sidebar.button("Sair", use_container_width=True):
            st.session_state["teacher_ok"] = False
            st.rerun()
    else:
        pwd = st.sidebar.text_input("Senha", type="password", key="teacher_pwd_sidebar")
        if st.sidebar.button("Entrar", use_container_width=True):
            st.session_state["teacher_ok"] = (pwd == TEACHER_PASS)
            st.rerun()


# =========================
# HELPERS
# =========================
def get_exercise_by_option(option_text: str):
    for ex in EXS:
        full = f"{ex['id']} — {ex['title']} [{ex['level']}]"
        if full == option_text:
            return ex
    return None


def render_exercise_card(ex):
    bg = LEVEL_COLORS.get(ex["level"], "#F5F5F5")
    st.markdown(
        f"""
        <div class="exercise-card" style="background:{bg};">
            <div class="exercise-title">{ex["id"]} — {ex["title"]}</div>
            <div class="exercise-meta"><b>Nível:</b> {ex["level"]}</div>
            <div>{ex["prompt"].replace(chr(10), "<br>")}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def difficulty_score(value: str) -> int:
    mapping = {"Fácil": 1, "Médio": 2, "Difícil": 3}
    return mapping.get(str(value), 0)


# =========================
# SIDEBAR
# =========================
teacher_login_ui()

st.sidebar.divider()
if teacher_is_logged():
    view = st.sidebar.radio("📌 Menu", ["Aluno", "Professor"], index=0)
else:
    view = "Aluno"
    st.sidebar.radio("📌 Menu", ["Aluno"], index=0, disabled=True)

st.sidebar.divider()
st.sidebar.markdown("### ☕ Aula")
st.sidebar.caption("Condicionais, if/else, else if e switch em Java.")

# =========================
# MAIN
# =========================
st.title("☕ Exercícios de Java — Condicionais e Estruturas de Seleção")
st.caption("Registre como a turma está respondendo aos exercícios da aula.")

if view == "Aluno":
    colA, colB = st.columns([1.2, 1.8])

    with colA:
        st.subheader("👤 Identificação")
        student_names = st.text_input(
            "Nome do aluno ou nomes da dupla",
            placeholder="Ex: Ana Silva ou Ana Silva e Bruno Souza",
            key="student_names"
        )

        level_filter = st.selectbox(
            "Filtrar exercícios por nível",
            ["(Todos)"] + LEVELS,
            key="student_level_filter"
        )

        if level_filter == "(Todos)":
            ex_list = EXS
        else:
            ex_list = [e for e in EXS if e["level"] == level_filter]

        options = [f"{e['id']} — {e['title']} [{e['level']}]" for e in ex_list]

        selected = st.selectbox(
            "📌 Escolha o exercício",
            options,
            key="exercise_select"
        )

        ex = get_exercise_by_option(selected)

        st.markdown("<div class='small-note'>Dica: o aluno pode colar abaixo o código Java produzido.</div>", unsafe_allow_html=True)

    with colB:
        render_exercise_card(ex)

    st.markdown("### ✅ Registro do aluno/grupo")

    with st.form(key=f"form_{ex['id']}", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)

        with c1:
            status = st.radio(
                "Você conseguiu fazer?",
                STATUS_OPTS,
                key=f"status_{ex['id']}"
            )

        with c2:
            difficulty = st.radio(
                "Dificuldade percebida",
                DIF_OPTS,
                key=f"difficulty_{ex['id']}"
            )

        with c3:
            needed_help = st.radio(
                "Precisou de ajuda?",
                HELP_OPTS,
                key=f"help_{ex['id']}"
            )

        comment = st.text_area(
            "Comentário",
            height=100,
            placeholder="Ex: entendi a lógica, mas tive dificuldade no switch / consegui com ajuda / travei na comparação...",
            key=f"comment_{ex['id']}"
        )

        java_code = st.text_area(
            "Cole aqui o código Java (opcional)",
            height=220,
            placeholder="public class Main {\n    public static void main(String[] args) {\n        // seu código aqui\n    }\n}",
            key=f"code_{ex['id']}"
        )

        submitted = st.form_submit_button("💾 Salvar registro", use_container_width=True)

    if submitted:
        if not student_names.strip():
            st.warning("Preencha o campo de identificação antes de salvar.")
        else:
            row = {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "student_names": student_names.strip(),
                "exercise_id": ex["id"],
                "exercise_title": ex["title"],
                "exercise_level": ex["level"],
                "status": status,
                "difficulty": difficulty,
                "needed_help": needed_help,
                "comment": (comment or "").strip(),
                "java_code": (java_code or "").strip(),
            }
            append_submission(row)
            st.success("Registro salvo com sucesso ✅")

elif view == "Professor":
    st.subheader("📊 Painel do Professor")

    df = load_df()

    st.markdown("### 🧨 Administração")
    with st.expander("Limpar respostas (apagar tudo)"):
        st.warning("Isso apaga TODOS os registros salvos. Não é possível desfazer.")
        confirm = st.checkbox("Confirmo que quero apagar todos os registros", key="confirm_delete_all")

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🗑️ Limpar respostas agora", use_container_width=True, disabled=not confirm):
                try:
                    if CSV_PATH.exists():
                        CSV_PATH.unlink()
                    if JSONL_PATH.exists():
                        JSONL_PATH.unlink()
                    if LOCK_PATH.exists():
                        LOCK_PATH.unlink()
                    st.success("Respostas apagadas com sucesso ✅")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao apagar arquivos: {e}")
        with col2:
            st.caption("Use no encerramento da aula ou antes de uma nova turma.")

    if df.empty:
        st.warning("Ainda não há registros salvos.")
    else:
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            ex_sel = st.selectbox("Filtrar por exercício", ["(Todos)"] + [e["id"] for e in EXS], key="prof_ex_filter")
        with f2:
            level_sel = st.selectbox("Filtrar por nível", ["(Todos)"] + LEVELS, key="prof_level_filter")
        with f3:
            status_sel = st.selectbox("Filtrar por status", ["(Todos)"] + STATUS_OPTS, key="prof_status_filter")
        with f4:
            last_n = st.slider("Mostrar últimos N", 20, 5000, 300, key="prof_last_n")

        dff = df.copy()

        if ex_sel != "(Todos)":
            dff = dff[dff["exercise_id"].astype(str) == ex_sel]
        if level_sel != "(Todos)":
            dff = dff[dff["exercise_level"].astype(str) == level_sel]
        if status_sel != "(Todos)":
            dff = dff[dff["status"].astype(str) == status_sel]

        if "timestamp" in dff.columns:
            dff = dff.sort_values("timestamp", ascending=False)

        total = len(dff)
        feito = int((dff["status"] == "✅ Feito").sum())
        nao = int((dff["status"] == "❌ Não consegui").sum())
        ajuda = int((dff["needed_help"] == "Sim").sum()) if "needed_help" in dff.columns else 0

        perc_feito = (feito / total) * 100 if total else 0
        perc_ajuda = (ajuda / total) * 100 if total else 0

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Registros", total)
        k2.metric("✅ Feito", feito)
        k3.metric("% Feito", f"{perc_feito:.1f}%")
        k4.metric("% com ajuda", f"{perc_ajuda:.1f}%")

        st.markdown("#### 📈 Distribuições")
        g1, g2, g3 = st.columns(3)

        with g1:
            st.caption("Status")
            st.bar_chart(dff["status"].value_counts())

        with g2:
            st.caption("Dificuldade percebida")
            dif_series = dff["difficulty"].value_counts().reindex(DIF_OPTS).fillna(0)
            st.bar_chart(dif_series)

        with g3:
            st.caption("Precisou de ajuda?")
            if "needed_help" in dff.columns:
                help_series = dff["needed_help"].value_counts().reindex(HELP_OPTS).fillna(0)
                st.bar_chart(help_series)

        st.markdown("#### 🧩 Resumo por exercício")
        resumo = (
            dff.groupby(["exercise_id", "exercise_title", "exercise_level"], dropna=False)
            .agg(
                registros=("exercise_id", "count"),
                feito=("status", lambda s: (s == "✅ Feito").sum()),
                nao_consegui=("status", lambda s: (s == "❌ Não consegui").sum()),
                com_ajuda=("needed_help", lambda s: (s == "Sim").sum() if len(s) else 0),
            )
            .reset_index()
        )

        resumo["% feito"] = ((resumo["feito"] / resumo["registros"]) * 100).round(1)
        resumo["% com ajuda"] = ((resumo["com_ajuda"] / resumo["registros"]) * 100).round(1)

        st.dataframe(
            resumo.sort_values(["exercise_id"]),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("#### 🔥 Ranking dos exercícios com maior dificuldade percebida")
        ranking = dff.copy()
        ranking["difficulty_points"] = ranking["difficulty"].apply(difficulty_score)

        ranking_df = (
            ranking.groupby(["exercise_id", "exercise_title", "exercise_level"], dropna=False)
            .agg(
                registros=("exercise_id", "count"),
                media_dificuldade=("difficulty_points", "mean")
            )
            .reset_index()
        )

        ranking_df["media_dificuldade"] = ranking_df["media_dificuldade"].round(2)
        ranking_df = ranking_df.sort_values(
            ["media_dificuldade", "registros"],
            ascending=[False, False]
        )

        st.dataframe(
            ranking_df,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("#### 💬 Comentários dos alunos")
        comments_df = dff.copy()
        comments_df["comment"] = comments_df["comment"].fillna("").astype(str).str.strip()
        comments_df = comments_df[comments_df["comment"] != ""]

        if comments_df.empty:
            st.info("Ainda não há comentários registrados.")
        else:
            st.dataframe(
                comments_df[[
                    "timestamp", "student_names", "exercise_id",
                    "exercise_title", "difficulty", "needed_help", "comment"
                ]].head(last_n),
                use_container_width=True,
                hide_index=True
            )

        st.markdown("#### 💻 Códigos enviados")
        code_df = dff.copy()
        code_df["java_code"] = code_df["java_code"].fillna("").astype(str).str.strip()
        code_df = code_df[code_df["java_code"] != ""]

        if code_df.empty:
            st.info("Ainda não há códigos Java enviados.")
        else:
            code_view = st.selectbox(
                "Selecione um envio para visualizar o código",
                code_df.apply(
                    lambda row: f"{row['timestamp']} | {row['student_names']} | {row['exercise_id']} — {row['exercise_title']}",
                    axis=1
                ).tolist(),
                key="selected_code_view"
            )

            selected_row = code_df.iloc[
                code_df.apply(
                    lambda row: f"{row['timestamp']} | {row['student_names']} | {row['exercise_id']} — {row['exercise_title']}",
                    axis=1
                ).tolist().index(code_view)
            ]

            st.code(selected_row["java_code"], language="java")

        st.markdown("#### 🧾 Registros")
        st.dataframe(
            dff.head(last_n),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("#### ⬇️ Download")
        st.download_button(
            "Baixar CSV filtrado",
            data=dff.to_csv(index=False).encode("utf-8"),
            file_name="feedback_java_condicionais_filtrado.csv",
            mime="text/csv",
            use_container_width=True
        )

        if CSV_PATH.exists():
            st.download_button(
                "Baixar CSV completo",
                data=CSV_PATH.read_bytes(),
                file_name="feedback_java_condicionais_completo.csv",
                mime="text/csv",
                use_container_width=True
            )
