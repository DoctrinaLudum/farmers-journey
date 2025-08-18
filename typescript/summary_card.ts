// typescript/summary_card.ts

// 1. Informa ao TypeScript que a variável SFL_PRICES existirá no escopo global da janela.
// Isso evita erros de compilação.
declare global {
    interface Window {
        SFL_PRICES: {
            data?: {
                p2p?: { [key: string]: string };
            }
        };
    }
}

// Define uma interface para os dados do resumo, para um código mais seguro e legível.
interface SummaryData {
    resourceName: string;
    resourceIcon: string;
    totalNodes: number;
    totalYield: number;
    totalSflValue: number;
    totalFertilized: number;
    totalBonusRewards: { [key: string]: number };
    totalBeeSwarms: number;
}

// 2. Garante que o script só execute após o carregamento completo do DOM.
document.addEventListener('DOMContentLoaded', () => {
    // Verifica se a variável global de preços foi carregada corretamente.
    if (typeof window.SFL_PRICES === 'undefined') {
        console.error("SFL_PRICES não foi encontrado. Verifique se a tag <script> está no dashboard.html.");
        return;
    }

    setupSummaryCardFilterLogic();
    setupSummaryCardInteractivity();
});

/**
 * Configura a lógica de filtro que calcula e exibe o card de resumo.
 */
function setupSummaryCardFilterLogic(): void {
    const mapWrapper = document.querySelector<HTMLElement>('.farm-layout-map');
    if (!mapWrapper) return;

    const summaryCard = document.getElementById('floating-summary-card');

    // Usa delegação de evento para cliques nos gatilhos da legenda.
    mapWrapper.addEventListener('click', (event: MouseEvent) => {
        // CORREÇÃO: Ouve cliques apenas nos gatilhos de filtro de RECURSO, ignorando os de AOE.
        const trigger = (event.target as HTMLElement).closest<HTMLElement>('.resource-filter-trigger');
        if (!trigger) return;

        const filterId = trigger.dataset.filterId;
        if (!filterId) return;

        // A lógica em `dashboard.ts` irá adicionar/remover a classe 'active'.
        // Se o trigger NÃO TEM a classe 'active' após o clique, significa que ele foi ativado.
        // Usamos um pequeno timeout para garantir que o script de `dashboard.ts` execute primeiro.
        setTimeout(() => {
            if (trigger.classList.contains('active')) {
                calculateAndShowSummary(filterId, trigger);
            } else {
                if (summaryCard) summaryCard.style.display = 'none';
            }
        }, 0);
    });
}

/**
 * Calcula os dados de resumo para um filtro ativo e chama a função para exibir o card.
 * @param filterId O ID do filtro de recurso (ex: 'wood', 'stone').
 */
function calculateAndShowSummary(filterId: string, triggerElement: HTMLElement): void {
    const mapWrapper = document.querySelector<HTMLElement>('.farm-layout-map');
    const summaryCard = document.getElementById('floating-summary-card');
    if (!mapWrapper || !summaryCard) return;

    // CORREÇÃO: O seletor agora encontra tanto recursos diretos quanto estufas que contêm a planta.
    // O seletor `~=` é ideal para atributos que contêm uma lista de valores separados por espaços.
    const matchingElements = mapWrapper.querySelectorAll<HTMLElement>(
        `[data-resource-filter-id="${filterId}"], [data-greenhouse-plants~="${filterId}"]`
    );

    if (matchingElements.length === 0) {
        summaryCard.style.display = 'none';
        return;
    }

    // Usa um objeto para agrupar os dados de resumo
    const summary: SummaryData = {
        resourceName: '', resourceIcon: '', totalNodes: 0, totalYield: 0,
        totalSflValue: 0, totalFertilized: 0, totalBonusRewards: {}, totalBeeSwarms: 0
    };

    const prices = window.SFL_PRICES?.data?.p2p || {};

    matchingElements.forEach(element => {
        if (!element.dataset.resourceInfo) return;

        try {
            const resource = JSON.parse(element.dataset.resourceInfo);
            const analysisData = resource.analysis;
            if (!analysisData) return;

            // NOVO: Lógica específica para a Estufa
            if (resource.type === 'Greenhouse' && analysisData.pots) {
                // Itera sobre os vasos para somar apenas os da planta selecionada
                Object.values(analysisData.pots as any[]).forEach((pot: any) => {
                    const plantName = pot.plant_name;
                    if (!plantName) return;

                    // Gera um ID de filtro para a planta no vaso para comparar
                    const potPlantFilterId = plantName.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
                    
                    if (potPlantFilterId === filterId) {
                        summary.totalNodes++;

                        if (!summary.resourceName) {
                            summary.resourceName = plantName;
                            summary.resourceIcon = pot.icon_path || '';
                        }

                        const yieldAmount = pot.calculations?.yield?.final_deterministic || 0;
                        summary.totalYield += yieldAmount;

                        const priceStr = prices[plantName];
                        if (priceStr) {
                            summary.totalSflValue += yieldAmount * parseFloat(priceStr);
                        }
                    }
                });
            } 
            // Lógica existente para outros recursos
            else if (element.dataset.resourceFilterId === filterId) {
                summary.totalNodes++;

                if (!summary.resourceName) {
                    summary.resourceName = analysisData.crop_name || analysisData.fruit_name || analysisData.flower_name || analysisData.resource_name || 'Recurso';
                    summary.resourceIcon = analysisData.icon_path || '';
                }
    
                const yieldAmount = analysisData.calculations?.yield?.final_deterministic || 0;
                summary.totalYield += yieldAmount;
    
                const priceStr = prices[summary.resourceName];
                if (priceStr) {
                    summary.totalSflValue += yieldAmount * parseFloat(priceStr);
                }
    
                if (analysisData.bonus_reward) {
                    for (const [item, amount] of Object.entries(analysisData.bonus_reward as Record<string, number>)) {
                        summary.totalBonusRewards[item] = (summary.totalBonusRewards[item] || 0) + amount;
                    }
                }
    
                if (analysisData.has_yield_fertiliser) {
                    summary.totalFertilized++;
                }
    
                if (analysisData.beeSwarm) {
                    summary.totalBeeSwarms++;
                }
            }
        } catch (e) {
            console.error("Erro ao analisar os dados da célula para o resumo:", e);
        }
    });

    populateAndShowSummaryCard(summary, triggerElement);
}

/**
 * Popula o card de resumo com os dados calculados e o exibe.
 * @param summaryData Objeto contendo todos os dados de resumo.
 */
function populateAndShowSummaryCard(summaryData: SummaryData, triggerElement: HTMLElement): void {
    const card = document.getElementById('floating-summary-card');
    const cardTitle = document.getElementById('summary-card-title');
    const cardIcon = document.getElementById('summary-card-icon') as HTMLImageElement;
    const cardBody = document.getElementById('summary-card-body');
    const statTemplate = document.getElementById('resource-card-stat-template') as HTMLTemplateElement;

    if (!card || !cardTitle || !cardIcon || !cardBody || !statTemplate) return;

    cardTitle.textContent = `Resumo: ${summaryData.resourceName}`;
    cardIcon.src = summaryData.resourceIcon ? `/static/${summaryData.resourceIcon}` : '';
    cardBody.innerHTML = '';

    const statsList = document.createElement('ul');
    statsList.className = 'list-group list-group-flush';

    const addStat = (label: string, value: string | number) => {
        if (value === 0 && label !== 'Nós') return;
        const clone = statTemplate.content.cloneNode(true) as DocumentFragment;
        clone.querySelector('.stat-label')!.textContent = label;
        clone.querySelector('.stat-value')!.textContent = String(value);
        statsList.appendChild(clone);
    };

    addStat('Nós', summaryData.totalNodes);
    addStat('Rendimento Total', summaryData.totalYield.toFixed(2));

    // NOVO: Adiciona o rendimento médio por nó, se houver mais de um nó.
    if (summaryData.totalNodes > 1) {
        const averageYield = summaryData.totalYield / summaryData.totalNodes;
        addStat('Rendimento Médio/Nó', averageYield.toFixed(2));
    }

    // NOVO: Só mostra o valor total se for maior que zero e adiciona um ícone.
    if (summaryData.totalSflValue > 0) {
        const clone = statTemplate.content.cloneNode(true) as DocumentFragment;
        const labelEl = clone.querySelector('.stat-label')!;
        // Adiciona o ícone e o texto ao rótulo
        labelEl.innerHTML = `<img src="/static/images/resources/flower.webp" alt="FLOWER" class="icon icon-1x me-1" style="vertical-align: text-bottom;"> Valor Total (Flower)`;
        
        const valueEl = clone.querySelector('.stat-value')!;
        valueEl.textContent = `~${summaryData.totalSflValue.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        
        statsList.appendChild(clone);
    }
    
    if (summaryData.totalFertilized > 0) {
        addStat('Fertilizados', `${summaryData.totalFertilized} de ${summaryData.totalNodes}`);
    }

    // NOVO: Adiciona a contagem de nós polinizados por abelhas.
    if (summaryData.totalBeeSwarms > 0) {
        const clone = statTemplate.content.cloneNode(true) as DocumentFragment;
        const labelEl = clone.querySelector('.stat-label')!;
        // Adiciona o ícone e o texto ao rótulo
        labelEl.innerHTML = `<img src="/static/images/misc/bee.webp" alt="Abelha" class="icon icon-1x me-1" style="vertical-align: text-bottom;"> Polinizados`;
        
        const valueEl = clone.querySelector('.stat-value')!;
        valueEl.textContent = `${summaryData.totalBeeSwarms} de ${summaryData.totalNodes}`;
        statsList.appendChild(clone);
    }

    if (Object.keys(summaryData.totalBonusRewards).length > 0) {
        const rewardsStr = Object.entries(summaryData.totalBonusRewards)
            .map(([item, amount]) => `+${amount} ${item}`)
            .join(', ');
        addStat('Recompensas Extra', rewardsStr);
    }

    cardBody.appendChild(statsList);

    // NOVO: Adiciona o disclaimer sobre os preços no final do card.
    const disclaimer = document.createElement('p');
    // Adiciona classes do Bootstrap para um fundo azul claro, padding e bordas arredondadas.
    disclaimer.className = 'small mt-3 mb-0 p-2 bg-info-subtle text-info-emphasis border border-info-subtle rounded';
    disclaimer.style.fontSize = '0.7rem';
    disclaimer.textContent = '*Preços estimados via sfl.world e podem variar.';
    cardBody.appendChild(disclaimer);

    // --- LÓGICA DE POSICIONAMENTO DINÂMICO ---
    // 1. Torna o card "invisível" mas mensurável para obter suas dimensões corretas.
    card.style.visibility = 'hidden';
    card.style.display = 'block';
    card.style.right = 'auto'; // Reseta o posicionamento à direita para usar 'left'
    card.style.left = '-9999px'; // Move para fora da tela

    // 2. Agora que está populado e visível (mas fora da tela), mede as dimensões.
    const cardWidth = card.offsetWidth;
    const cardHeight = card.offsetHeight;
    const margin = 15;

    const triggerRect = triggerElement.getBoundingClientRect();

    // 3. Calcula a posição. Tenta posicionar à esquerda do item da legenda.
    let left = triggerRect.left - cardWidth - margin;
    // Se não couber à esquerda, posiciona à direita.
    if (left < margin) {
        left = triggerRect.right + margin;
    }

    // Tenta alinhar o topo do card com o topo do gatilho.
    let top = triggerRect.top;
    // Se passar do final da tela, alinha com a parte de baixo da tela.
    if (top + cardHeight > window.innerHeight) {
        top = window.innerHeight - cardHeight - margin;
    }
    // Garante que não saia pelo topo da tela.
    top = Math.max(margin, top);

    card.style.left = `${left}px`;
    card.style.top = `${top}px`;
    card.style.visibility = 'visible';
}

/**
 * Configura a interatividade do card de resumo (arrastar e fechar).
 */
function setupSummaryCardInteractivity(): void {
    const card = document.getElementById('floating-summary-card');
    const cardHeader = document.getElementById('floating-summary-card-header');
    const closeBtn = document.getElementById('summary-card-close-btn');
    const mapWrapper = document.querySelector<HTMLElement>('.farm-layout-map');

    if (!card || !cardHeader || !closeBtn || !mapWrapper) return;

    // Função auxiliar para fechar o card e limpar o filtro, evitando duplicação de código.
    const closeSummaryCard = () => {
        if (card.style.display !== 'none') {
            card.style.display = 'none';
            // Dispara um evento customizado para que o `dashboard.ts` possa limpar o filtro visual.
            mapWrapper.dispatchEvent(new CustomEvent('clear-filter'));
        }
    };

    closeBtn.addEventListener('click', closeSummaryCard);

    // NOVO: Adiciona um ouvinte de evento global para a tecla 'Escape'.
    document.addEventListener('keydown', (event: KeyboardEvent) => {
        // Se a tecla 'Escape' for pressionada e o card estiver visível, fecha-o.
        if (event.key === 'Escape' && card.style.display !== 'none') {
            closeSummaryCard();
        }
    });

    cardHeader.addEventListener('mousedown', (e: MouseEvent) => {
        e.preventDefault();
        document.body.classList.add('is-dragging-card');
        const rect = card.getBoundingClientRect();
        const offsetX = e.clientX - rect.left;
        const offsetY = e.clientY - rect.top;

        const onMouseMove = (moveEvent: MouseEvent) => {
            card.style.left = `${moveEvent.clientX - offsetX}px`;
            card.style.top = `${moveEvent.clientY - offsetY}px`;
        };

        const onMouseUp = () => {
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('mouseup', onMouseUp);
            document.body.classList.remove('is-dragging-card');
        };

        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
    });
}

// Garante que o ficheiro seja tratado como um módulo pelo TypeScript.
export {};