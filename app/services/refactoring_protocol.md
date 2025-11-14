# Protocolo de Refatoração de Serviços de Análise de Recursos

## 1. Objetivo

O objetivo deste protocolo é padronizar a arquitetura dos serviços de análise de recursos (madeira, mineração, etc.), garantindo que cada serviço seja:

*   **Autossuficiente:** Contenha toda a lógica necessária para sua análise, sem depender de serviços genéricos.
*   **Desacoplado:** Separe claramente a análise de **potencial teórico (Sumário)** da análise do **estado real (Nós Individuais)**.
*   **Claro e Manutenível:** Utilize funções privadas com responsabilidades únicas, facilitando a depuração e futuras atualizações.

## 2. Estrutura do Serviço

Cada serviço de recurso deve seguir a seguinte estrutura de funções:

1.  **Função Orquestradora Principal:**
    *   `analyze_[recurso]_resources(farm_data)`: Ponto de entrada do serviço.

2.  **Funções de Coleta de Dados (Setup):**
    *   `_get_all_item_data()`: Unifica todos os domínios de itens.
    *   `_get_player_items(farm_data)`: Extrai todos os itens do jogador.
    *   `_filter_boosts_for_[recurso]`: Cria o catálogo de bônus relevantes para o recurso específico.

3.  **Funções de Análise Desacopladas:**
    *   `_analyze_farm_summary(...)`: Calcula o sumário teórico (Min/Méd/Máx, Custo, Eficiência).
    *   `_analyze_individual_nodes(...)`: Analisa o estado real de cada nó (árvore, rocha, etc.) na fazenda.

4.  **Funções de Lógica de Negócio:**
    *   `_get_active_player_boosts(...)`: Determina os bônus **base** do jogador.
    *   `_get_[recurso]_drop_amount(...)`: Calcula o rendimento (yield).
    *   `_get_[recurso]_recovery_time(...)`: Calcula o tempo de recuperação.
    *   `_get_[ferramenta]_cost_and_quantity_info(...)`: Calcula o custo e uso de ferramentas.
    *   `_format_buffs_for_display(...)`: Formata os bônus para a UI.

## 3. Fluxo de Execução e Responsabilidades

A função principal `analyze_[recurso]_resources` deve orquestrar o fluxo da seguinte maneira:

1.  **Setup Inicial:**
    *   Chamar `_get_all_item_data()` para ter uma fonte única de dados de itens.
    *   Chamar `_filter_boosts_for_[recurso]` para criar um catálogo de bônus específico para o recurso em questão (ex: apenas bônus que afetam `Wood`, `Tree`, `Axe`).
        *   **Ponto Crítico:** Este filtro deve ser abrangente, incluindo `YIELD`, `RECOVERY_TIME`, `COST` e **`CRITICAL_CHANCE`** como tipos de bônus relevantes.

2.  **Análise Desacoplada:**
    *   Chamar `_analyze_farm_summary()` para obter o dicionário `summary_analysis`. Esta função é um "mundo fechado" e deve conter toda a lógica para:
        *   Obter os bônus base do jogador (sem `YIELD` de críticos).
        *   Calcular o rendimento **Mínimo** (apenas com bônus base).
        *   Construir uma lista de bônus de potencial máximo (base + `YIELD` de todos os críticos, incluindo "Native").
        *   Calcular o rendimento **Máximo**.
        *   Calcular o rendimento **Médio** usando a fórmula de média ponderada com as chances de crítico.
        *   Calcular custos de ferramentas e métricas de eficiência (por ciclo).
    *   Chamar `_analyze_individual_nodes()` para obter a análise do estado real da fazenda. Esta função também é um "mundo fechado" e deve:
        *   Obter a lista de bônus base.
        *   Iterar sobre cada nó (árvore, rocha) da fazenda.
        *   **Ponto Crítico:** Usar `copy.deepcopy()` da lista de bônus base no início de cada iteração para evitar contaminação de estado entre os nós.
        *   Aplicar os bônus de críticos que **realmente ocorreram** naquele nó específico.
        *   Calcular o tempo de recuperação usando a lógica de `effective_chopped_at` (ver abaixo).
        *   Determinar o status ("Pronta" ou "Recuperando").

3.  **Montagem da Resposta:**
    *   Combinar os resultados de `summary_analysis` e `individual_analysis_result` em um único dicionário `view_data` a ser retornado para o template.

## 4. Métodos e Lógicas Chave a Replicar

*   **Filtragem de Bônus de Crítico:** A função `_get_active_player_boosts` **deve** identificar itens que concedem `CRITICAL_CHANCE` e **ignorar** os bônus de `YIELD` desses itens ao montar a lista de bônus base.

*   **Cálculo de Tempo de Recuperação (Lógica `chop.ts`):**
    1.  A função `_get_[recurso]_recovery_time` deve calcular o tempo final (`final`) e também a **redução total em segundos** (`reduction_seconds`).
    2.  Na análise de nós individuais, o `choppedAt` efetivo deve ser calculado como: `effective_chopped_at = choppedAt - reduction_ms`.
    3.  A verificação de prontidão (`is_ready`) deve ser sempre: `current_timestamp >= (effective_chopped_at + TEMPO_BASE_DE_RECUPERACAO)`.
    4.  O timestamp de "Pronta Em" (`ready_at_ms`) deve ser sempre: `effective_chopped_at + TEMPO_BASE_DE_RECUPERACAO`.

*   **Cálculo de Custo de Ferramenta:** Deve haver uma função dedicada que considere o preço base, os bônus de desconto e os casos especiais (como "Foreman Beaver" que zera o custo).