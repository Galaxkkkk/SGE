# Sistema de Gerenciamento de Estoque com Python

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2.1+-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📝 Descrição

Sistema completo de gerenciamento de estoque desenvolvido em Python utilizando:
- **CustomTkinter** para interface gráfica moderna
- **SQLite** para armazenamento de dados
- Arquitetura **MVC** (Model-View-Controller)
- Padrão **CRUD** para operações básicas

## ✨ Funcionalidades Principais

### 🔐 Autenticação de Usuários
- Sistema de login seguro
- Usuário admin padrão (admin/admin123)
- Níveis de acesso (administrador/comum)

### 📦 Gestão de Produtos
- Cadastro de novos itens
- Visualização em tabela organizada
- Edição completa de produtos
- Exclusão de itens do estoque
- 20 produtos de mercado pré-cadastrados

### 📊 Relatórios Inteligentes
- Identificação automática de itens com estoque baixo
- Destaque visual para produtos abaixo do nível mínimo
- Cálculo da quantidade faltante

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Finalidade | Versão |
|------------|------------|--------|
| Python | Linguagem principal | 3.8+ |
| CustomTkinter | Interface gráfica | ≥5.2.1 |
| SQLite | Banco de dados | 3 |
| Pillow | Manipulação de imagens | ≥10.0.0 |

## ⚙️ Configuração do Ambiente

git clone https://github.com/seu-usuario/estoque-system.git
cd estoque-system
pip install -r requirements.txt
python app.py

## 🤝 Como Contribuir

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/awesome-feature`)
3. Commit suas alterações (`git commit -m 'Add awesome feature'`)
4. Push para a branch (`git push origin feature/awesome-feature`)
5. Abra um Pull Request

## 📄 Licença

Distribuído sob licença MIT. Veja `LICENSE` para mais informações.

## ✉️ Contato

Desenvolvido por [Victoria Peixoto de OLiveira](https://github.com/galaxkkkk)  
Email: seu-email@exemplo.com

---

**Nota**: Para utilizar o sistema, execute `python app.py` e faça login com:
- Usuário: `admin`
- Senha: `admin123`

**Dica**: Os produtos pré-cadastrados incluem itens como arroz, feijão, óleo, leite e outros produtos básicos de mercado, com quantidades e preços realistas.
