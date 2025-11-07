
#  Sistema de Biblioteca - Versão Premium by Luiz Mendes


from datetime import datetime, timedelta


#  Classes Principais

class Livro:
    def __init__(self, titulo, autor, ano):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.disponivel = True

    def __str__(self):
        status = " Disponível" if self.disponivel else "❌ Emprestado"
        return f" {self.titulo} - {self.autor} ({self.ano}) [{status}]"


class Usuario:
    def __init__(self, nome, matricula):
        self.nome = nome
        self.matricula = matricula
        self.historico = []

    def __str__(self):
        return f"👤 {self.nome} (Matrícula: {self.matricula})"


class Emprestimo:
    def __init__(self, livro, usuario):
        self.livro = livro
        self.usuario = usuario
        self.data_emprestimo = datetime.now()
        self.data_devolucao = self.data_emprestimo + timedelta(days=7)
        self.devolvido = False

    def __str__(self):
        status = " Devolvido" if self.devolvido else " Em aberto"
        return (f" {self.livro.titulo} | Usuário: {self.usuario.nome} | "
                f"Empréstimo: {self.data_emprestimo.strftime('%d/%m/%Y')} | "
                f"Devolução: {self.data_devolucao.strftime('%d/%m/%Y')} | {status}")



#  Base de Dados em Memória

livros = []
usuarios = []
emprestimos = []


#  Funções do Sistema

def cadastrar_livro():
    titulo = input(" Título do livro: ")
    autor = input(" Autor: ")
    ano = input(" Ano de publicação: ")
    livros.append(Livro(titulo, autor, ano))
    print(" Livro cadastrado com sucesso!\n")


def listar_livros():
    if not livros:
        print(" Nenhum livro cadastrado.\n")
        return
    print("\n===  LIVROS CADASTRADOS ===")
    for i, livro in enumerate(livros, 1):
        print(f"{i}. {livro}")
    print()


def editar_livro():
    listar_livros()
    if not livros: return
    try:
        indice = int(input(" Número do livro para editar: ")) - 1
        livro = livros[indice]
        livro.titulo = input(f"Novo título ({livro.titulo}): ") or livro.titulo
        livro.autor = input(f"Novo autor ({livro.autor}): ") or livro.autor
        livro.ano = input(f"Novo ano ({livro.ano}): ") or livro.ano
        print(" Livro atualizado com sucesso!\n")
    except (ValueError, IndexError):
        print(" Opção inválida.\n")


def remover_livro():
    listar_livros()
    if not livros: return
    try:
        indice = int(input("🗑 Número do livro para remover: ")) - 1
        removido = livros.pop(indice)
        print(f" Livro '{removido.titulo}' removido com sucesso!\n")
    except (ValueError, IndexError):
        print(" Opção inválida.\n")


def cadastrar_usuario():
    nome = input(" Nome do usuário: ")
    matricula = input(" Matrícula: ")
    usuarios.append(Usuario(nome, matricula))
    print(" Usuário cadastrado com sucesso!\n")


def listar_usuarios():
    if not usuarios:
        print(" Nenhum usuário cadastrado.\n")
        return
    print("\n===  USUÁRIOS CADASTRADOS ===")
    for i, u in enumerate(usuarios, 1):
        print(f"{i}. {u}")
    print()


def realizar_emprestimo():
    listar_usuarios()
    if not usuarios: return
    try:
        idx_user = int(input("👤 Escolha o número do usuário: ")) - 1
        usuario = usuarios[idx_user]
    except (ValueError, IndexError):
        print(" Usuário inválido.\n")
        return

    listar_livros()
    try:
        idx_livro = int(input("📚 Escolha o número do livro: ")) - 1
        livro = livros[idx_livro]
        if not livro.disponivel:
            print(" Livro já emprestado!\n")
            return
        emprestimo = Emprestimo(livro, usuario)
        emprestimos.append(emprestimo)
        livro.disponivel = False
        usuario.historico.append(emprestimo)
        print(f" Empréstimo realizado! Devolução até {emprestimo.data_devolucao.strftime('%d/%m/%Y')}.\n")
    except (ValueError, IndexError):
        print(" Livro inválido.\n")


def devolver_livro():
    listar_usuarios()
    if not usuarios: return
    try:
        idx_user = int(input(" Usuário que está devolvendo: ")) - 1
        usuario = usuarios[idx_user]
    except (ValueError, IndexError):
        print(" Usuário inválido.\n")
        return

    emprestimos_ativos = [e for e in usuario.historico if not e.devolvido]
    if not emprestimos_ativos:
        print(" Nenhum empréstimo ativo para este usuário.\n")
        return

    print("\n===  EMPRÉSTIMOS ATIVOS ===")
    for i, e in enumerate(emprestimos_ativos, 1):
        print(f"{i}. {e}")
    try:
        idx_emp = int(input(" Escolha o número do empréstimo para devolver: ")) - 1
        emprestimo = emprestimos_ativos[idx_emp]
        emprestimo.devolvido = True
        emprestimo.livro.disponivel = True
        print(" Livro devolvido com sucesso!\n")
    except (ValueError, IndexError):
        print(" Opção inválida.\n")


def historico_usuario():
    listar_usuarios()
    if not usuarios: return
    try:
        idx_user = int(input(" Escolha o número do usuário: ")) - 1
        usuario = usuarios[idx_user]
    except (ValueError, IndexError):
        print(" Usuário inválido.\n")
        return

    if not usuario.historico:
        print(" Nenhum histórico encontrado.\n")
        return

    print(f"\n===  HISTÓRICO DE {usuario.nome} ===")
    for h in usuario.historico:
        print(h)
    print()



#  Menu Principal

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
        opcao = input(" Escolha uma opção: ")

        if opcao == "1": cadastrar_livro()
        elif opcao == "2": listar_livros()
        elif opcao == "3": editar_livro()
        elif opcao == "4": remover_livro()
        elif opcao == "5": cadastrar_usuario()
        elif opcao == "6": listar_usuarios()
        elif opcao == "7": realizar_emprestimo()
        elif opcao == "8": devolver_livro()
        elif opcao == "9": historico_usuario()
        elif opcao == "0":
            print(" Saindo do sistema... Até logo!")
            break
        else:
            print(" Opção inválida. Tente novamente.\n")



#  Execução

if __name__ == "__main__":
    print(" Bem-vindo ao Sistema de Biblioteca! ✨\n")
    menu()
