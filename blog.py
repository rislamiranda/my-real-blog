import streamlit as st
import os
import re
from datetime import datetime

# Configuração da página do Streamlit
st.set_page_config(page_title="Risla Miranda", layout="centered")

# Função para listar arquivos de posts na pasta 'posts'
def get_post_files():
    return [f for f in os.listdir("posts") if f.endswith(".md")]

# Função para carregar a data, título, e conteúdo de um arquivo Markdown
def load_post(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    
    # Extrair a data do post (formato: <!-- Data: YYYY-MM-DD -->)
    date_match = re.search(r"<!-- Data: (\d{4}-\d{2}-\d{2}) -->", content)
    date = date_match.group(1) if date_match else "2020-01-01"  # Data padrão, se não houver data
    date = datetime.strptime(date, "%Y-%m-%d").date()
    
    # Extrair o título (primeira linha que começa com '#')
    title_match = re.search(r"^# (.+)", content, re.MULTILINE)
    title = title_match.group(1) if title_match else "Sem título"

    # Remover a linha da data do conteúdo principal
    content = re.sub(r"<!-- Data: \d{4}-\d{2}-\d{2} -->", "", content)
    
    return date, content

# Carregar os posts e ordenar pela data
posts = []
for filename in get_post_files():
    date, content = load_post(os.path.join("posts", filename))
    posts.append((filename, date, content))

# Ordenar os posts pela data (do mais recente para o mais antigo)
posts.sort(reverse=True, key=lambda x: x[1])

# Inicializar estado da sessão para controlar exibição
if "selected_post" not in st.session_state:
    st.session_state["selected_post"] = None

# Página principal ou exibição de post
if st.session_state["selected_post"] is None:
    # Página principal: título, mini bio, e lista de posts
    st.title("Risla Miranda")
    st.markdown("""
    👋 **Bem-vindo ao meu site!**  
    Sou cientista de dados no Ministério da Gestão e da Inovação em Serviços Públicos. Sou servidora pública federal desde 2013! Sou economista, com mestrado em direitos humanos, e meu maior interesse é ciência de dados aplicada a políticas públicas e a direitos humanos.  
    Você pode me encontrar no [LinkedIn](https://www.linkedin.com/in/rislamiranda/) e no [GitHub](https://github.com/rislamiranda). Também pesquiso e escrevo sobre audiovisual e gênero no [Arte Aberta](https://arteaberta.com).
    """)
    st.header("Posts")

    # Exibir lista de posts na página principal
    for filename, date, content in posts:
        title_match = re.search(r"^# (.+)", content, re.MULTILINE)
        title = title_match.group(1) if title_match else "Sem título"
        if st.button(f"{title} ({date})"):
            st.session_state["selected_post"] = filename

    # Sidebar para selecionar post
    selected_title = st.sidebar.selectbox("Escolha um post", ["Selecione um post"] + [re.search(r"^# (.+)", content, re.MULTILINE).group(1) for _, _, content in posts])

    # Verificar se um post foi selecionado no sidebar
    if selected_title != "Selecione um post":
        # Encontra o arquivo correspondente ao título selecionado
        selected_filename = next(filename for filename, _, content in posts if re.search(r"^# (.+)", content, re.MULTILINE).group(1) == selected_title)
        st.session_state["selected_post"] = selected_filename

else:
    # Página de leitura do post selecionado
    selected_filename = st.session_state["selected_post"]
    for filename, date, content in posts:
        if filename == selected_filename:
            # Exibir a data e o conteúdo diretamente, sem adicionar título
            st.markdown(f"**Publicado em: {date}**\n\n{content}")
    
    # Botão para retornar à página principal
    if st.button("Voltar à lista de posts"):
        st.session_state["selected_post"] = None