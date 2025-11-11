// typescript/expansion_planner.ts

/**
 * Propósito: Configurar o formulário "Meta Final".
 * Adiciona um ouvinte de evento que, ao submeter, busca os dados da API
 * e chama a função para renderizar os resultados do plano de expansão.
 */
export function setupGoalForm() {
    const goalForm = document.getElementById('goal-form') as HTMLFormElement;
    if (goalForm) {
        goalForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const resultsContainer = document.getElementById('goal-results-container');
            if (!resultsContainer) return;

            resultsContainer.innerHTML = `<div class="d-flex justify-content-center align-items-center mt-3"><div class="spinner-border spinner-border-sm" role="status"><span class="visually-hidden">Calculando...</span></div><span class="ms-2 small">Calculando plano...</span></div>`;

            const farmId = goalForm.dataset.farmId;
            const currentLandType = goalForm.dataset.currentLandType;
            const currentLevel = goalForm.dataset.currentLevel;
            const goalLevelSelect = document.getElementById('goal_level') as HTMLSelectElement;
            const goalLevel = goalLevelSelect.value;

            if (!goalLevel) {
                resultsContainer.innerHTML = '<p class="text-muted text-center small mt-3">Por favor, selecione um nível válido.</p>';
                return;
            }

            const apiUrl = `/api/goal_requirements/${farmId}/${currentLandType}/${currentLevel}?goal_level=${goalLevel}`;

            try {
                const response = await fetch(apiUrl);
                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(`Erro na API (${response.status}): ${errorText}`);
                }
                const data = await response.json();

                resultsContainer.innerHTML = '';
                if (data && (data.requirements || data.unlocks)) {
                    renderGoalResults(data);
                } else {
                    resultsContainer.innerHTML = '<p class="text-muted text-center small mt-3">Não foi possível calcular o plano para esta meta.</p>';
                }
            } catch (error) {
                console.error("Ocorreu um erro ao processar a resposta da API:", error);
                resultsContainer.innerHTML = '<p class="text-danger text-center small mt-3">Ocorreu um erro ao buscar os dados. Tente novamente.</p>';
            }
        });
    }
}

/**
 * Propósito: Renderizar os resultados do plano de expansão na secção "Meta Final".
 */
function renderGoalResults(data: any) {
    // --- Parte 1: Setup dos templates e containers ---
    const resultsContainer = document.getElementById('goal-results-container');
    const mainTemplate = document.getElementById('goal-list-template') as HTMLTemplateElement;
    const itemTemplate = document.getElementById('goal-list-item-template') as HTMLTemplateElement;
    const summaryTableTemplate = document.getElementById('unlocks-summary-table-template') as HTMLTemplateElement;
    const summaryItemTemplate = document.getElementById('unlocks-summary-item-template') as HTMLTemplateElement;

    if (!resultsContainer || !mainTemplate || !itemTemplate || !summaryTableTemplate || !summaryItemTemplate) {
        console.error("Um ou mais templates para renderizar os resultados não foram encontrados.");
        return;
    }

    resultsContainer.innerHTML = ''; 
    const mainClone = mainTemplate.content.cloneNode(true) as DocumentFragment;

    // --- Parte 2: Preenche as informações gerais do plano (com modificações) ---
    const goalLevelEl = mainClone.querySelector('[data-template="goal-level"]');
    if (goalLevelEl) goalLevelEl.textContent = data.goal_level_display;

    const goalLandTypeEl = mainClone.querySelector('[data-template="goal-land-type"]');
    if (goalLandTypeEl) goalLandTypeEl.textContent = data.goal_land_type;
    
    const bumpkinLevelEl = mainClone.querySelector('[data-template="bumpkin-level"]');
    if(bumpkinLevelEl) bumpkinLevelEl.textContent = data.max_bumpkin_level;

    const totalTimeEl = mainClone.querySelector('[data-template="total-time"]');
    if(totalTimeEl) totalTimeEl.textContent = data.total_time_str;
    
    // Preenche o Custo Total
    const totalCostEl = mainClone.querySelector('[data-template="total-cost"]');
    if (totalCostEl && data.total_sfl_cost) {
        const sflValue = parseFloat(data.total_sfl_cost);
        totalCostEl.innerHTML = window.currencyConverter.generateCurrencyHTML(sflValue);
    }

    // Preenche o Custo Relativo
    const totalRelativeCostEl = mainClone.querySelector('[data-template="total-relative-cost"]');
    if (totalRelativeCostEl && data.total_relative_sfl_cost) {
        const sflValue = parseFloat(data.total_relative_sfl_cost);
        totalRelativeCostEl.innerHTML = window.currencyConverter.generateCurrencyHTML(sflValue);
    }

    // --- Parte 3: Renderiza a lista de requisitos (com modificações) ---
    const column1 = mainClone.querySelector('[data-column="1"]');
    const column2 = mainClone.querySelector('[data-column="2"]');

    if (column1 && column2 && data.requirements) {
        data.requirements.forEach((item: any, index: number) => {
            const itemClone = itemTemplate.content.cloneNode(true) as DocumentFragment;
            
            const iconEl = itemClone.querySelector<HTMLImageElement>('[data-template="icon"]');
            if (iconEl && item.icon) {
                iconEl.src = `/static/${item.icon}`;
            }
            
            const nameEl = itemClone.querySelector('[data-template="name"]');
            if (nameEl) nameEl.textContent = item.name;

            const shortfallEl = itemClone.querySelector<HTMLSpanElement>('[data-template="shortfall"]');
            if (shortfallEl) {
                const shortfallValue = parseFloat(item.shortfall);
                if (shortfallValue > 0) {
                    shortfallEl.textContent = `Faltam ${shortfallValue.toLocaleString('pt-BR', { useGrouping: true })}`;
                    shortfallEl.className = 'badge bg-warning text-dark';
                } else {
                    shortfallEl.textContent = 'Completo';
                    shortfallEl.className = 'badge bg-success';
                }
            }

            const neededEl = itemClone.querySelector<HTMLElement>('[data-template="value_of_needed"]');
            if (neededEl) {
                const neededValue = parseFloat(item.needed);
                neededEl.textContent = `de ${neededValue.toLocaleString('pt-BR', { useGrouping: true })}`;
            }

            const sflValueEl = itemClone.querySelector<HTMLElement>('[data-template="sfl_value"]');
            if (sflValueEl) {
                const sflValueNum = parseFloat(item.sfl_value);
                sflValueEl.innerHTML = window.currencyConverter.generateCurrencyHTML(sflValueNum, '~');
            }

            if (index % 2 === 0) {
                column1.appendChild(itemClone);
            } else {
                column2.appendChild(itemClone);
            }
        });
    }

    resultsContainer.appendChild(mainClone);

    // --- Parte 4: Renderiza os Desbloqueios e Ganhos (sem alterações aqui) ---
    const unlocksData = data.unlocks;
    const summaryList = unlocksData?.summary; 

    if (summaryList && summaryList.length > 0) {
        const tableClone = summaryTableTemplate.content.cloneNode(true) as DocumentFragment;
        const tableBody = tableClone.querySelector('[data-template="summary-table-body"]');

        if (tableBody) {
            summaryList.forEach((item: any) => {
                const itemClone = summaryItemTemplate.content.cloneNode(true) as DocumentFragment;
                const row = itemClone.querySelector('[data-template="item-row"]') as HTMLElement;
                const icon = itemClone.querySelector<HTMLImageElement>('[data-template="icon"]');
                const name = itemClone.querySelector<HTMLSpanElement>('[data-template="name"]');
                const total = itemClone.querySelector<HTMLTableCellElement>('[data-template="total"]');

                if (icon) {
                    icon.src = `/static/${item.icon}`;
                }
                if (name) name.textContent = item.name;
                if (total) total.textContent = `+${item.total}`;

                let tooltipTitle = 'Ganhos por Nível:\n';
                for (const [level, count] of Object.entries(item.details)) {
                    tooltipTitle += `- Nível ${level}: +${count}\n`;
                }
                
                if (row) {
                    row.title = tooltipTitle.trim();
                }

                tableBody.appendChild(itemClone);
            });
        }
        resultsContainer.appendChild(tableClone);
    }
}

/**
 * Propósito: Configurar e gerir o contador regressivo para uma expansão em andamento.
 */
export function setupExpansionCountdown() {
    const countdownElement = document.getElementById('countdown-timer');
    if (!countdownElement) return;

    const readyAtTimestamp = parseInt(countdownElement.dataset.readyAt || '0', 10);
    if (!readyAtTimestamp) return;

    const interval = setInterval(() => {
        const now = new Date().getTime();
        const distance = readyAtTimestamp - now;

        if (distance < 0) {
            clearInterval(interval);
            return;
        }

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        let timeLeft = '';
        if (days > 0) timeLeft += `${days}d `;
        timeLeft += `${String(hours).padStart(2, '0')}h `;
        timeLeft += `${String(minutes).padStart(2, '0')}m `;
        timeLeft += `${String(seconds).padStart(2, '0')}s`;
        
        countdownElement.textContent = `Faltam ${timeLeft.trim()}`;
    }, 1000);
}


/**
 * Propósito: Configura todas as interações do mapa de expansão.
 * A nova versão usa delegação de evento para gerenciar os tooltips em múltiplos mapas (um por aba de ilha).
 */
export function setupInteractiveMap() {
    // O container principal que detém todos os painéis de mapa (abas)
    const mapTabContent = document.getElementById('map-tab-content');
    if (!mapTabContent) return;

    // Função para esconder todos os tooltips
    const hideAllTooltips = () => {
        mapTabContent.querySelectorAll<HTMLElement>('.map-tooltip').forEach(tt => {
            tt.style.display = 'none';
        });
    };

    // --- LÓGICA DO TOOLTIP USANDO DELEGAÇÃO DE EVENTO ---

    // Evento para quando o mouse entra em um lote
    mapTabContent.addEventListener('mouseenter', (event) => {
        const plot = (event.target as HTMLElement).closest('.map-plot');
        if (!plot) return;

        // Encontra o painel da aba ativa para localizar o tooltip correto
        const activePane = plot.closest('.tab-pane');
        if (!activePane) return;

        const tooltip = activePane.querySelector<HTMLElement>('.map-tooltip');
        if (!tooltip) return;

        // Extrai os dados do lote
        const requirements = JSON.parse((plot as HTMLElement).dataset.plotRequirements || '{}');
        const nodes = JSON.parse((plot as HTMLElement).dataset.plotNodes || '{}');
        const plotState = (plot as HTMLElement).dataset.plotState;
        const plotNumber = (plot as HTMLElement).dataset.plotNumber;

        // Monta o conteúdo do tooltip
        let content = `<div class="tooltip-title">Lote #${plotNumber}</div><ul class="tooltip-list">`;
        if (plotState === 'owned' || plotState === 'in_progress' || plotState === 'construction_complete') {
            content += '<li class="tooltip-list-header">Recursos neste lote:</li>';
            if (Object.keys(nodes).length === 0) {
                 content += '<li>Nenhum recurso novo.</li>';
            } else {
                for (const [node, count] of Object.entries(nodes)) {
                    content += `<li>${node}: +${count}</li>`;
                }
            }
        } else if (plotState === 'next_available' || plotState === 'locked') {
            content += '<li class="tooltip-list-header">Requisitos para desbloquear:</li>';
            if (Object.keys(requirements).length === 0) {
                content += '<li>Disponível na próxima ilha.</li>';
            } else {
                for (const [req, value] of Object.entries(requirements)) {
                    content += `<li>${req}: ${value}</li>`;
                }
            }
        }
        content += '</ul>';

        // Exibe o tooltip
        tooltip.innerHTML = content;
        tooltip.style.display = 'block';
    }, true); // Usa captura de evento para garantir que o listener do plot seja ativado

    // Evento para mover o mouse sobre um lote (para posicionar o tooltip)
    mapTabContent.addEventListener('mousemove', (event) => {
        const plot = (event.target as HTMLElement).closest('.map-plot');
        if (!plot) return;

        const activePane = plot.closest('.tab-pane');
        if (!activePane) return;

        const tooltip = activePane.querySelector<HTMLElement>('.map-tooltip');
        if (tooltip && tooltip.style.display === 'block') {
            const offsetX = 5;
            const offsetY = 5;
            tooltip.style.left = `${event.clientX + offsetX}px`;
            tooltip.style.top = `${event.clientY + offsetY}px`;
        }
    }, true);

    // Evento para quando o mouse sai da área do mapa
    mapTabContent.addEventListener('mouseleave', hideAllTooltips, true);
}


/**
 * NOVO: Configura o redimensionamento dinâmico do mapa da fazenda para evitar barras de rolagem.
 */
export function setupDynamicMapResizing() {
    const mapTabEl = document.querySelector('#layout-map-tab');
    if (!mapTabEl) return;

    // Função para injetar ou remover o estilo dinâmico
    const updateMapStyle = (numColumns: number, containerWidth: number) => {
        const existingStyle = document.getElementById('map-resize-style');
        if (existingStyle) {
            existingStyle.remove();
        }

        const baseCellSize = 40; // Tamanho base da célula do style.css
        const borderSize = 2; // 1px de borda em cada lado
        const requiredWidth = numColumns * (baseCellSize + borderSize);

        if (requiredWidth > containerWidth) {
            // Calcula o novo tamanho e garante que não seja muito pequeno
            const newCellSize = Math.max(20, Math.floor(containerWidth / numColumns) - borderSize);
            const newIconSize = Math.max(16, newCellSize - 4);

            const style = document.createElement('style');
            style.id = 'map-resize-style';
            style.innerHTML = `
                .farm-layout-cell, .farm-layout-cell-empty {
                    width: ${newCellSize}px !important;
                    height: ${newCellSize}px !important;
                }
                .amount-label, .cell-badge {
                    font-size: 0.55rem !important; /* Reduz o tamanho da fonte dos badges */
                    padding: 1px 3px !important;
                }
            `;
            document.head.appendChild(style);
        }
    };

    const handleResize = () => {
        const mapWrapper = document.getElementById('farm-map-table-wrapper');
        if (!mapWrapper) return;
        
        const firstRow = mapWrapper.querySelector('table tbody tr');
        if (!firstRow) return;

        const numColumns = firstRow.children.length;
        if (numColumns === 0) return;
        
        updateMapStyle(numColumns, mapWrapper.clientWidth);
    };

    // Listener para quando a aba do mapa se torna visível
    mapTabEl.addEventListener('shown.bs.tab', () => setTimeout(handleResize, 50));

    // Listener para redimensionamento da janela (com debounce)
    let resizeTimeout: number;
    window.addEventListener('resize', () => {
        if (mapTabEl.classList.contains('active')) {
            clearTimeout(resizeTimeout);
            resizeTimeout = window.setTimeout(handleResize, 200);
        }
    });

    // Verificação inicial caso a aba já esteja ativa no carregamento da página
    if (mapTabEl.classList.contains('active')) {
        setTimeout(handleResize, 150);
    }
}

/**
 * Configura o filtro interativo para o mapa da fazenda.
 * Lida com cliques nos itens da legenda (recursos e AOE) para destacar
 * as células relevantes no mapa.
 */
export function setupFarmMapFilter() {
    const mapWrapper = document.querySelector('.farm-layout-map');
    if (!mapWrapper) {
        return;
    }

    // CORREÇÃO: Declara allTriggers aqui para que ambos os listeners possam acessá-lo.
    const allTriggers = mapWrapper.querySelectorAll<HTMLElement>('[data-filter-id]');

    // CORREÇÃO: Seleciona tanto as células da tabela quanto os itens de sobreposição para o filtro.
    const filterableItems = mapWrapper.querySelectorAll<HTMLElement>('.farm-layout-cell, .map-item-overlay');
    let activeFilterId: string | null = null;

    const applyFilter = () => {
        // Se nenhum filtro estiver ativo, remove o escurecimento de todos os itens.
        if (!activeFilterId) {
            filterableItems.forEach(item => item.classList.remove('is-dimmed'));
            return;
        }

        // A partir daqui, o compilador sabe que activeFilterId é uma string.
        // Atribuí-lo a uma nova constante ajuda a manter a inferência de tipo dentro do loop.
        const currentFilter = activeFilterId;

        // Itera sobre cada item (célula, overlay, edifício) para decidir se deve ser destacado ou escurecido.
        filterableItems.forEach(item => {
            const aoeSourceId = item.dataset.aoeSourceId;
            const resourceFilterId = item.dataset.resourceFilterId;
            const aoeSourcesStr = item.dataset.aoeSources || '';
            const aoeSources = aoeSourcesStr.split(' ');

            // NOVO: Verifica se o item é um edifício que contém a cultura filtrada.
            const greenhousePlants = item.dataset.greenhousePlants || '';
            const cropMachinePlants = item.dataset.cropMachinePlants || '';

            // A célula deve ser destacada se:
            // 1. É a própria fonte do filtro (seja AOE ou recurso).
            // 2. É um recurso que corresponde ao filtro.
            // 3. Está dentro da área de efeito de uma AOE que corresponde ao filtro.
            // 4. É um edifício (Greenhouse/Crop Machine) que contém a cultura filtrada.
            const shouldHighlight = aoeSourceId === currentFilter ||
                                    resourceFilterId === currentFilter ||
                                    aoeSources.includes(currentFilter) ||
                                    greenhousePlants.split(' ').includes(currentFilter) ||
                                    cropMachinePlants.split(' ').includes(currentFilter);

            item.classList.toggle('is-dimmed', !shouldHighlight);
        });
    };

    // NOVO: Ouve o evento 'clear-filter' disparado pelo summary_card.ts
    // para desativar o filtro visual.
    mapWrapper.addEventListener('clear-filter', () => {
        activeFilterId = null;
        allTriggers.forEach(t => t.classList.remove('active'));
        applyFilter();
    });
    // Usa delegação de evento no contêiner do mapa para mais eficiência.
    mapWrapper.addEventListener('click', (event) => {
        const target = event.target as HTMLElement;
        // Encontra o gatilho de filtro mais próximo que foi clicado.
        const trigger = target.closest<HTMLElement>('[data-filter-id]');

        if (!trigger) {
            return; // Sai se o clique não foi em um gatilho de filtro.
        }

        event.preventDefault();
        const clickedFilterId = trigger.dataset.filterId;

        if (!clickedFilterId) return;

        // Se o gatilho clicado já está ativo, desativa-o.
        if (trigger.classList.contains('active')) {
            activeFilterId = null;
            trigger.classList.remove('active');
        } else {
            // Caso contrário, desativa todos os outros e ativa o clicado.
            allTriggers.forEach(t => t.classList.remove('active'));
            trigger.classList.add('active');
            activeFilterId = clickedFilterId;

            // NOVO: Rola a tela para o primeiro recurso correspondente ao filtro
            if (activeFilterId) {
                // CORREÇÃO: O seletor agora inclui os atributos de plantas para encontrar o edifício correto.
                const firstElement = mapWrapper.querySelector<HTMLElement>(
                    `[data-resource-filter-id="${activeFilterId}"], [data-aoe-source-id="${activeFilterId}"], [data-greenhouse-plants~="${activeFilterId}"], [data-crop-machine-plants~="${activeFilterId}"]`
                );
        
                if (firstElement) {
                    firstElement.scrollIntoView({
                        behavior: 'smooth', // Rolagem suave
                        block: 'center'      // Tenta centralizar o elemento verticalmente
                    });
                }
            }
        }

        applyFilter();
    });
}