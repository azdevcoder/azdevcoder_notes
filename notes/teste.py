# --- Sistema de Teste: Gestão de Biblioteca ---

def linha_divisora():
    print("-" * 10)

# 1. Definição de dados iniciais
livros_disponiveis = ["Dom Casmurro", "O Alquimista", "1984", "O Pequeno Príncipe"]
usuarios_ativos = {"Ana": 2, "Bruno": 0, "Carla": 5}

print("TESTE 1: Estado inicial dos dados")
print(f"Livros no catálogo: {livros_disponiveis}")
print(f"Status dos usuários (nome: livros emprestados): {usuarios_ativos}")
linha_divisora()

# 2. Testando uma função de empréstimo
def emprestar_livro(usuario, livro):
    print(f"[LOG] Tentando emprestar '{livro}' para {usuario}...")
    
    if livro not in livros_disponiveis:
        print(f"[ERRO] O livro '{livro}' não está no catálogo.")
        return False
    
    if usuarios_ativos.get(usuario, 0) >= 3:
        print(f"[AVISO] {usuario} já atingiu o limite de 3 livros.")
        return False
    
    # Executando a operação
    livros_disponiveis.remove(livro)
    usuarios_ativos[usuario] = usuarios_ativos.get(usuario, 0) + 1
    print(f"[SUCESSO] Empréstimo realizado com êxito!")
    return True

# 3. Executando bateria de testes
print("TESTE 2: Simulação de empréstimos")

# Caso de sucesso
emprestar_livro("Bruno", "1984")

# Caso de erro: Livro inexistente
emprestar_livro("Ana", "Harry Potter")

# Caso de erro: Limite de usuário atingido
emprestar_livro("Carla", "Dom Casmurro")

linha_divisora()

# 4. Testando Loops e Condicionais nos resultados finais
print("TESTE 3: Verificação final de estoque")
for livro in ["O Alquimista", "1984", "O Hobbit"]:
    status = "Disponível" if livro in livros_disponiveis else "Indisponível/Emprestado"
    print(f"Checagem de estoque -> {livro}: {status}")

linha_divisora()

print("TESTE 4: Dicionário final de usuários")
for nome, qtd in usuarios_ativos.items():
    print(f"Usuário: {nome:10} | Livros com ele: {qtd}")

print("\n--- Fim dos testes ---")