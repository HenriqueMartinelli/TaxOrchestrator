# 📦 Processamento Tributário de Pedidos

Microserviço em Python para realizar leitura de pedidos via Excel, cálculo de impostos conforme nova legislação brasileira (IBS e CBS), e persistência no MongoDB.

---

## 🧠 Arquitetura

Este projeto adota **arquitetura hexagonal (Ports and Adapters)** com inspiração em **Clean Architecture**:

```
app/
├── application/
│   ├── ports/              # Interfaces (OrdersServicePort)
│   └── usecases/           # Lógica de negócio (List/Get/Process Orders)
├── controllers/            # Controladores da API
├── core/                   # Configuração geral (env, logging)
├── infrastructure/
│   ├── database/           # MongoDB repository
│   ├── messaging/          # EventBus
│   └── pipeline/           # ExcelReader e PolarsProcessor
├── routers/                # FastAPI routers
├── schemas/                # Modelos Pydantic (DTOs)
├── services/               # Adapters para integração dos use cases
├── shared/                 # Exceptions e Utils
├── main.py                 # Entrypoint da API

```

---

## 📐 Padrões de Projeto Usados

- **Ports and Adapters (Hexagonal Architecture)**
- **Factory Pattern** (Leitor Excel)
- **Strategy Pattern** (Cálculo tributário)
- **DTOs e Pydantic para validação**
- **BackgroundTasks** para execução assíncrona
- **EventBus simples** para possível desacoplamento de eventos

---

## ⚙️ Como Funciona

1. Recebe Excel com pedidos.
2. Lê e valida dados (usando Polars em modo Lazy).
3. Calcula impostos com base nas regras do `tax_rates.json`.
4. Insere dados processados no MongoDB.
5. Permite consultar pedidos via API.

---

## 📦 Instalando o Poetry

Recomenda-se seguir o guia oficial de instalação:
🔗 https://python-poetry.org/docs/#installation

---

## ▶️ Executando em ambiente de desenvolvimento

### Ativando o ambiente com Poetry
```bash
poetry shell
```

### Instalando as dependências
```bash
poetry install
```

### Iniciando a API
```bash
task up
```

A aplicação estará acessível em: [http://localhost:8000](http://localhost:8000)

---

## ✅ Testes

Para rodar os testes com cobertura:
```bash
task test
```
---

## 📚 Documentação da API

- Swagger UI: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

> ℹ️ Para desativar a docs, defina `dev mode = 0` no arquivo `.env`.

---

```
---

## 📦 Extras

- `sample_orders.xlsx`: arquivo de exemplo de pedidos
- `tax_rates.json`: configuração das alíquotas de impostos
- `generate_sample_excel.py`: script para gerar dados mock

---

Feito com ❤️ e boas práticas de software.
