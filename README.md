# Sistema Bancário Pro: POO Avançada & Persistência JSON 🏦

Este projeto simula um ecossistema bancário operado via CLI (Interface de Linha de Comando), desenvolvido para demonstrar o domínio de **Programação Orientada a Objetos (POO)** em Python. A arquitetura foca em escalabilidade, permitindo que um único cliente possua múltiplas contas correntes vinculadas ao seu CPF.

## 🌟 Diferenciais Técnicos

A aplicação utiliza recursos modernos do Python para garantir um código limpo e eficiente:

* **`@classmethod` (Padrão Factory)**: Implementado para a reconstrução de objetos (`Transacao`, `Conta`, `Cliente`) a partir de dados serializados em JSON.
* **`@property` (Atributos Dinâmicos)**: 
    * `saldo_total`: Calcula em tempo real a soma do saldo com o limite de cheque especial.
    * `cpf_formatado`: Aplica máscaras de exibição (000.000.000-00) sem alterar o dado bruto.
    * `historico`: Converte logs de transações em objetos vivos para manipulação de dados.
* **Persistência de Dados**: Uso da biblioteca `json` para salvar o estado completo do banco em `data_contas.json`.

---

## 🏗️ Arquitetura e Modelagem

O sistema segue o princípio da responsabilidade única (**SRP**), dividindo a lógica entre modelos de dados e serviços de orquestração.



### Componentes Principais:
1.  **`Transacao`**: Gerencia os registros de movimentação com timestamp.
2.  **`Conta`**: Controla o saldo e as regras de negócio para saques e depósitos.
3.  **`Cliente`**: Centraliza os dados do titular e atua como um "container" para múltiplas instâncias de `Conta`.
4.  **`SistemaBancario`**: Classe de serviço responsável pelo I/O de arquivos, geração de números sequenciais e fluxo de operações.



---

## 🚀 Funcionalidades da CLI

| Sigla | Operação | Descrição |
| :--- | :--- | :--- |
| **nu** | Novo Usuário | Cadastra o cliente e cria sua conta corrente inicial. |
| **nc** | Nova Conta | **(Destaque)** Cria contas adicionais para um CPF já existente no sistema. |
| **d** | Depósito | Realiza crédito na conta informada. |
| **s** | Saque | Realiza débito validando saldo + limite de cheque especial. |
| **e** | Extrato | Exibe o histórico detalhado e saldos (atual e disponível). |
| **lc** | Listar | Gera um relatório de todas as contas, titulares e CPFs cadastrados. |
| **q** | Sair | Finaliza a aplicação e persiste as alterações no JSON. |

---

## 📦 Como Instalar e Rodar

1.  **Clone o repositório**:
    ```bash
    git clone https://github.com/EliasOFreitas/dio-luizalabs-python-desafio2
    ```
2.  **Execute o script principal**:
    ```bash
    python main.py
    ```

> **Atenção**: O arquivo `data_contas.json` será gerado automaticamente após a primeira operação de cadastro ou transação.

---

## 🧠 Conceitos de Engenharia Aplicados

* **Encapsulamento**: Atributos protegidos e acesso via propriedades.
* **Composição/Agregação**: Um objeto `Cliente` contém uma lista de objetos `Conta`.
* **Tratamento de Exceções**: Robustez na leitura de arquivos corrompidos ou inexistentes.
* **Desacoplamento**: A interface de usuário (menu) é separada da lógica de persistência e modelos.

---
**Desenvolvido por [Elias Oliveira]**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/eliasodefreitas)
