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

    // Configura a interatividade para cada painel de forma genérica
    setupPanelInteractivity('fishing');
    setupPanelInteractivity('flowers');

    // NOVO: Configura todos os filtros genéricos da página (incluindo o de NPCs)
    setupGenericFilters();

    // NOVO: Configura o botão de atualização do painel de tesouros.
    setupTreasureDigUpdater();

    // NOVO: Configura o realce do grid de tesouros ao passar o mouse sobre as dicas.
    setupHintHighlighter();
    
});

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
 * Configura o botão de atualização para o painel de escavação de tesouros.
 * Usa delegação de evento para funcionar mesmo após o painel ser recarregado via AJAX.
 */
function setupTreasureDigUpdater() {
    const COOLDOWN_SECONDS = 10;

    /**
     * Desativa um botão e exibe um contador regressivo.
     * @param button O elemento do botão para aplicar o cooldown.
     */
    const startCooldown = (button: HTMLButtonElement) => {
        button.disabled = true;
        const icon = button.querySelector<HTMLElement>('i.bi-arrow-clockwise');
        const spinner = button.querySelector<HTMLElement>('.spinner-border');
        const timerSpan = button.querySelector<HTMLSpanElement>('.cooldown-timer');

        if (!timerSpan) return;

        // Esconde outros elementos e mostra o timer
        icon?.classList.add('d-none');
        spinner?.classList.add('d-none');
        timerSpan.classList.remove('d-none');

        let secondsLeft = COOLDOWN_SECONDS;
        timerSpan.textContent = `(${secondsLeft}s)`;

        const interval = setInterval(() => {
            secondsLeft--;
            if (timerSpan) timerSpan.textContent = `(${secondsLeft}s)`;
            
            if (secondsLeft <= 0) {
                clearInterval(interval);
                button.disabled = false;
                timerSpan?.classList.add('d-none');
                icon?.classList.remove('d-none');
            }
        }, 1000);
    };

    // Cooldown inicial ao carregar a página
    const initialButton = document.querySelector<HTMLButtonElement>('#update-treasure-dig-btn');
    if (initialButton) {
        startCooldown(initialButton);
    }

    // Ouvinte de evento para cliques
    document.addEventListener('click', async (event) => {
        const target = event.target as HTMLElement;
        // Encontra o botão de atualização, mesmo que o clique seja em um ícone dentro dele
        const updateButton = target.closest<HTMLButtonElement>('#update-treasure-dig-btn');

        if (!updateButton || updateButton.disabled) return;

        const farmId = updateButton.dataset.farmId;
        const icon = updateButton.querySelector<HTMLElement>('i.bi-arrow-clockwise');
        const spinner = updateButton.querySelector<HTMLElement>('.spinner-border');
        const timerSpan = updateButton.querySelector<HTMLSpanElement>('.cooldown-timer');
        const panelWrapper = document.getElementById('treasure-dig-panel-wrapper');

        if (!farmId || !panelWrapper) {
            console.error("Botão de atualização ou painel wrapper não encontrado.");
            return;
        }

        // Mostra o estado de carregamento (spinner)
        updateButton.disabled = true;
        icon?.classList.add('d-none');
        timerSpan?.classList.add('d-none');
        spinner?.classList.remove('d-none');

        try {
            const response = await fetch(`/api/farm/${farmId}/treasure_dig_update`);
            if (!response.ok) {
                throw new Error(`A resposta da rede não foi OK (${response.status}).`);
            }
            const data = await response.json();

            if (data.success) {
                panelWrapper.innerHTML = data.html;
                // Após a atualização, encontra o novo botão e inicia seu cooldown
                const newButton = document.querySelector<HTMLButtonElement>('#update-treasure-dig-btn');
                if (newButton) {
                    startCooldown(newButton);
                }
                // Dispara um evento customizado para notificar outros scripts que o painel foi atualizado
                panelWrapper.dispatchEvent(new CustomEvent('panelUpdated'));
            } else {
                console.error('Erro ao atualizar:', data.error);
                alert('Falha ao buscar dados atualizados. Tente novamente.');
                startCooldown(updateButton); // Inicia cooldown mesmo em caso de falha
            }
        } catch (error) {
            console.error('Erro na requisição fetch:', error);
            alert('Ocorreu um erro de rede. Verifique sua conexão e tente novamente.');
            startCooldown(updateButton); // Inicia cooldown em caso de erro de rede
        }
    });
}

/**
 * Configura o realce no grid de escavação quando o usuário passa o mouse
 * sobre uma dica de padrão.
 */
function setupHintHighlighter() {
    // Usa delegação de evento no wrapper do painel, pois o conteúdo é dinâmico.
    const panelWrapper = document.getElementById('treasure-dig-panel-wrapper');
    if (!panelWrapper) return;

    const clearHighlights = () => {
        document.querySelectorAll('.treasure-grid-cell.hint-highlight').forEach(cell => {
            cell.classList.remove('hint-highlight');
        });
    };

    panelWrapper.addEventListener('mouseover', (event) => {
        const target = event.target as HTMLElement;
        const hintLi = target.closest<HTMLElement>('[data-highlight-coords]');

        if (hintLi) {
            // Limpa destaques anteriores para evitar sobreposição se o mouse se mover rápido
            clearHighlights();
            try {
                const coordsToHighlight: [number, number][] = JSON.parse(hintLi.dataset.highlightCoords || '[]');
                
                coordsToHighlight.forEach(([x, y]) => {
                    const cell = document.querySelector(`.treasure-grid-cell[data-x='${x}'][data-y='${y}']`);
                    cell?.classList.add('hint-highlight');
                });
            } catch (e) {
                console.error("Falha ao analisar as coordenadas de realce:", e);
            }
        }
    });

    // Limpa os destaques quando o mouse sai da área do painel que contém as dicas
    panelWrapper.addEventListener('mouseout', clearHighlights);
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
        const totalCostFormatted = parseFloat(data.total_sfl_cost).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        totalCostEl.textContent = totalCostFormatted;
    }

    // Preenche o Custo Relativo
    const totalRelativeCostEl = mainClone.querySelector('[data-template="total-relative-cost"]');
    if (totalRelativeCostEl && data.total_relative_sfl_cost) {
        const totalCostFormatted = parseFloat(data.total_relative_sfl_cost).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        totalRelativeCostEl.textContent = totalCostFormatted;
    }

    // --- Parte 3: Renderiza a lista de requisitos (com modificações) ---
    const column1 = mainClone.querySelector('[data-column="1"]');
    const column2 = mainClone.querySelector('[data-column="2"]');

    if (column1 && column2 && data.requirements) {
        data.requirements.forEach((item: any, index: number) => {
            const itemClone = itemTemplate.content.cloneNode(true) as DocumentFragment;
            
            const iconEl = itemClone.querySelector<HTMLImageElement>('[data-template="icon"]');
            if (iconEl && item.icon) {
                // Lógica simplificada: O backend sempre envia um caminho relativo.
                // O frontend apenas adiciona o prefixo /static/.
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

            // NOVO: Preenche o valor individual em SFL
            const sflValueEl = itemClone.querySelector<HTMLElement>('[data-template="sfl_value"]');
            if (sflValueEl) {
                const sflValue = parseFloat(item.sfl_value);
                sflValueEl.textContent = sflValue.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
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
                    // CORREÇÃO: O backend agora fornece o caminho relativo correto no campo 'item.icon'.
                    // O frontend apenas precisa adicionar o prefixo '/static/'.
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

/**
 * Configura a interatividade de um painel (filtros e ordenação da tabela).
 * @param panelPrefix O prefixo usado nos IDs dos elementos do painel (ex: 'fishing', 'flowers').
 */
function setupPanelInteractivity(panelPrefix: string) {
    const panel = document.getElementById(`${panelPrefix}-panel`);
    if (!panel) return;
    // A filtragem agora é tratada pelo setupGenericFilters global.
    setupPanelTableSorter(panelPrefix);
}

/**
 * Configura a ordenação para a tabela de um painel específico.
 * @param panelPrefix O prefixo do painel.
 */
function setupPanelTableSorter(panelPrefix: string) {
    const tableBody = document.getElementById(`${panelPrefix}-log-accordion`);
    const headers = document.querySelectorAll(`#${panelPrefix}-table .sortable-header`);

    if (!tableBody || headers.length === 0) return;

    const sortState: { [key: string]: boolean } = {};

    headers.forEach(header => {
        header.addEventListener('click', () => {
            const sortBy = (header as HTMLElement).dataset.sort;
            if (!sortBy) return;
            
            sortState[sortBy] = !sortState[sortBy];
            const isAscending = sortState[sortBy];

            const rows = Array.from(tableBody.children);
            const rowPairs: [HTMLElement, HTMLElement][] = [];
            for (let i = 0; i < rows.length; i += 2) {
                rowPairs.push([rows[i] as HTMLElement, rows[i + 1] as HTMLElement]);
            }

            rowPairs.sort((pairA, pairB) => {
                const dataRowA = pairA[0];
                const dataRowB = pairB[0];
                const cellA = dataRowA.querySelector(`td[data-key="${sortBy}"]`);
                const cellB = dataRowB.querySelector(`td[data-key="${sortBy}"]`);

                const valueA = parseFloat(cellA?.getAttribute('data-value') || '0');
                const valueB = parseFloat(cellB?.getAttribute('data-value') || '0');
                
                return isAscending ? valueA - valueB : valueB - valueA;
            });

            rowPairs.forEach(pair => {
                tableBody.appendChild(pair[0]);
                tableBody.appendChild(pair[1]);
            });
        });
    });
}

/**
 * NOVO: Configura todos os grupos de filtros genéricos na página.
 * Um grupo de filtro é um elemento com `data-filter-group` e `data-filter-target`.
 * Ele filtra os elementos alvo com base nos botões clicados dentro dele.
 */
function setupGenericFilters() {
    // Mapa para agrupar filtros pelo seu seletor de alvo.
    // Chave: seletor CSS (ex: '#npc-gift-accordion > .list-group-item')
    // Valor: { elements: NodeListOf<Element>, activeFilters: { [key: string]: string } }
    const filterTargets = new Map<string, { elements: NodeListOf<Element>, activeFilters: { [key: string]: string } }>();

    const filterGroups = document.querySelectorAll('[data-filter-group]');

    // 1. Agrupar todos os filtros e seus alvos
    filterGroups.forEach(groupEl => {
        const group = groupEl as HTMLElement;
        const targetSelector = group.dataset.filterTarget;
        if (!targetSelector) return;

        // Se este seletor de alvo ainda não foi visto, inicialize-o no mapa.
        if (!filterTargets.has(targetSelector)) {
            const elements = document.querySelectorAll(targetSelector);
            if (elements.length > 0) {
                filterTargets.set(targetSelector, {
                    elements: elements,
                    activeFilters: {}
                });
            }
        }
    });

    // 2. Adicionar ouvintes de evento a cada grupo de filtro
    filterGroups.forEach(groupEl => {
        const group = groupEl as HTMLElement;
        const targetSelector = group.dataset.filterTarget;
        if (!targetSelector) return;

        const targetData = filterTargets.get(targetSelector);
        if (!targetData) return;
        
        group.addEventListener('click', (event) => {
            const button = (event.target as HTMLElement).closest('button');
            if (!button) return;

            const isAlreadyActive = button.classList.contains('active');
            let filterValue = button.dataset.filterValue || 'all';
            // O atributo a ser filtrado (ex: 'seasons', 'type', 'key-reward')
            // Usa o atributo do botão se existir, senão o do grupo.
            const filterAttribute = button.dataset.filterAttribute || group.dataset.filterAttribute || '';

            if (!filterAttribute) return;

            // LÓGICA DE TOGGLE: Se clicar em um filtro já ativo (que não seja o 'todos'),
            // desativa esse filtro e volta para a visualização 'todos'.
            if (isAlreadyActive && filterValue !== 'all') {
                delete targetData.activeFilters[filterAttribute];
                button.classList.remove('active');
                const allButton = group.querySelector('button[data-filter-value="all"]');
                if (allButton) allButton.classList.add('active');
            } else {
                // Lógica original: define o filtro com base no botão clicado.
                if (filterValue === 'all') {
                    delete targetData.activeFilters[filterAttribute];
                } else {
                    targetData.activeFilters[filterAttribute] = filterValue;
                }
                // Atualiza a classe 'active' nos botões do grupo atual
                group.querySelectorAll('button').forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
            }

            // Aplica a lógica de filtragem para os elementos alvo
            targetData.elements.forEach(itemEl => {
                const item = itemEl as HTMLElement;
                let isVisible = true;

                // Verifica se o item corresponde a TODOS os filtros ativos para este alvo
                for (const attr in targetData.activeFilters) {
                    // CORREÇÃO: Converte o nome do atributo de kebab-case (ex: 'key-reward')
                    // para camelCase (ex: 'keyReward') para acessar o DOM dataset corretamente.
                    const camelCaseAttr = attr.replace(/-./g, x => x.toUpperCase()[1]);

                    const filter = targetData.activeFilters[attr];
                    const itemValue = item.dataset[camelCaseAttr] || '';
                    
                    // A lógica de `includes` é mais flexível para atributos com múltiplos valores (ex: data-seasons="spring,summer")
                    if (!itemValue.includes(filter)) {
                        isVisible = false;
                        break;
                    }
                }
                
                // Lógica para mostrar/esconder
                const isTableRow = item.matches('tr');
                item.style.display = isVisible ? '' : 'none';
                
                // Se for uma linha de tabela, também esconde a linha de detalhes seguinte
                if (isTableRow) {
                    const detailsRow = item.nextElementSibling;
                    if (detailsRow) (detailsRow as HTMLElement).style.display = isVisible ? '' : 'none';
                }
            });
        });
    });
}