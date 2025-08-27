// typescript/dashboard.ts
import { CurrencyConverter } from './currency_converter.js';
import { FloatingControlPanel } from './floating_panel.js';
import { ResourceInfoCard } from './resource_info_card.js';

// Declara o objeto global do Bootstrap para que o TypeScript o reconheça.
declare const bootstrap: any;

// Estende a interface global Window para informar ao TypeScript sobre nossa nova propriedade.
declare global {
    interface Window {
        currencyConverter: CurrencyConverter;
    }
}
/**
 * NOVO: Inicializa as funcionalidades que dependem do conversor de moeda.
 * Esta função agora busca as taxas de câmbio de forma assíncrona e, em seguida,
 * inicializa o conversor e o painel de controle flutuante.
 */
async function initializeCurrencyFeatures() {
    // Usa o novo método de fábrica estático para criar a instância do conversor.
    // Isso encapsula a chamada de API dentro da própria classe CurrencyConverter.
    const converter = await CurrencyConverter.create();

    if (converter) {
        // Anexa a instância à `window` para que possa ser acessada por outros scripts e filtros.
        window.currencyConverter = converter;
        // Inicializa o painel de controle flutuante, que depende do conversor.
        const panel = new FloatingControlPanel(converter);
        panel.init();
        console.log("Conversor de moeda e painel de controle inicializados com sucesso.");
    } else {
        // Se a criação falhar, exibe um erro e as funcionalidades de moeda não serão ativadas.
        console.error("Falha ao inicializar o conversor de moeda. As funcionalidades de moeda estarão desativadas.");
    }
}

/**
 * Inicializa todos os componentes interativos do Bootstrap, como Popovers e Tooltips.
 * Esta função deve ser chamada uma vez, após o carregamento do DOM.
 */
function setupBootstrapComponents() {
    // CORREÇÃO: Adiciona um ouvinte de evento explícito para garantir que as abas funcionem.
    // A inicialização anterior não era suficiente para resolver o conflito.
    const triggerTabList = document.querySelectorAll('[data-bs-toggle="tab"]');
    triggerTabList.forEach(triggerEl => {
        // Cria a instância do Tab do Bootstrap
        const tab = new bootstrap.Tab(triggerEl);
        // Adiciona um ouvinte de clique que força a exibição da aba.
        triggerEl.addEventListener('click', (event: Event) => {
            event.preventDefault(); // Previne o comportamento padrão do link/botão
            tab.show(); // Usa o método .show() do Bootstrap para exibir a aba correta
        });
    });

    // Inicializa todos os Popovers na página.
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    popoverTriggerList.forEach(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl, {
        // Usar 'body' como container evita problemas de posicionamento dentro de tabelas ou outros componentes complexos.
        container: 'body'
    }));

    // Inicializa todos os Tooltips na página.
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
}

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
 * NOVO: Atualiza o estado visual do botão "Ver Dicas".
 * @param isActive Define se o botão deve estar no estado ativo (balão visível) ou inativo.
 */
function updateHintsButtonState(isActive: boolean) {
    const button = document.getElementById('toggle-hints-balloon-btn');
    if (!button) return;

    const textSpan = button.querySelector<HTMLSpanElement>('.button-text');

    if (isActive) {
        button.classList.add('active');
        if (textSpan) textSpan.textContent = 'Dicas Ativas';
    } else {
        button.classList.remove('active');
        if (textSpan) textSpan.textContent = 'Ver Dicas';
    }
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
                // --- MELHORIA DE USABILIDADE ---
                // Verifica se o balão de dicas estava visível antes de substituir o HTML.
                const oldBalloon = panelWrapper.querySelector('#hints-balloon');
                const wasBalloonVisible = oldBalloon ? !oldBalloon.classList.contains('d-none') : false;

                panelWrapper.innerHTML = data.html;

                // Se o balão estava visível, remove a classe 'd-none' do novo balão.
                if (wasBalloonVisible) {
                    panelWrapper.querySelector('#hints-balloon')?.classList.remove('d-none');
                    // E também atualiza o estado do botão para "ativo"
                    updateHintsButtonState(true);
                } else {
                    // Garante que o botão esteja no estado correto se o balão estava fechado
                    updateHintsButtonState(false);
                }

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
 * Configura a interatividade do painel de dicas flutuante.
 * Esta função lida com:
 * 1. Mostrar/esconder o balão ao clicar no botão "Ver Dicas".
 * 2. Arrastar o balão pela tela.
 * 3. Recolher/expandir o conteúdo do balão ao clicar no seu cabeçalho.
 */
function setupFloatingHintsPanel() {
	const panelWrapper = document.getElementById('treasure-dig-panel-wrapper');
	if (!panelWrapper) return;

	// --- Lógica para MOSTRAR/ESCONDER o balão ---
	panelWrapper.addEventListener('click', (event: MouseEvent) => {
		const target = event.target as HTMLElement;
		const toggleBtn = target.closest<HTMLButtonElement>('#toggle-hints-balloon-btn');
		if (toggleBtn) {
			const balloon = document.getElementById('hints-balloon');
            // Adiciona uma verificação para garantir que o balão existe antes de manipulá-lo.
            // Isso previne um erro 'TypeError' se o botão for clicado mas o balão não estiver no DOM.
            if (!balloon) {
                return;
            }
			balloon.classList.toggle('d-none');
            updateHintsButtonState(!balloon.classList.contains('d-none'));
		}
	});
 
	// --- Lógica para EFEITO DE OCIOSIDADE ---
	let idleTimer: number;
	const IDLE_TIMEOUT = 5000; // 5 segundos para considerar ocioso

	const resetIdleTimer = () => {
		// Busca o balão dinamicamente, pois ele pode ser recriado.
		const balloon = document.getElementById('hints-balloon');
		if (balloon) {
			balloon.classList.remove('is-idle');
			clearTimeout(idleTimer);
			idleTimer = window.setTimeout(() => {
				const currentBalloon = document.getElementById('hints-balloon');
				currentBalloon?.classList.add('is-idle');
			}, IDLE_TIMEOUT);
		}
	};

	// Inicia e reinicia o timer em qualquer atividade do usuário na página
	['mousemove', 'mousedown', 'keydown', 'scroll', 'touchstart'].forEach(event => {
		document.addEventListener(event, resetIdleTimer);
	});
	// Também reinicia quando o painel é atualizado para garantir o estado correto
	panelWrapper.addEventListener('panelUpdated', resetIdleTimer);

	// --- Lógica para ARRASTAR o balão ---
	panelWrapper.addEventListener('mousedown', (e: MouseEvent) => {
		const target = e.target as HTMLElement;
		const header = target.closest<HTMLElement>('#hints-balloon-header');
		const balloon = target.closest<HTMLElement>('#hints-balloon');

		if (!header || !balloon) return;

		// Prevent default browser behavior like text selection
		e.preventDefault();

		// Adiciona uma classe para desativar a transição CSS durante o arrasto
		balloon.classList.add('is-dragging-balloon');

		// Get the initial position of the balloon and the mouse using getBoundingClientRect(),
		// which is always relative to the viewport and more reliable than offsetLeft/Top.
		const rect = balloon.getBoundingClientRect();
		const offsetX = e.clientX - rect.left;
		const offsetY = e.clientY - rect.top;

		// This is crucial for the first drag when the element is positioned with bottom/right.
		// It switches the element to be positioned by top/left.
		if (balloon.style.right !== 'auto' || balloon.style.bottom !== 'auto') {
			balloon.style.left = `${rect.left}px`;
			balloon.style.top = `${rect.top}px`;
			balloon.style.right = 'auto';
			balloon.style.bottom = 'auto';
		}

		document.body.classList.add('is-dragging');

		const onMouseMove = (moveEvent: MouseEvent) => {
			// Calculate the new top/left position based on the mouse movement and the initial offset.
			const newLeft = moveEvent.clientX - offsetX;
			const newTop = moveEvent.clientY - offsetY;

			balloon.style.left = `${newLeft}px`;
			balloon.style.top = `${newTop}px`;
		};

		const onMouseUp = () => {
			document.removeEventListener('mousemove', onMouseMove);
			document.removeEventListener('mouseup', onMouseUp);
			document.body.classList.remove('is-dragging');
			// Remove a classe para reativar a transição CSS
			balloon.classList.remove('is-dragging-balloon');
		};

		document.addEventListener('mousemove', onMouseMove);
		document.addEventListener('mouseup', onMouseUp);
	});
}

/**
 * NOVO: Configura o redimensionamento dinâmico do mapa da fazenda para evitar barras de rolagem.
 */
function setupDynamicMapResizing() {
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
function setupFarmMapFilter() {
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

/**
 * NOVO: Configura a lógica para fechar os painéis flutuantes (cards de detalhes, resumo, dicas)
 * quando o usuário clica em qualquer lugar fora deles.
 */
function setupClickAwayClosers(): void {
    document.addEventListener('mousedown', (event: MouseEvent) => {
        const target = event.target as HTMLElement;

        // --- Card de Detalhes do Recurso ---
        const resourceCard = document.getElementById('floating-resource-card');
        if (resourceCard && resourceCard.style.display !== 'none') {
            // Não fecha se o clique for dentro do card ou no gatilho que o abriu.
            if (!resourceCard.contains(target) && !target.closest('.resource-info-trigger')) {
                resourceCard.style.display = 'none';
            }
        }

        // --- Card de Resumo (da legenda) e Filtros de AOE ---
        const summaryCard = document.getElementById('floating-summary-card');
        const mapWrapper = document.querySelector<HTMLElement>('.farm-layout-map');
        // Procura por QUALQUER filtro ativo, seja de recurso ou de AOE.
        const activeFilter = mapWrapper?.querySelector<HTMLElement>('.resource-filter-trigger.active, .aoe-filter-trigger.active');

        // A lógica de fechar/limpar é acionada se um filtro estiver ativo OU o card de resumo estiver visível.
        if (activeFilter || (summaryCard && summaryCard.style.display !== 'none')) {
            // Um clique é considerado "fora" se não for no card de resumo E não for em NENHUM gatilho de filtro.
            const isClickOnSummaryCard = summaryCard ? summaryCard.contains(target) : false;
            const isClickOnAnyFilterTrigger = target.closest('.resource-filter-trigger, .aoe-filter-trigger');

            if (!isClickOnSummaryCard && !isClickOnAnyFilterTrigger) {
                if (mapWrapper) {
                    // Este evento é capturado por `setupFarmMapFilter` para limpar o filtro visual.
                    mapWrapper.dispatchEvent(new CustomEvent('clear-filter'));
                }
                if (summaryCard) {
                    summaryCard.style.display = 'none';
                }
            }
        }

        // --- Balão de Dicas (Escavação de Tesouros) ---
        const hintsBalloon = document.getElementById('hints-balloon');
        if (hintsBalloon && !hintsBalloon.classList.contains('d-none')) {
            // Não fecha se o clique for dentro do balão ou no botão que o alterna.
            if (!hintsBalloon.contains(target) && !target.closest('#toggle-hints-balloon-btn')) {
                hintsBalloon.classList.add('d-none');
                updateHintsButtonState(false); // Atualiza o estado do botão "Ver Dicas".
            }
        }
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
        // NOVO: Usa generateCurrencyHTML para criar todos os spans de uma vez.
        totalCostEl.innerHTML = window.currencyConverter.generateCurrencyHTML(sflValue);
    }

    // Preenche o Custo Relativo
    const totalRelativeCostEl = mainClone.querySelector('[data-template="total-relative-cost"]');
    if (totalRelativeCostEl && data.total_relative_sfl_cost) {
        const sflValue = parseFloat(data.total_relative_sfl_cost);
        // NOVO: Usa generateCurrencyHTML para criar todos os spans de uma vez.
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
                const sflValueNum = parseFloat(item.sfl_value);
                // CORREÇÃO: Usa `innerHTML` em vez de `outerHTML`.
                // Isso preserva a tag <small> original e seu estilo (font-size: 0.75em),
                // garantindo que o container de moeda herde o tamanho de fonte correto.
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
 * Ponto de entrada principal do script.
 * Executa quando todo o conteúdo HTML da página foi carregado.
 */
document.addEventListener('DOMContentLoaded', async () => {
    // Inicializa todas as funcionalidades da página.
    // A inicialização da moeda agora é assíncrona e tratada separadamente.
    initializeCurrencyFeatures();

    setupGoalForm();
    setupMilestoneInteraction();
    setupExpansionCountdown();
    setupAllProgressBars();
    setupInteractiveMap();
    setupPanelInteractivity('fishing');
    setupPanelInteractivity('flowers');
    setupGenericFilters();
    setupTreasureDigUpdater();
    setupHintHighlighter();
    setupFloatingHintsPanel();
    setupBootstrapComponents();
    setupDynamicMapResizing();
    setupFarmMapFilter();
    setupClickAwayClosers();
    // NOVO: Inicializa o card de informações de recurso a partir da sua própria classe.
    new ResourceInfoCard().init();
});

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
            // Adiciona um bloco try-catch para evitar que um seletor inválido
            // no HTML quebre a execução de todo o script.
            try {
                const elements = document.querySelectorAll(targetSelector);
                if (elements.length > 0) {
                    filterTargets.set(targetSelector, {
                        elements: elements,
                        activeFilters: {}
                    });
                }
            } catch (e) {
                console.error(`Seletor inválido encontrado em data-filter-target: "${targetSelector}"`, e);
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