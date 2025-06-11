import sqlite3

def criar_conexao(nome_db):
    """Cria uma conexão com o banco de dados SQLite especificado."""
    conn = None
    try:
        conn = sqlite3.connect(nome_db)
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    return conn

def criar_tabela_produtos(nome_db, nome_tabela):
    """Cria a tabela de produtos se ela não existir."""
    conn = criar_conexao(nome_db)
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {nome_tabela} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_produto TEXT NOT NULL,
                    quantidade INTEGER NOT NULL,
                    preco_compra REAL NOT NULL,
                    imagem TEXT,
                    cor_tag TEXT,
                    estoque_minimo INTEGER,
                    data_compra TEXT,
                    descricao_produto TEXT
                );
            """)
            conn.commit()
            print(f"Tabela '{nome_tabela}' verificada/criada com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao criar tabela: {e}")
        finally:
            if conn:
                conn.close()

def inserir_produto(nome_db, nome_tabela, produto_data):
    """Insere um novo produto no banco de dados."""
    conn = criar_conexao(nome_db)
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO {nome_tabela} (
                    nome_produto, quantidade, preco_compra, imagem, cor_tag, 
                    estoque_minimo, data_compra, descricao_produto
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                produto_data["Nome do Produto"],
                produto_data["Quantidade"],
                produto_data["Preço de Compra (R$)"],
                produto_data["Imagem"],
                produto_data["Cor da Tag"],
                produto_data["Estoque Mínimo"],
                produto_data["Data de Compra"], # Já deve ser uma string 'YYYY-MM-DD'
                produto_data["Descrição do Produto"]
            ))
            conn.commit()
            return cursor.lastrowid # Retorna o ID do item inserido
        except sqlite3.Error as e:
            print(f"Erro ao inserir produto: {e}")
            return None
        finally:
            if conn:
                conn.close()

def selecionar_todos_produtos(nome_db, nome_tabela):
    """Seleciona todos os produtos do banco de dados."""
    conn = criar_conexao(nome_db)
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {nome_tabela};")
            # Obter os nomes das colunas para criar um DataFrame
            colunas = [description[0] for description in cursor.description]
            dados = cursor.fetchall()
            return colunas, dados
        except sqlite3.Error as e:
            print(f"Erro ao selecionar produtos: {e}")
            return [], []
        finally:
            if conn:
                conn.close()

def selecionar_produto_por_id(nome_db, nome_tabela, produto_id):
    """Seleciona um produto pelo ID."""
    conn = criar_conexao(nome_db)
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {nome_tabela} WHERE id = ?;", (produto_id,))
            colunas = [description[0] for description in cursor.description]
            dado = cursor.fetchone()
            if dado:
                return dict(zip(colunas, dado)) # Retorna como dicionário para fácil acesso
            return None
        except sqlite3.Error as e:
            print(f"Erro ao selecionar produto por ID: {e}")
            return None
        finally:
            if conn:
                conn.close()

def atualizar_produto(nome_db, nome_tabela, produto_id, produto_data):
    """Atualiza um produto existente no banco de dados."""
    conn = criar_conexao(nome_db)
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE {nome_tabela} SET
                    nome_produto = ?,
                    quantidade = ?,
                    preco_compra = ?,
                    imagem = ?,
                    cor_tag = ?,
                    estoque_minimo = ?,
                    data_compra = ?,
                    descricao_produto = ?
                WHERE id = ?;
            """, (
                produto_data["Nome do Produto"],
                produto_data["Quantidade"],
                produto_data["Preço de Compra (R$)"],
                produto_data["Imagem"],
                produto_data["Cor da Tag"],
                produto_data["Estoque Mínimo"],
                produto_data["Data de Compra"],
                produto_data["Descrição do Produto"],
                produto_id
            ))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao atualizar produto: {e}")
            return False
        finally:
            if conn:
                conn.close()

def deletar_produto(nome_db, nome_tabela, produto_id):
    """Deleta um produto do banco de dados pelo ID."""
    conn = criar_conexao(nome_db)
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {nome_tabela} WHERE id = ?;", (produto_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao deletar produto: {e}")
            return False
        finally:
            if conn:
                conn.close()