# API de Análise de E-mails com IA (Google Gemini)

Esta API é projetada para analisar, classificar e gerar respostas para e-mails usando o Google Gemini.

## Arquitetura

A solução utiliza uma abordagem de **modelo único**, onde um Large Language Model (LLM), o `gemini-1.5-flash`, executa todas as tarefas de IA.

Através de **Engenharia de Prompt**, o modelo é instruído a realizar um pipeline de tarefas em uma única chamada:
1.  **Limpeza de Dados:** O texto do e-mail é higienizado, removendo dados sensíveis.
2.  **Classificação:** O Gemini analisa o texto e o classifica como 'Produtivo' ou 'Improdutivo'.
3.  **Geração de Resposta:** Com base na classificação e no conteúdo, o Gemini gera uma resposta contextualizada e profissional.
4.  **Saída Estruturada:** O modelo é instruído a retornar sua análise em um formato JSON garantido, tornando a integração robusta e confiável.

Esta arquitetura minimiza a latência (apenas uma chamada de API) e simplifica a manutenção do código.

## Features

-   Endpoints para processar um e-mail individual via JSON (`/process-single-email`) ou um lote de e-mails via upload de arquivo CSV/Excel (`/process-batch`).
-   Limpeza e anonimização de dados sensíveis como URLs, e-mails e telefones.
-   Classificação de e-mails em 'Produtivo' ou 'Improdutivo'.
-   Geração de resposta automática e contextualizada usando IA.
-   Logging para monitoramento de cada etapa do processo.

## Como Executar Localmente

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/pv-toledo/email-classifier-api.git](https://github.com/pv-toledo/email-classifier-api.git)
    cd email-classifier-api
    ```

2.  **Crie e ative o ambiente virtual:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    -   Crie um arquivo `.env` na raiz do projeto.
    -   Adicione sua chave de API do Google Gemini:
        ```
        GOOGLE_API_KEY="AIza..."
        ```

5.  **Rode o servidor:**
    ```bash
    uvicorn main:app --reload
    ```

A API estará disponível em `http://127.0.0.1:8000` e a documentação interativa em `http://127.0.0.1:8000/docs`.

## Endpoints da API

* `POST /process-single-email`
    * **Input:** JSON com uma chave `content` contendo o texto do e-mail.
    * **Output:** JSON com a classificação e a resposta sugerida para o e-mail.

* `POST /process-batch`
    * **Input:** Upload de um arquivo `.csv` ou `.xlsx`. O arquivo deve conter uma única coluna com o cabeçalho `texto_do_email`.
    * **Output:** Uma lista de objetos JSON, cada um contendo o e-mail original, sua classificação e a resposta sugerida.