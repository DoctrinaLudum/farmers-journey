# Jornada do Fazendeiro - Painel para Sunflower Land

![Simulador de Meta](https://i.imgur.com/g8i4VfR.png)

## 📖 Sobre o Projeto

**Jornada do Fazendeiro** é um painel de controle (dashboard) web desenvolvido para auxiliar jogadores do jogo [Sunflower Land](https://sunflower-land.com/). A aplicação fornece uma visão detalhada e organizada da fazenda de um jogador, ajudando no planejamento de expansões, gerenciamento de inventário e acompanhamento do progresso geral.

**Nota:** Este é um projeto pessoal para fins de estudo e uso próprio.

---

## ✨ Funcionalidades Principais

* **Painel Geral**: Visão rápida dos seus SFL, Coins, nível do Bumpkin e outros status vitais.
* **Planejador de Expansão**:
    * Mapa interativo que exibe o progresso das suas expansões.
    * **Simulador de Meta**: Calcule os recursos necessários para alcançar qualquer nível de expansão.
    * Exibe o **Custo Total**, **Custo Relativo** (apenas do que falta) e os custos individuais por recurso em SFL.
* **Diário de Pesca**: Acompanhe os peixes capturados, recordes, iscas e conquistas relacionadas à pesca.
* **Resumo do Inventário**: Visualize todos os seus itens e o valor estimado total em SFL.

---

## 🛠️ Tecnologias Utilizadas

* **Back-end**: Python, Flask, Flask-Caching
* **Front-end**: TypeScript, Bootstrap
* **Gerenciamento de Pacotes**: Poetry (Python), NPM (Node.js)

---

## 🚀 Como Usar

Na página inicial, insira o ID da sua fazenda de Sunflower Land e clique em "Carregar Fazenda" para visualizar os painéis com os dados correspondentes.

---

## 📝 TODO (Próximos Passos e Ideias)

* **Valores de Recursos**:
    * [ ] Implementar cálculo de valor em SFL para `Coins`, `Gem` e `Oil`, que não possuem preço de mercado direto.

* **Novas Funcionalidades**:
    * [ ] **Planejador de Habilidades (Skills)**: Uma interface para visualizar os benefícios de cada habilidade e planejar a melhor ordem de desbloqueio.
    * [ ] **Rastreador de Construções**: Painel para ver os requisitos e benefícios de construções como Padaria, Cozinha, etc.
    * [ ] **Otimizador de Plantações**: Ferramenta para calcular qual plantação é mais lucrativa com base no tempo e custo de sementes.
    * [ ] **Painel de Animais**: Seção para gerenciar a produção e rentabilidade dos animais (galinhas, vacas, etc.).

* **Melhorias de Usabilidade (QoL)**:
    * [ ] **Modo Escuro (Dark Mode)**: Adicionar um tema escuro para a interface.
    * [ ] **Salvar Farm ID**: Usar o `localStorage` do navegador para salvar o ID da fazenda, evitando que o usuário precise digitá-lo a cada visita.
    * [ ] **Suporte a Múltiplas Línguas (i18n)**: Preparar o projeto para ser traduzido, começando pelo inglês.
    * [ ] **Página de Carregamento (Loading)**: Melhorar o feedback visual enquanto os dados da API estão sendo carregados.

---

## 🙏 Agradecimentos e Créditos

* **Sunflower Land**: Pelo jogo incrível e por manterem uma API pública para a comunidade.
* **SFL.world**: Este projeto não seria possível sem as APIs de dados e os preços de itens disponibilizados por [sfl.world](https://sfl.world/). Muitas das informações e referências de dados foram baseadas no excelente trabalho deles.