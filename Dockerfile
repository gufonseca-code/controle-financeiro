# Usa a imagem oficial do Red Hat Universal Base Image com Python 3.11
FROM registry.access.redhat.com/ubi9/python-311

# Define o diretório de trabalho
WORKDIR /app

# No UBI, as dependências de compilação costumam ser instaladas via dnf ou microdnf
# O psycopg2-binary que está no seu requirements.txt 
# pode precisar de bibliotecas de desenvolvimento do Postgres
USER root
RUN dnf install -y gcc postgresql-devel && dnf clean all


# Copia e instala as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .
RUN chmod +x entrypoint.sh

USER 1001

# Comando para rodar a aplicação
CMD ["./entrypoint.sh"]
