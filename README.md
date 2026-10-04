# RestoLab

Uma academia interativa em Streamlit para aprender **congruências e restos de divisão**, dos fundamentos até inversos e equações modulares.

## Como executar

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

O aplicativo ficará disponível em `http://localhost:8501`.

## Recursos

- oito aulas progressivas com exemplos, dicas e acompanhamento de conclusão;
- arena de prática em três dificuldades, com questões de restos, operações e potências;
- XP, metas diárias, sequência, precisão, conquistas e progresso da sessão;
- laboratório para comparar números, calcular inversos e resolver congruências lineares;
- relógio modular animado pelos controles e tabelas de soma e multiplicação;
- guia de bolso com propriedades, atalhos, vocabulário e armadilhas comuns;
- layout responsivo para desktop e celular.

## Testes

O núcleo matemático é independente da interface e pode ser validado sem iniciar o Streamlit:

```bash
python -m unittest discover -s tests -v
```
