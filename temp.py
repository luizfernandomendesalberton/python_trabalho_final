from datetime import datetime, timedelta

# -------------------------
# Classes Principais
# -------------------------

class Livro:
    def __init__(self, titulo, autor, ano, disponivel = True):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.disponivel = disponivel

    def __str__(self):
        status = "Disponível" if self.disponivel else "Emprestado"
        return f"{self.titulo} - {self.autor} ({self.ano}) [{status}]"


class Usuario:
    def __init__(self, nome, matricula):
        self.nome = nome
        self.matricula = matricula
        self.historico = []  # lista de objetos Emprestimo

    def __str__(self):
        return f"👤 {self.nome} (Matrícula: {self.matricula})"


class Emprestimo:
    def __init__(self, livro: Livro, usuario: Usuario, dias: int = 7):
        self.livro = livro
        self.usuario = usuario
        self.data_emprestimo = datetime.now()
        self.data_devolucao = self.data_emprestimo + timedelta(days=dias)
        self.devolvido = False
        self.data_devolvido = None

    def marcar_devolvido(self):
        if self.devolvido:
            return False
        self.devolvido = True
        self.data_devolvido = datetime.now()
        return True

    def esta_atrasado(self):
        return (not self.devolvido) and (datetime.now() > self.data_devolucao)

    def __str__(self):
        status = "Devolvido" if self.devolvido else "Em aberto"
        devolucao = self.data_devolucao.strftime("%d/%m/%Y")
        emprest = self.data_emprestimo.strftime("%d/%m/%Y")
        return (f"{self.livro.titulo} | Usuário: {self.usuario.nome} | "
                f"Empréstimo: {emprest} | Devolução: {devolucao} | {status}")


# -------------------------
# Base de Dados em Memória
# -------------------------

livros: list[Livro] = []
usuarios: list[Usuario] = []
emprestimos: list[Emprestimo] = []


# -------------------------
# Helpers de UX / Validação
# -------------------------

def pause():
    input("\nPressione Enter para continuar...")


def validar_indice(lista, indice):
    """Retorna item se índice for válido, senão None."""
    try:
        if indice < 0 or indice >= len(lista):
            return None
        return lista[indice]
    except Exception:
        return None


# -------------------------
# Funções do Sistema
# -------------------------

def cadastrar_livro():
    titulo = input("Título do livro: ").strip()
    if not titulo:
        print("Título não pode ser vazio.")
        pause()
        return
    autor = input("Autor: ").strip() or "Desconhecido"
    ano = input("Ano de publicação: ").strip() or "N/A"
    livros.append(Livro(titulo, autor, ano))
    print("Livro cadastrado com sucesso!")
    pause()


def listar_livros():
    if not livros:
        print("Nenhum livro cadastrado.")
        return
    print("\n=== LIVROS CADASTRADOS ===")
    for i, livro in enumerate(livros, 1):
        print(f"{i}. {livro}")


def editar_livro():
    listar_livros()
    if not livros:
        pause()
        return
    try:
        indice = int(input("Número do livro para editar: ")) - 1
    except ValueError:
        print("Opção inválida.")
        pause()
        return

    livro = validar_indice(livros, indice)
    if livro is None:
        print("Livro não encontrado.")
        pause()
        return

    novo_titulo = input(
        f"Novo título ({livro.titulo}): ").strip() or livro.titulo
    novo_autor = input(f"Novo autor ({livro.autor}): ").strip() or livro.autor
    novo_ano = input(f"Novo ano ({livro.ano}): ").strip() or livro.ano

    livro.titulo = novo_titulo
    livro.autor = novo_autor
    livro.ano = novo_ano

    print("Livro atualizado com sucesso!")
    pause()


def remover_livro():
    listar_livros()
    if not livros:
        pause()
        return
    try:
        indice = int(input("🗑 Número do livro para remover: ")) - 1
    except ValueError:
        print("Opção inválida.")
        pause()
        return

    livro = validar_indice(livros, indice)
    if livro is None:
        print("Livro não encontrado.")
        pause()
        return

    if not livro.disponivel:
        print("❌ Este livro está emprestado e não pode ser removido.")
        pause()
        return

    removido = livros.pop(indice)
    print(f"Livro '{removido.titulo}' removido com sucesso!")
    pause()


def cadastrar_usuario():
    nome = input("Nome do usuário: ").strip()
    if not nome:
        print("Nome não pode ser vazio.")
        pause()
        return
    matricula = input("Matrícula: ").strip()
    if not matricula:
        print("Matrícula não pode ser vazia.")
        pause()
        return

    if any(u.matricula == matricula for u in usuarios):
        print("Já existe usuário com esta matrícula.")
        pause()
        return

    usuarios.append(Usuario(nome, matricula))
    print("Usuário cadastrado com sucesso!")
    pause()


def listar_usuarios():
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    print("\n=== USUÁRIOS CADASTRADOS ===")
    for i, u in enumerate(usuarios, 1):
        print(f"{i}. {u}")


def realizar_emprestimo():
    listar_usuarios()
    if not usuarios:
        pause()
        return
    try:
        idx_user = int(input("👤 Escolha o número do usuário: ")) - 1
    except ValueError:
        print("Usuário inválido.")
        pause()
        return

    usuario = validar_indice(usuarios, idx_user)
    if usuario is None:
        print("Usuário inválido.")
        pause()
        return

    listar_livros()
    if not livros:
        pause()
        return
    try:
        idx_livro = int(input("📚 Escolha o número do livro: ")) - 1
    except ValueError:
        print("Livro inválido.")
        pause()
        return

    livro = validar_indice(livros, idx_livro)
    if livro is None:
        print("Livro inválido.")
        pause()
        return

    if not livro.disponivel:
        print("Livro já emprestado!")
        pause()
        return

    emprestimo = Emprestimo(livro, usuario)
    emprestimos.append(emprestimo)
    usuario.historico.append(emprestimo)
    livro.disponivel = False

    print(f"Empréstimo realizado! Devolução até {emprestimo.data_devolucao.strftime('%d/%m/%Y')}.")
    pause()


def devolver_livro():
    listar_usuarios()
    if not usuarios:
        pause()
        return
    try:
        idx_user = int(input("Usuário que está devolvendo (número): ")) - 1
    except ValueError:
        print("Usuário inválido.")
        pause()
        return

    usuario = validar_indice(usuarios, idx_user)
    if usuario is None:
        print("Usuário inválido.")
        pause()
        return

    emprestimos_ativos = [e for e in usuario.historico if not e.devolvido]
    if not emprestimos_ativos:
        print("Nenhum empréstimo ativo para este usuário.")
        pause()
        return

    print("\n=== EMPRÉSTIMOS ATIVOS ===")
    for i, e in enumerate(emprestimos_ativos, 1):
        atraso = " ⏰ ATRASADO" if e.esta_atrasado() else ""
        print(f"{i}. {e} {atraso}")

    try:
        idx_emp = int(
            input("Escolha o número do empréstimo para devolver: ")) - 1
    except ValueError:
        print("Opção inválida.")
        pause()
        return

    emprestimo = validar_indice(emprestimos_ativos, idx_emp)
    if emprestimo is None:
        print("Empréstimo inválido.")
        pause()
        return

    if emprestimo.devolvido:
        print("Este empréstimo já foi devolvido.")
        pause()
        return

    emprestimo.marcar_devolvido()
    emprestimo.livro.disponivel = True

    print("Livro devolvido com sucesso!")
    pause()


def historico_usuario():
    listar_usuarios()
    if not usuarios:
        pause()
        return
    try:
        idx_user = int(input("Escolha o número do usuário: ")) - 1
    except ValueError:
        print("Usuário inválido.")
        pause()
        return

    usuario = validar_indice(usuarios, idx_user)
    if usuario is None:
        print("Usuário inválido.")
        pause()
        return

    if not usuario.historico:
        print("Nenhum histórico encontrado para este usuário.")
        pause()
        return

    print(f"\n=== HISTÓRICO DE {usuario.nome} ===")
    for h in usuario.historico:
        atraso = " ⏰ ATRASADO" if h.esta_atrasado() else ""
        if h.devolvido:
            devolv_str = f"Devolvido em {h.data_devolvido.strftime('%d/%m/%Y')}"
        else:
            devolv_str = f"Devolver até {h.data_devolucao.strftime('%d/%m/%Y')}"
        print(
            f"- {h.livro.titulo} | {devolv_str} | Status: {'Devolvido' if h.devolvido else 'Em aberto'}{atraso}")
    pause()


# -------------------------
# Menu Principal
# -------------------------

def menu():
    while True:
        print("""
=================  SISTEMA DE BIBLIOTECA =================
1️⃣  Cadastrar novo livro
2️⃣  Listar livros
3️⃣  Editar livro
4️⃣  Remover livro
5️⃣  Cadastrar usuário
6️⃣  Listar usuários
7️⃣  Realizar empréstimo
8️⃣  Devolver livro
9️⃣  Ver histórico de usuário
0️⃣  Sair
============================================================
""")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1": cadastrar_livro()
        elif opcao == "2": listar_livros(), pause()
        elif opcao == "3": editar_livro()
        elif opcao == "4": remover_livro()
        elif opcao == "5": cadastrar_usuario()
        elif opcao == "6": listar_usuarios(), pause()
        elif opcao == "7": realizar_emprestimo()
        elif opcao == "8": devolver_livro()
        elif opcao == "9": historico_usuario()
        elif opcao == "0":
            print("Saindo do sistema... Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")
            pause()


# -------------------------
# Execução
# -------------------------

if __name__ == "__main__":
    print("\nBem-vindo ao Sistema de Biblioteca! ✨\n")
    menu()
