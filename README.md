# ECOS DA PEDRA — Uma Jornada pela Arte Rupestre

Jogo educacional responsivo para estudantes do Ensino Médio aprenderem, revisarem e treinarem oralmente uma apresentação sobre arte rupestre.

## Executar

Requer Node.js 18 ou superior.

```bash
npm install
npm run dev
```

Abra o endereço exibido pelo Vite (normalmente `http://localhost:5173`). Para gerar a versão de produção:

```bash
npm run build
npm run preview
```

## Recursos

- Seis temas e 180 atividades locais (30 por tema), sem backend.
- Expedição em cinco áreas, XP, sequências, níveis e conquistas.
- Associação por arrastar ou tocar, parede-detetive com hotspots e respostas abertas com autoavaliação honesta.
- Revisão adaptativa por categoria, repetição local e Fogueira de Revisão.
- Modo apresentador com a Regra dos 5 Pontos, cronômetro e relatório de prontidão.
- Salvamento automático em `localStorage`, controles de som e reset com confirmação.
- Navegação por teclado, contraste, layouts responsivos e respeito a `prefers-reduced-motion`.

## Estrutura

`src/data` contém conteúdo, perguntas, conquistas e modelo de progresso; `src/pages` reúne as áreas da experiência; `src/components` contém elementos reutilizáveis; `src/hooks` gerencia persistência; e `src/styles` define a atmosfera visual.
