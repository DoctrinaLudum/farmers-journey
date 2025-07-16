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
                if (data && data.requirements) {
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
 * Faz com que os mini-cards das conquistas se expandam para mostrar detalhes
 * e gerencia os estados de 'ativo' e 'inativo' para uma melhor experiência visual.
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
 * Encontra todas as barras de progresso na página e usa o atributo 'aria-valuenow'
 * para definir o seu estilo 'width', fazendo-as preencher visualmente.
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
 * Recebe os dados da API e usa os templates HTML para construir e exibir a lista
 * de requisitos, custos e tempo para atingir a meta selecionada.
 */
function renderGoalResults(data: any) {
    const resultsContainer = document.getElementById('goal-results-container');
    const mainTemplate = document.getElementById('goal-list-template') as HTMLTemplateElement;
    const itemTemplate = document.getElementById('goal-list-item-template') as HTMLTemplateElement;
    if (!resultsContainer || !mainTemplate || !itemTemplate) return;

    resultsContainer.innerHTML = '';
    const mainClone = mainTemplate.content.cloneNode(true) as DocumentFragment;
    mainClone.querySelector('[data-template="goal-level"]')!.textContent = data.goal_level_display;
    mainClone.querySelector('[data-template="goal-land-type"]')!.textContent = data.goal_land_type;
    mainClone.querySelector('[data-template="bumpkin-level"]')!.textContent = data.max_bumpkin_level;
    mainClone.querySelector('[data-template="total-time"]')!.textContent = data.total_time_str;
    
    const totalCostFormatted = parseFloat(data.total_sfl_cost).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    mainClone.querySelector('[data-template="total-cost"]')!.textContent = totalCostFormatted;

    const column1 = mainClone.querySelector('[data-column="1"]')!;
    const column2 = mainClone.querySelector('[data-column="2"]')!;

    data.requirements.forEach((item: any, index: number) => {
        const itemClone = itemTemplate.content.cloneNode(true) as DocumentFragment;
        itemClone.querySelector<HTMLImageElement>('[data-template="icon"]')!.src = item.icon;
        itemClone.querySelector('[data-template="name"]')!.textContent = item.name;

        const shortfallEl = itemClone.querySelector<HTMLSpanElement>('[data-template="shortfall"]')!;
        const shortfallValue = parseFloat(item.shortfall);
        if (shortfallValue > 0) {
            shortfallEl.textContent = `Faltam ${shortfallValue.toLocaleString('pt-BR', { useGrouping: true, minimumFractionDigits: 2 })}`;
            shortfallEl.className = 'badge text-bg-warning';
        } else {
            shortfallEl.textContent = 'Completo';
            shortfallEl.className = 'badge text-bg-success';
        }

        const neededEl = itemClone.querySelector<HTMLElement>('[data-template="value_of_needed"]')!;
        if (neededEl) {
            const neededValue = parseFloat(item.needed);
            neededEl.textContent = `de ${neededValue.toLocaleString('pt-BR', { useGrouping: true, minimumFractionDigits: 2 })}`;
        }

        if (index % 2 === 0) {
            column1.appendChild(itemClone);
        } else {
            column2.appendChild(itemClone);
        }
    });

    resultsContainer.appendChild(mainClone);
}


/**
 * Propósito: Configurar e gerir o contador regressivo para uma expansão em andamento.
 * Procura por um elemento com o ID 'countdown-timer' e, se o encontrar, inicia um
 * temporizador que atualiza o tempo restante a cada segundo até a expansão ficar pronta.
 */
function setupExpansionCountdown() {
    const countdownElement = document.getElementById('countdown-timer');
    if (!countdownElement) return;

    const readyAtTimestamp = parseInt(countdownElement.dataset.readyAt || '0', 10);
    if (!readyAtTimestamp) {
        countdownElement.textContent = "Erro na data.";
        return;
    }

    const interval = setInterval(() => {
        const now = new Date().getTime();
        const distance = readyAtTimestamp - now;

        if (distance < 0) {
            clearInterval(interval);
            countdownElement.textContent = "Expansão Concluída!";
            // (A lógica para mudar a cor para sucesso pode ser adicionada aqui se desejar)
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
        
        // ADICIONADO: O prefixo "Faltam" é adicionado aqui pelo script.
        countdownElement.textContent = `Faltam ${timeLeft.trim()}`;
    }, 1000);
}