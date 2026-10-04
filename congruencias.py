"""Núcleo matemático e banco de conteúdo do RestoLab.

Este módulo não depende do Streamlit, o que torna a matemática fácil de testar.
"""

from __future__ import annotations

from dataclasses import dataclass
from random import Random


@dataclass(frozen=True)
class Question:
    prompt: str
    subtitle: str
    choices: tuple[int, ...]
    answer: int
    explanation: str
    topic: str
    difficulty: str


LESSONS = (
    {
        "icon": "🧩",
        "title": "Divisão euclidiana",
        "level": "Fundamentos",
        "summary": "Todo inteiro se separa em grupos completos e um resto.",
        "body": "Para a e m > 0, existem únicos q e r tais que a = mq + r, com 0 ≤ r < m. O número q é o quociente e r é o resto.",
        "example": "43 = 6 × 7 + 1  →  resto 1",
        "tip": "O resto nunca é negativo nem alcança o divisor.",
    },
    {
        "icon": "🔁",
        "title": "Congruência",
        "level": "Fundamentos",
        "summary": "Números com o mesmo resto pertencem à mesma classe.",
        "body": "Escrevemos a ≡ b (mod m) quando m divide a − b. Isso equivale a dizer que a e b deixam o mesmo resto por m.",
        "example": "38 ≡ 3 (mod 7), pois 38 − 3 = 35",
        "tip": "Leia ≡ como ‘é congruente a’, e não como igualdade comum.",
    },
    {
        "icon": "🕐",
        "title": "Aritmética do relógio",
        "level": "Intuição",
        "summary": "Depois da última posição, a contagem recomeça.",
        "body": "Um relógio de 12 horas calcula módulo 12. Avançar 15 horas é igual a avançar 3 posições: 15 ≡ 3 (mod 12).",
        "example": "9h + 8h → 17h ≡ 5h (mod 12)",
        "tip": "Ciclos, calendários, música e computação usam a mesma ideia.",
    },
    {
        "icon": "➕",
        "title": "Soma e subtração",
        "level": "Operações",
        "summary": "Reduza cada parcela antes ou depois da operação.",
        "body": "Se a ≡ b e c ≡ d (mod m), então a + c ≡ b + d e a − c ≡ b − d (mod m).",
        "example": "47 + 38 ≡ 2 + 3 ≡ 0 (mod 5)",
        "tip": "Trocar números grandes por restos pequenos evita contas longas.",
    },
    {
        "icon": "✖️",
        "title": "Produtos e potências",
        "level": "Operações",
        "summary": "A congruência é preservada ao multiplicar e elevar.",
        "body": "Podemos reduzir fatores e bases: se a ≡ b (mod m), então ac ≡ bc e aⁿ ≡ bⁿ (mod m).",
        "example": "23² ≡ 3² ≡ 9 ≡ 4 (mod 5)",
        "tip": "Reduza a cada multiplicação para manter os números pequenos.",
    },
    {
        "icon": "⚡",
        "title": "Padrões de potências",
        "level": "Estratégia",
        "summary": "Restos de potências acabam formando ciclos.",
        "body": "Liste algumas potências reduzidas. Quando um resto se repetir, o ciclo recomeça; reduza o expoente pelo tamanho do ciclo.",
        "example": "2ⁿ mod 5: 2, 4, 3, 1, 2… ciclo 4",
        "tip": "Para 2¹⁰⁰ mod 5, como 100 ≡ 0 (mod 4), o resto é 1.",
    },
    {
        "icon": "🔍",
        "title": "Critérios de divisibilidade",
        "level": "Aplicações",
        "summary": "Critérios conhecidos são atalhos de congruência.",
        "body": "Como 10 ≡ 1 (mod 3 e mod 9), a soma dos algarismos tem o mesmo resto que o número nesses módulos.",
        "example": "7 452 ≡ 7+4+5+2 = 18 ≡ 0 (mod 9)",
        "tip": "Para módulo 11, use a soma alternada dos algarismos.",
    },
    {
        "icon": "🔐",
        "title": "Inverso modular",
        "level": "Avançado",
        "summary": "Dividir módulo m significa multiplicar por um inverso.",
        "body": "O inverso de a módulo m é x tal que ax ≡ 1 (mod m). Ele existe exatamente quando mdc(a, m) = 1.",
        "example": "3⁻¹ ≡ 5 (mod 7), pois 3 × 5 ≡ 1",
        "tip": "Não cancele fatores sem verificar se eles são invertíveis.",
    },
)


def euclidean_division(a: int, modulus: int) -> tuple[int, int]:
    """Retorna quociente e resto canônico para módulo positivo."""
    if modulus <= 0:
        raise ValueError("O módulo precisa ser positivo.")
    return divmod(a, modulus)


def are_congruent(a: int, b: int, modulus: int) -> bool:
    if modulus <= 0:
        raise ValueError("O módulo precisa ser positivo.")
    return (a - b) % modulus == 0


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Retorna (mdc, x, y) tal que ax + by = mdc(a,b)."""
    old_r, r = abs(a), abs(b)
    old_s, s, old_t, t = 1, 0, 0, 1
    while r:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    return old_r, old_s * (-1 if a < 0 else 1), old_t * (-1 if b < 0 else 1)


def modular_inverse(a: int, modulus: int) -> int | None:
    if modulus <= 1:
        return None
    gcd, x, _ = extended_gcd(a, modulus)
    return x % modulus if gcd == 1 else None


def solve_linear_congruence(a: int, b: int, modulus: int) -> list[int]:
    """Resolve ax ≡ b (mod m), retornando as soluções em [0,m)."""
    if modulus <= 0:
        raise ValueError("O módulo precisa ser positivo.")
    return [x for x in range(modulus) if (a * x - b) % modulus == 0]


def residue_table(modulus: int, operation: str = "+") -> list[list[int]]:
    if not 2 <= modulus <= 15:
        raise ValueError("Use um módulo entre 2 e 15.")
    if operation not in {"+", "×"}:
        raise ValueError("Operação inválida.")
    op = (lambda a, b: a + b) if operation == "+" else (lambda a, b: a * b)
    return [[op(a, b) % modulus for b in range(modulus)] for a in range(modulus)]


def _choices(answer: int, modulus: int, rng: Random) -> tuple[int, ...]:
    values = {answer}
    while len(values) < min(4, modulus):
        values.add(rng.randrange(modulus))
    return tuple(sorted(values))


def generate_question(difficulty: str = "Médio", seed: int | None = None) -> Question:
    """Gera perguntas reprodutíveis quando uma semente é informada."""
    rng = Random(seed)
    if difficulty == "Fácil":
        modulus = rng.randint(3, 9)
        number = rng.randint(12, 80)
        answer = number % modulus
        quotient = number // modulus
        return Question(
            f"Qual é o resto de {number} ÷ {modulus}?",
            f"Complete: {number} ≡ ? (mod {modulus})",
            _choices(answer, modulus, rng), answer,
            f"{number} = {modulus} × {quotient} + {answer}.",
            "Resto direto", difficulty,
        )

    if difficulty == "Difícil":
        modulus = rng.randint(5, 12)
        base = rng.randint(2, 12)
        exponent = rng.randint(4, 10)
        answer = pow(base, exponent, modulus)
        return Question(
            f"Qual é o resto de {base}^{exponent} por {modulus}?",
            "Reduza a base e procure um ciclo nas potências.",
            _choices(answer, modulus, rng), answer,
            f"Calculando com redução a cada etapa: {base}^{exponent} ≡ {answer} (mod {modulus}).",
            "Potências", difficulty,
        )

    modulus = rng.randint(4, 11)
    left, right = rng.randint(15, 80), rng.randint(8, 50)
    use_product = rng.choice((True, False))
    if use_product:
        answer = (left * right) % modulus
        expression = f"{left} × {right}"
        reduced = f"({left % modulus} × {right % modulus})"
        topic = "Produto modular"
    else:
        answer = (left + right) % modulus
        expression = f"{left} + {right}"
        reduced = f"({left % modulus} + {right % modulus})"
        topic = "Soma modular"
    return Question(
        f"Quanto vale {expression} módulo {modulus}?",
        "Reduza os termos antes de operar.",
        _choices(answer, modulus, rng), answer,
        f"{reduced} mod {modulus} = {answer}.", topic, difficulty,
    )
