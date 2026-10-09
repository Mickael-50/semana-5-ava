import csv
import re
from datetime import datetime
from pathlib import Path


ARQUIVO_ENTRADA = Path("dados.csv")
ARQUIVO_RELATORIO = Path("relatorio.txt")

COLUNAS_OBRIGATORIAS = {"email", "cpf", "telefone", "data"}


class FormatoInvalidoError(Exception):
    """Exceção personalizada para dados que não atendem às regras do sistema."""


def validar_email(email: str) -> bool:
    """Valida uma estrutura comum de e-mail."""
    padrao = r"^[\w.+-]+@[\w-]+(?:\.[\w-]+)+$"
    return bool(re.fullmatch(padrao, email.strip()))


def validar_cpf(cpf: str) -> bool:
    """Valida o formato do CPF, com ou sem pontuação."""
    padrao = r"(?:\d{11}|\d{3}\.\d{3}\.\d{3}-\d{2})"
    return bool(re.fullmatch(padrao, cpf.strip()))


def validar_telefone(telefone: str) -> bool:
    """Valida telefones brasileiros comuns, com DDD, com ou sem pontuação."""
    padrao = r"(?:\(?\d{2}\)?\s?)?(?:9?\d{4})-?\d{4}"
    return bool(re.fullmatch(padrao, telefone.strip()))


def validar_data(data: str) -> bool:
    """Valida datas no formato DD/MM/AAAA e verifica se a data existe."""
    if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", data.strip()):
        return False
    try:
        datetime.strptime(data.strip(), "%d/%m/%Y")
        return True
    except ValueError:
        return False


def validar_registro(registro: dict, numero_linha: int) -> dict:
    """Retorna o registro com os resultados das validações."""
    try:
        email = registro["email"].strip()
        cpf = registro["cpf"].strip()
        telefone = registro["telefone"].strip()
        data = registro["data"].strip()
    except KeyError as erro:
        raise KeyError(f"Coluna obrigatória ausente: {erro.args[0]}") from erro

    validacoes = {
        "email": validar_email(email),
        "cpf": validar_cpf(cpf),
        "telefone": validar_telefone(telefone),
        "data": validar_data(data),
    }

    campos_invalidos = [campo for campo, valido in validacoes.items() if not valido]

    if campos_invalidos:
        raise FormatoInvalidoError(
            f"Linha {numero_linha}: campos inválidos: {', '.join(campos_invalidos)}"
        )

    return {
        "linha": numero_linha,
        "email": email,
        "cpf": cpf,
        "telefone": telefone,
        "data": data,
    }


def analisar_arquivo(caminho: Path) -> tuple[list[dict], list[str], int]:
    validos = []
    invalidos = []
    total_registros = 0

    try:
        with caminho.open("r", encoding="utf-8", newline="") as arquivo:
            leitor = csv.DictReader(arquivo)

            if leitor.fieldnames is None:
                raise ValueError("O arquivo CSV está vazio ou não possui cabeçalho.")

            colunas = {coluna.strip() for coluna in leitor.fieldnames if coluna}
            faltantes = COLUNAS_OBRIGATORIAS - colunas
            if faltantes:
                raise KeyError(
                    f"Colunas obrigatórias ausentes no CSV: {', '.join(sorted(faltantes))}"
                )

            # Normaliza os nomes das colunas para minúsculas e remove espaços.
            leitor.fieldnames = [coluna.strip().lower() for coluna in leitor.fieldnames]

            for numero_linha, registro in enumerate(leitor, start=2):
                if not registro or all(
                    valor is None or not valor.strip()
                    for valor in registro.values()
                ):
                    continue

                total_registros += 1
                try:
                    registro_validado = validar_registro(registro, numero_linha)
                    validos.append(registro_validado)
                except FormatoInvalidoError as erro:
                    invalidos.append(str(erro))
                except (KeyError, AttributeError, TypeError) as erro:
                    invalidos.append(f"Linha {numero_linha}: registro incompleto ou inválido ({erro}).")
                except ValueError as erro:
                    invalidos.append(f"Linha {numero_linha}: valor inválido ({erro}).")

    except FileNotFoundError:
        print(f"Erro: o arquivo '{caminho}' não foi encontrado.")
        raise
    except PermissionError:
        print(f"Erro: sem permissão para ler '{caminho}'.")
        raise
    except csv.Error as erro:
        print(f"Erro ao interpretar o CSV: {erro}")
        raise
    else:
        print(f"Leitura concluída: {caminho}")
    finally:
        print("Etapa de leitura finalizada.")

    return validos, invalidos, total_registros


def gerar_relatorio(validos: list[dict], invalidos: list[str], total: int) -> str:
    percentual = (len(validos) / total * 100) if total else 0.0
    linhas = [
        "=" * 55,
        "RELATÓRIO DE ANÁLISE DE DADOS",
        "=" * 55,
        f"Total de registros analisados: {total}",
        f"Registros válidos: {len(validos)}",
        f"Registros inválidos: {len(invalidos)}",
        f"Taxa de aprovação: {percentual:.2f}%",
        "",
        "REGISTROS VÁLIDOS",
        "-" * 55,
    ]

    if validos:
        for item in validos:
            linhas.append(
                f"Linha {item['linha']}: e-mail={item['email']} | "
                f"CPF={item['cpf']} | telefone={item['telefone']} | data={item['data']}"
            )
    else:
        linhas.append("Nenhum registro válido.")

    linhas.extend(["", "REGISTROS INVÁLIDOS", "-" * 55])
    if invalidos:
        linhas.extend(invalidos)
    else:
        linhas.append("Nenhum registro inválido.")

    linhas.append("=" * 55)
    return "\n".join(linhas)


def main() -> None:
    try:
        validos, invalidos, total = analisar_arquivo(ARQUIVO_ENTRADA)
    except (FileNotFoundError, PermissionError, KeyError, ValueError, csv.Error) as erro:
        print(f"Não foi possível concluir a análise: {erro}")
        return
    else:
        relatorio = gerar_relatorio(validos, invalidos, total)
        try:
            with ARQUIVO_RELATORIO.open("w", encoding="utf-8") as arquivo:
                arquivo.write(relatorio)
        except OSError as erro:
            print(f"Erro ao salvar o relatório: {erro}")
        else:
            print("\n" + relatorio)
            print(f"\nRelatório salvo em: {ARQUIVO_RELATORIO.resolve()}")
        finally:
            print("Processamento encerrado.")


if __name__ == "__main__":
    main()
