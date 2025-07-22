// typescript/dashboard.ts

/**
 * Ponto de entrada principal do script.
 * Executa quando todo o conteúdo HTML da página foi carregado.
 */
document.addEventListener('DOMContentLoaded', () => {
    
    // Configura a interatividade do formulário de metas de expansão.
    setupGoalForm();

    // Configura a interatividade do painel de conquistas de pesca.
    setupMilestoneInteraction();
    
    // Configura o contador regressivo para a expansão em andamento, se existir.
    setupExpansionCountdown();

    // Configura a largura inicial de todas as barras de progresso na página.
    setupAllProgressBars();

    // Configura toda a interatividade do mapa de expansão (filtros e tooltips).
    setupInteractiveMap();

    // Configura o filtro de peixes por temporada.
    setupFishingFilters();

    // Configura o filtro dos cabeçalhos (no inventario, capturados).
    setupTableSorters();});


/**
 * Propósito: Configurar o formulário "Meta Final".
 * Adiciona um ouvinte de evento que, ao submeter, busca os dados da API
 * e chama a função para renderizar os resultados do plano de expansão.
 */
function setupGoalForm() {
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
 * Propósito: Configurar a interatividade do painel de conquistas.
 */
function setupMilestoneInteraction() {
    const miniCardsContainer = document.querySelector('.milestones-mini-cards-container');
    const detailsWrapper = document.getElementById('milestone-accordion-parent');
    if (!miniCardsContainer || !detailsWrapper) return;

    const miniCards = miniCardsContainer.querySelectorAll('.milestone-mini-card');
    const collapseElements = detailsWrapper.querySelectorAll('.collapse');

    collapseElements.forEach(collapseEl => {
        collapseEl.addEventListener('show.bs.collapse', (event) => {
            const target = event.target as HTMLElement;
            const triggerCard = document.querySelector(`[href="#${target.id}"]`);
            miniCards.forEach(card => {
                card.classList.toggle('active', card === triggerCard);
                card.classList.toggle('is-inactive', card !== triggerCard);
            });
        });

        collapseEl.addEventListener('hide.bs.collapse', () => {
            miniCards.forEach(card => card.classList.remove('active', 'is-inactive'));
        });
    });
}


/**
 * Propósito: Ler o valor de progresso de todas as barras e definir a sua largura visual.
 */
function setupAllProgressBars() {
    const allProgressBars = document.querySelectorAll('.progress-bar');
    allProgressBars.forEach(bar => {
        const progressBar = bar as HTMLElement;
        const progressValue = progressBar.getAttribute('aria-valuenow');
        if (progressValue) {
            progressBar.style.width = progressValue + '%';
        }
    });
}


/**
 * Propósito: Renderizar os resultados do plano de expansão na secção "Meta Final".
 */
function renderGoalResults(data: any) {
    // --- Parte 1: Setup dos templates e containers ---
    const resultsContainer = document.getElementById('goal-results-container');
    const mainTemplate = document.getElementById('goal-list-template') as HTMLTemplateElement;
    const itemTemplate = document.getElementById('goal-list-item-template') as HTMLTemplateElement;
    
    // NOVOS templates para a tabela de resumo
    const summaryTableTemplate = document.getElementById('unlocks-summary-table-template') as HTMLTemplateElement;
    const summaryItemTemplate = document.getElementById('unlocks-summary-item-template') as HTMLTemplateElement;

    // Verificação de segurança para garantir que todos os templates existem
    if (!resultsContainer || !mainTemplate || !itemTemplate || !summaryTableTemplate || !summaryItemTemplate) {
        console.error("Um ou mais templates para renderizar os resultados não foram encontrados.");
        return;
    }

    resultsContainer.innerHTML = ''; // Limpa os resultados anteriores
    const mainClone = mainTemplate.content.cloneNode(true) as DocumentFragment;

    // --- Parte 2: Preenche as informações gerais do plano (sem alterações aqui) ---
    const goalLevelEl = mainClone.querySelector('[data-template="goal-level"]');
    if (goalLevelEl) goalLevelEl.textContent = data.goal_level_display;

    const goalLandTypeEl = mainClone.querySelector('[data-template="goal-land-type"]');
    if (goalLandTypeEl) goalLandTypeEl.textContent = data.goal_land_type;
    
    const bumpkinLevelEl = mainClone.querySelector('[data-template="bumpkin-level"]');
    if(bumpkinLevelEl) bumpkinLevelEl.textContent = data.max_bumpkin_level;

    const totalTimeEl = mainClone.querySelector('[data-template="total-time"]');
    if(totalTimeEl) totalTimeEl.textContent = data.total_time_str;
    
    const totalCostEl = mainClone.querySelector('[data-template="total-cost"]');
    if (totalCostEl) {
        const totalCostFormatted = parseFloat(data.total_sfl_cost).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        totalCostEl.textContent = totalCostFormatted;
    }

    // --- Parte 3: Renderiza a lista de requisitos (sem alterações aqui) ---
    const column1 = mainClone.querySelector('[data-column="1"]');
    const column2 = mainClone.querySelector('[data-column="2"]');

    if (column1 && column2 && data.requirements) {
        data.requirements.forEach((item: any, index: number) => {
            const itemClone = itemTemplate.content.cloneNode(true) as DocumentFragment;
            
            const iconEl = itemClone.querySelector<HTMLImageElement>('[data-template="icon"]');
            if (iconEl) iconEl.src = item.icon;
            
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

            if (index % 2 === 0) {
                column1.appendChild(itemClone);
            } else {
                column2.appendChild(itemClone);
            }
        });
    }

    // Adiciona a primeira parte (requisitos) ao container
    resultsContainer.appendChild(mainClone);

    // --- Parte 4: Renderiza os Desbloqueios e Ganhos (LÓGICA CORRIGIDA E ATUALIZADA) ---
    const unlocksData = data.unlocks;
    const summaryList = unlocksData?.summary; // Usando a nova estrutura de dados 'summary'

    if (summaryList && summaryList.length > 0) {
        // Usa os novos templates de tabela
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
                    // Determina a pasta do ícone com base no tipo do item
                    const iconType = item.type === 'building' ? 'buildings' : 'nodes';
                    icon.src = `/static/images/${iconType}/${item.name.toLowerCase().replace(/ /g, '_')}.png`;
                }
                if (name) name.textContent = item.name;
                if (total) total.textContent = `+${item.total}`;

                // Cria o texto para o tooltip dinamicamente
                let tooltipTitle = 'Ganhos por Nível:\n';
                // Itera sobre os detalhes de cada item
                for (const [level, count] of Object.entries(item.details)) {
                    tooltipTitle += `- Nível ${level}: +${count}\n`;
                }
                
                // Adiciona o tooltip à linha da tabela (<tr>)
                if (row) {
                    row.title = tooltipTitle.trim();
                }

                tableBody.appendChild(itemClone);
            });
        }
        // Adiciona a tabela de ganhos ao container de resultados
        resultsContainer.appendChild(tableClone);
    }
}


/**
 * Propósito: Configurar e gerir o contador regressivo para uma expansão em andamento.
 */
function setupExpansionCountdown() {
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
 */
function setupInteractiveMap() {
    const mapGrid = document.getElementById('expansion-map-grid');
    const filterTabs = document.getElementById('map-filter-tabs');
    const tooltip = document.getElementById('map-tooltip') as HTMLElement;

    if (!mapGrid || !filterTabs || !tooltip) return;

    const allPlots = Array.from(mapGrid.querySelectorAll('.map-plot')) as HTMLElement[];

    filterTabs.addEventListener('click', (event) => {
        const target = event.target as HTMLButtonElement;
        if (target.tagName !== 'BUTTON') return;
        const filter = target.dataset.islandFilter;
        filterTabs.querySelectorAll('button').forEach(btn => btn.classList.remove('active'));
        target.classList.add('active');
        allPlots.forEach(plot => {
            plot.classList.toggle('is-filtered', !(filter === 'all' || filter === plot.dataset.plotIsland));
        });
    });

    allPlots.forEach(plot => {
        plot.addEventListener('mouseenter', () => {
            const requirements = JSON.parse(plot.dataset.plotRequirements || '{}');
            const nodes = JSON.parse(plot.dataset.plotNodes || '{}');
            const plotState = plot.dataset.plotState;
            const plotNumber = plot.dataset.plotNumber;

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
            tooltip.innerHTML = content;
            tooltip.style.display = 'block';
        });

        plot.addEventListener('mousemove', (event) => {
            const offsetX = 5;
            const offsetY = 5;
            tooltip.style.left = `${event.clientX + offsetX}px`;
            tooltip.style.top = `${event.clientY + offsetY}px`;
        });

        plot.addEventListener('mouseleave', () => {
            tooltip.style.display = 'none';
        });
    });
}

function setupFishingFilters() {
    const seasonFilters = document.getElementById('season-filter-buttons');
    const typeFilters = document.getElementById('fishtype-filter-buttons');
    
    // Alvos do filtro
    const fishRows = document.querySelectorAll('#fishingLogAccordion > tr[data-fishtype]');
    const codexItems = document.querySelectorAll('.codex-item[data-fishtype]');

    if (!seasonFilters || !typeFilters) return;

    let currentSeasonFilter = 'all';
    let currentTypeFilter = 'all';

    function applyFilters() {
        // Filtra o Diário de Pesca
        fishRows.forEach(rowEl => {
            const row = rowEl as HTMLElement;
            const itemSeasons = row.dataset.seasons || '';
            const itemType = row.dataset.fishtype || '';

            const seasonMatch = currentSeasonFilter === 'all' || itemSeasons.includes(currentSeasonFilter);
            const typeMatch = currentTypeFilter === 'all' || itemType === currentTypeFilter;

            const shouldShow = seasonMatch && typeMatch;
            row.style.display = shouldShow ? '' : 'none';
            const detailsRow = row.nextElementSibling;
            if (detailsRow) (detailsRow as HTMLElement).style.display = shouldShow ? '' : 'none';
        });

        // Filtra o Códice Visual
        codexItems.forEach(itemEl => {
            const item = itemEl as HTMLElement;
            const itemSeasons = item.dataset.seasons || '';
            const itemType = item.dataset.fishtype || '';

            const seasonMatch = currentSeasonFilter === 'all' || itemSeasons.includes(currentSeasonFilter);
            const typeMatch = currentTypeFilter === 'all' || itemType === currentTypeFilter;
            
            item.style.display = (seasonMatch && typeMatch) ? 'flex' : 'none'; // Usar flex para manter o layout
        });
    }

    seasonFilters.addEventListener('click', (event) => {
        const button = (event.target as HTMLElement).closest('button');
        if (!button) return;
        currentSeasonFilter = button.dataset.season || 'all';
        seasonFilters.querySelectorAll('button').forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        applyFilters();
    });

    typeFilters.addEventListener('click', (event) => {
        const button = (event.target as HTMLElement).closest('button');
        if (!button) return;
        currentTypeFilter = button.dataset.fishtype || 'all';
        typeFilters.querySelectorAll('button').forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        applyFilters();
    });
}

function setupTableSorters() {
    const tableBody = document.getElementById('fishingLogAccordion');
    // Seleciona os cabeçalhos pela classe que já adicionámos
    const headers = document.querySelectorAll('.sortable-header');

    if (!tableBody || headers.length === 0) return;

    // Guarda o estado da ordenação para cada coluna
    const sortState: { [key: string]: boolean } = {};

    headers.forEach(header => {
        header.addEventListener('click', () => {
            const sortBy = (header as HTMLElement).dataset.sort;
            if (!sortBy) return;

            // Inicia ou inverte a direção da ordenação para esta coluna
            sortState[sortBy] = !sortState[sortBy];
            const isAscending = sortState[sortBy];

            // 1. Agrupa as linhas em pares (item + detalhes)
            const rows = Array.from(tableBody.children);
            const rowPairs: [HTMLElement, HTMLElement][] = [];
            for (let i = 0; i < rows.length; i += 2) {
                rowPairs.push([rows[i] as HTMLElement, rows[i + 1] as HTMLElement]);
            }

            // 2. Ordena os pares com base no data-value
            rowPairs.sort((pairA, pairB) => {
                const dataRowA = pairA[0];
                const dataRowB = pairB[0];
                
                // Seletor CORRIGIDO para encontrar a célula pelo seu data-key
                const cellA = dataRowA.querySelector(`td[data-key="${sortBy}"]`);
                const cellB = dataRowB.querySelector(`td[data-key="${sortBy}"]`);

                const valueA = parseFloat(cellA?.getAttribute('data-value') || '0');
                const valueB = parseFloat(cellB?.getAttribute('data-value') || '0');
                
                return isAscending ? valueA - valueB : valueB - valueA;
            });

            // 3. Re-insere as linhas ordenadas no corpo da tabela
            rowPairs.forEach(pair => {
                tableBody.appendChild(pair[0]);
                tableBody.appendChild(pair[1]);
            });
        });
    });
}