# Jornada do Fazendeiro - Painel para Sunflower Land

![Simulador de Meta](https://i.imgur.com/g8i4VfR.png)

## 📖 Sobre o Projeto

**Jornada do Fazendeiro** é um painel de controle (dashboard) web avançado para jogadores de [Sunflower Land](https://sunflower-land.com/). A aplicação vai além de um simples visualizador, oferecendo uma **análise profunda e detalhada** da sua fazenda. Com um mapa interativo e um motor de cálculo de bônus, a ferramenta permite otimizar a coleta de recursos, planejar expansões e maximizar a eficiência do seu jogo.

**Nota:** Este é um projeto pessoal para fins de estudo e uso próprio.

---

## ✨ Funcionalidades Implementadas

### Painel de Análise da Fazenda
O coração da ferramenta é um dashboard completo que centraliza todas as informações vitais da sua fazenda:

*   **Mapa Interativo da Fazenda**: Uma representação visual completa da sua terra, exibindo a localização de todos os recursos, construções e colecionáveis.
    *   Clique em qualquer recurso (árvores, pedras, plantações, etc.) para abrir um **card de detalhes** com informações em tempo real sobre seu estado, tempo de recuperação e rendimento (yield) calculado.
*   **Análise Detalhada de Recursos**: Painéis dedicados para:
    *   **Recursos Básicos**: Madeira, Pedra, Ferro, Ouro e Crimstone.
    *   **Culturas e Colheitas**: Plantações, Frutas, Flores e Colmeias.
    *   **Máquinas**: Crop Machine e Estufa (Greenhouse).
*   **Motor de Cálculo de Bônus Abrangente**: A ferramenta calcula e aplica automaticamente todos os bônus que afetam sua fazenda, incluindo:
    *   Skills do Bumpkin
    *   Buds (com lógica de `Type` + `Stem` e `Aura`)
    *   Wearables (Vestíveis)
    *   Collectibles (SFTs)
    *   Mecânicas Nativas do Jogo (como acertos críticos, fertilizantes e enxames de abelhas).
*   **Visualização de Área de Efeito (AOE)**: Clique em itens como o "Espantalho" ou a "Queen Cornelia" na legenda do mapa para ver instantaneamente a área de cobertura e os recursos afetados.
*   **Dicas de Escavação de Tesouros**: Um painel auxiliar que ajuda a decifrar as dicas para encontrar tesouros no deserto, mostrando a grade de escavação e os padrões.

### ⚙️ Arquitetura Orientada a Dados e Precisão de Bônus

Recentemente, os serviços de análise de recursos (`fruit_service`, `chop_service`, `flower_service`, etc.) foram extensivamente refatorados para adotar uma **arquitetura totalmente orientada a dados**. Isso significa que a lógica de cálculo de rendimentos, tempos de recuperação e aplicação de bônus agora é lida diretamente de arquivos de domínio padronizados (`collectiblesItemBuffs.py`, `wearablesItemBuffs.py`, `skills.py`, `resources.py`), em vez de ser hardcoded em cada serviço.

**Benefícios:**

*   **Manutenibilidade Aprimorada**: Facilita a atualização e adição de novos itens, habilidades e mecânicas de jogo sem a necessidade de modificar a lógica central dos serviços.
*   **Precisão nos Cálculos**: Garante que todos os bônus, incluindo acertos críticos e modificadores complexos, sejam aplicados de forma consistente e precisa, espelhando fielmente a lógica do jogo.
*   **Extensibilidade**: Permite que novos tipos de bônus e condições sejam facilmente integrados no futuro.

### Ferramentas de Planejamento e Gestão

*   **Planejador de Expansão**:
    *   Mapa interativo que exibe o progresso visual das suas expansões.
    *   **Simulador de Meta**: Calcule os recursos necessários para alcançar qualquer nível de expansão, com detalhamento de custos totais e o que ainda falta.
*   **Diário de Pesca**: Acompanhe os peixes capturados, recordes de tamanho, iscas utilizadas e as conquistas de pesca.
*   **Gestão de Tarefas e Entregas**:
    *   **Quadro de Tarefas (Chores)**: Veja as tarefas diárias e os recursos necessários.
    *   **Entregas (Deliveries)**: Acompanhe os pedidos dos NPCs, recompensas e prazos.
*   **Resumo do Inventário**: Visualize todos os seus itens e o valor estimado total em SFL (baseado nos preços de mercado).

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
    * [ ] **Refatorar Cálculo de Bônus Multiplicativos**: Bônus de mel (Bee Suit, Honeycomb Shield, King of Bears) são aplicados como multiplicadores no jogo, mas estão configurados como aditivos nos arquivos de configuração. É necessário refatorar o `resource_analysis_service.py` para interpretar corretamente esses casos, possivelmente adicionando um campo de "display_value" para manter a consistência visual, sem hardcoding de exceções.
    * [ ] **Ampliar Cobertura de Testes**: Continuar a implementação de testes unitários para os serviços de back-end (`bud_service`, `mining_service`, etc.) para garantir a precisão dos cálculos de bônus e evitar regressões. (Testes básicos já existem para `analysis`, `domain_data` e `sunflower_api`).
    * [ ] **Valores de Mercado para Itens Internos**: Implementar cálculo de valor em SFL para `Coins`, `Gold` e `Oil`, que atualmente não possuem valor de mercado direto.
    * [ ] **Refinar Responsividade**: Melhorar a adaptação da interface para uma experiência otimizada em dispositivos móveis.

---

## 🙏 Agradecimentos e Créditos

* **Sunflower Land**: Pelo jogo incrível e por manterem uma API pública para a comunidade.
* **SFL.world**: Este projeto não seria possível sem as APIs de dados e os preços de itens disponibilizados por [sfl.world](https://sfl.world/). Muitas das informações e referências de dados foram baseadas no excelente trabalho deles.