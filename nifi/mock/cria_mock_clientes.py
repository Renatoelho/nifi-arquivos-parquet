from faker import Faker
import csv

nome_arquivo = "clientes.csv"
numero_registros = 1000000

fake = Faker()
Faker.seed(42)

print(f"Gerando {numero_registros} registros fictícios no arquivo {nome_arquivo}...")

with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(["id", "nome", "email"])

    for i in range(1, numero_registros + 1):
        nome = fake.name()
        email = fake.email()
    
        writer.writerow([i, nome, email])

        if i % 100000 == 0:
            print(f"{i} registros gerados...")

print(f"Arquivo {nome_arquivo} gerado com sucesso!")
