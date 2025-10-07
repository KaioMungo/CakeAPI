# Usa uma imagem base oficial do Python (versão slim para ser menor)
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /usr/src/app

# Copia o arquivo de dependências e instala as bibliotecas
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código da aplicação
COPY . .

# Expõe a porta que o Flask vai usar (padrão 5000)
EXPOSE 5000

# Variável de ambiente para o Flask
ENV FLASK_APP=app.py

# Comando para rodar a aplicação quando o container iniciar
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
