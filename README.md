# Jornada do Fazendeiro - Painel para Sunflower Land

![Simulador de Meta](https://i.imgur.com/g8i4VfR.png)

## 📖 Sobre o Projeto

**Jornada do Fazendeiro** é um painel de controle (dashboard) web avançado para jogadores de [Sunflower Land](https://sunflower-land.com/). A aplicação vai além de um simples visualizador, oferecendo uma **análise profunda e detalhada** da sua fazenda. Com um mapa interativo e um motor de cálculo de bônus, a ferramenta permite otimizar a coleta de recursos, planejar expansões e maximizar a eficiência do seu jogo.


**Nota:** Este é um projeto pessoal para fins de estudo e uso próprio.

---

## ✨ Funcionalidades Principais

### Painel de Análise da Fazenda
O coração da ferramenta é um dashboard completo que centraliza todas as informações vitais:

*   **Mapa Interativo da Fazenda**: Uma representação visual completa da sua terra, exibindo todos os recursos como árvores, pedras, plantações, frutas e flores.
    *   Clique em qualquer recurso para abrir um **card de detalhes** com informações em tempo real.
*   **Análise Detalhada de Recursos**:
    *   Veja o **rendimento (yield)** e o **tempo de recuperação** de cada recurso.
    *   Acompanhe bônus ativos de fertilizantes, abelhas e outros itens.
    *   Para frutas, visualize as colheitas restantes.
*   **Motor de Cálculo de Bônus Abrangente**: A ferramenta calcula e aplica automaticamente todos os bônus que afetam sua fazenda, incluindo:
    *   Skills do Bumpkin
    *   Buds (com lógica de `Type` + `Stem` e `Aura`)
    *   Wearables (Vestíveis)
    *   Collectibles (SFTs)
    *   Mecânicas Nativas do Jogo (como acertos críticos)
*   **Visualização de Área de Efeito (AOE)**: Clique em itens como o "Espantalho" ou a "Queen Cornelia" na legenda para ver instantaneamente a área de cobertura e os recursos afetados no mapa.
*   **Gerenciador da Estufa (Greenhouse)**: Visualize as plantas na sua estufa e os bônus específicos aplicados a elas.
*   **Dicas de Escavação de Tesouros**: Um painel auxiliar que ajuda a decifrar as dicas para encontrar tesouros.

### Outras Ferramentas

*   **Planejador de Expansão**:
    *   Mapa interativo que exibe o progresso das suas expansões.
    *   **Simulador de Meta**: Calcule os recursos necessários para alcançar qualquer nível de expansão, com detalhamento de custos totais e relativos.
*   **Diário de Pesca**: Acompanhe os peixes capturados, recordes, iscas e conquistas.
*   **Resumo do Inventário**: Visualize todos os seus itens e o valor estimado total em SFL.


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

O projeto está em constante evolução. Aqui estão algumas das funcionalidades e melhorias planejadas:

* **Novas Funcionalidades**:
    * [ ] **Painel de Animais**: Seção para gerenciar a produção e rentabilidade dos animais (galinhas, vacas, etc.).
    * [ ] **Rastreador de Construções**: Painel para ver os requisitos e benefícios de construções como Padaria, Cozinha, etc.
    * [ ] **Otimizador de Plantações**: Ferramenta para calcular qual plantação é mais lucrativa com base no tempo e custo de sementes.
    * [ ] **Planejador de Habilidades (Skills)**: Uma interface para visualizar os benefícios de cada habilidade e planejar a melhor ordem de desbloqueio.

* **Melhorias de Usabilidade (QoL)**:
    * [ ] **Conversor de Moeda ($, R$)**: Integrar com APIs de cotação para exibir os valores em SFL, Dólar e Real, permitindo ao usuário alternar entre as moedas.
    * [ ] **Gerenciador de Perfis**: Permitir salvar múltiplos IDs de fazenda, dar apelidos e alternar rapidamente entre eles (evolução do "Salvar Farm ID").
    * [ ] **Página de Carregamento (Loading)**: Melhorar o feedback visual enquanto os dados da API estão sendo carregados.
    * [ ] **Modo Escuro (Dark Mode)**: Adicionar um tema escuro para a interface.
    * [ ] **Suporte a Múltiplas Línguas (i18n)**: Preparar o projeto para ser traduzido, começando pelo inglês.

* **Melhorias Técnicas e Otimização**:
    * [ ] **Implementar Testes Unitários**: Criar testes para os serviços de back-end (`bud_service`, `mining_service`, etc.) para garantir a precisão dos cálculos de bônus e evitar regressões.
    * [ ] **Valores de Mercado para Itens Internos**: Implementar cálculo de valor em SFL para `Coins`, `Gem` e `Oil`.
    * [ ] **Refinar Responsividade**: Melhorar a adaptação da interface para uma experiência otimizada em dispositivos móveis.

---

## 🙏 Agradecimentos e Créditos

* **Sunflower Land**: Pelo jogo incrível e por manterem uma API pública para a comunidade.
* **SFL.world**: Este projeto não seria possível sem as APIs de dados e os preços de itens disponibilizados por [sfl.world](https://sfl.world/). Muitas das informações e referências de dados foram baseadas no excelente trabalho deles.
