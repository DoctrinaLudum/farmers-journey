// ARQUIVO ATUALIZADO: typescript/dashboard.ts

// Removido 'declare var Isotope' e 'declare var Sortable' pois não são mais usados.

document.addEventListener('DOMContentLoaded', () => {
    // A lógica do formulário de metas não muda.
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
                const responseText = await response.text();

                if (!response.ok) {
                    throw new Error(`Erro na API (${response.status}): ${responseText}`);
                }

                const data = JSON.parse(responseText);

                resultsContainer.innerHTML = '';
                if (data && data.requirements) {
                    renderGoalResults(data);
                } else {
                    resultsContainer.innerHTML = '<p class="text-muted text-center small mt-3">Não foi possível calcular o plano para esta meta.</p>';
                    console.warn("Resposta da API bem-sucedida, mas sem dados de requisitos:", data);
                }

            } catch (error) {
                console.error("Ocorreu um erro ao processar a resposta da API:", error);
                resultsContainer.innerHTML = '<p class="text-danger text-center small mt-3">Ocorreu um erro ao buscar os dados. Tente novamente.</p>';
            }
        });
    }

    // ---> LÓGICA DO INVENTÁRIO REMOVIDA <---
    // Não precisamos mais de JavaScript para controlar o layout do inventário.
    // O CSS agora trata de tudo.
});

// A função renderGoalResults permanece a mesma.
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