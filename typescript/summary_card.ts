// typescript/summary_card.ts
import { positionCardAroundGroup } from "./card_positioner.js";

/**
 * Mapeia nomes de itens para seus caminhos de imagem.
 * Esta é uma versão simplificada do lado do cliente da função do backend.
 * @param itemName O nome do item.
 * @returns O caminho para o ícone do item.
 */
function getItemImagePath(itemName: string): string {
    if (!itemName) return '/static/images/resources/question-mark.png';

    const formattedName = itemName.toLowerCase().replace(/ /g, '_').replace(/'/g, '');




    return `/static/images/crops/${formattedName}.webp`;
}
import { CurrencyConverter } from "./currency_converter.js";
// Define uma interface para os dados de preços, para um código mais seguro.
interface SflPrices {
    data?: {
        p2p?: { [key: string]: string };
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
    sourceType?: 'Crop Machine' | 'Greenhouse' | 'Plot';
}

// NOVO: Interface para um buff aplicado, para maior clareza.
interface AppliedBuff {
    source_item: string;
    value: number;
    count?: number;
    type: 'YIELD' | 'TIME' | string; // Outros tipos podem existir
}


// NOVO: Define uma interface para os dados de um pacote na Crop Machine.
interface CropMachinePack {
    crop: string;
    seeds: number;
    yield_info: {
        final_deterministic: number;
        applied_buffs: AppliedBuff[];
        average_yield_per_seed: number; 
    };
    time_to_ready_formatted: string;
    pack_index: number;
}

// NOVO: Define uma interface para os dados de resumo da Crop Machine.
interface CropMachineSummaryData {
    isCropMachine: true;
    resourceName: string;
    resourceIcon: string;
    packs: CropMachinePack[];
}
// NOVO: Define uma interface para os dados de impostos, tornando o código mais claro.
interface TaxInfo {
    originalRate: number;
    vipDiscount: number;
    finalRate: number;
    islandName: string;
}


// Armazena os preços em uma variável no escopo do módulo para evitar re-parsing.
let sflPrices: SflPrices = {};
// NOVO: Armazena o tipo de ilha e o status VIP do usuário para cálculos de impostos.
let islandType: string = 'basic';
let isVip: boolean = false;

document.addEventListener('DOMContentLoaded', () => {
    // Carrega os preços do data-attribute do body.
    const pricesData = document.body.dataset.sflPrices;
    if (pricesData) {
        try {
            sflPrices = JSON.parse(pricesData);
        } catch (e) {
            console.error("Falha ao analisar os dados de preços (data-sfl-prices):", e);
        }
    } else {
        console.error("data-sfl-prices não foi encontrado no body. Verifique se os dados estão sendo passados pelo backend.");
    }

    // NOVO: Carrega o tipo de ilha e o status VIP do data-attribute do painel do mapa.
    // Estes dados são essenciais para calcular a taxa de venda de recursos.
    // Esta é uma abordagem mais direcionada do que usar o body.
    const mapPanel = document.querySelector<HTMLElement>('.farm-layout-map');
    if (mapPanel) {
        islandType = mapPanel.dataset.islandType || 'basic';
        isVip = mapPanel.dataset.isVip === 'true';
    } else {
        console.error("Painel do mapa (.farm-layout-map) não encontrado. A lógica de impostos pode não funcionar.");
    }

    setupSummaryCardFilterLogic();
    setupSummaryCardInteractivity();
});

/**
 * NOVO: Calcula a taxa de imposto sobre recursos com base no tipo de ilha e status VIP.
 * @param island O tipo de ilha do jogador (ex: 'basic', 'spring', 'desert').
 * @param isVip Se o jogador tem acesso VIP.
 * @returns A taxa de imposto como um decimal (ex: 0.5 para 50%).
 */
function getResourceTax(island: string, isVip: boolean): TaxInfo {
    let originalRate: number;
    let islandName: string;

    switch (island) {
        case 'spring':
            originalRate = 0.50; // Petal Paradise: 50%
            islandName = 'Petal Paradise';
            break;
        case 'desert':
            originalRate = 0.20; // Desert Island: 20%
            islandName = 'Desert Island';
            break;
        case 'volcano':
            originalRate = 0.15; // Volcano Island: 15%
            islandName = 'Volcano Island';
            break;
        case 'basic': // Tutorial Island
        default:
            // Retorna 100% de imposto, efetivamente não pode vender.
            return { originalRate: 1, vipDiscount: 0, finalRate: 1, islandName: 'Tutorial Island' };
    }

    const vipDiscount = isVip ? originalRate / 2 : 0;
    const finalRate = originalRate - vipDiscount;

    if (isVip) {
        return { originalRate, vipDiscount, finalRate, islandName };
    }

    return { originalRate, vipDiscount: 0, finalRate, islandName };
}

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

    // REATORADO: Seletor unificado para encontrar todos os tipos de recursos, incluindo os dentro de edifícios.
    const matchingElements = mapWrapper.querySelectorAll<HTMLElement>( 
        `[data-resource-filter-id="${filterId}"], [data-greenhouse-plants~="${filterId}"], [data-crop-machine-plants~="${filterId}"]`
    );

    if (matchingElements.length === 0) {
        summaryCard.style.display = 'none';
        return;
    }

    // NOVO: Lógica especial para a Crop Machine.
    // Se o recurso clicado for parte da Crop Machine, mostra um card interativo com os detalhes de cada pacote.
    const firstElement = matchingElements[0];
    const resource = JSON.parse(firstElement.dataset.resourceInfo || '{}');

    if (resource.type === 'Crop Machine') {
        const analysisData = resource.analysis;
        // O filterId é o nome da cultura em kebab-case, ex: "red-pepper".
        // Precisamos do nome normal para o título e o ícone.
        const cropNameFromFilter = filterId.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());

        // Filtra a fila para obter apenas os pacotes da cultura selecionada.
        const packsForCrop = (analysisData?.queue || []).filter((pack: any) => 
            (pack.crop || '').toLowerCase().replace(/ /g, '-') === filterId
        );

        const cropMachineSummary: CropMachineSummaryData = {
            isCropMachine: true,
            resourceName: cropNameFromFilter,
            resourceIcon: getItemImagePath(cropNameFromFilter),
            packs: packsForCrop
        };

        populateAndShowSummaryCard(cropMachineSummary, triggerElement, getResourceTax(islandType, isVip), matchingElements);
        return;
    }
    // Usa um objeto para agrupar os dados de resumo
    const summary: SummaryData = {
        resourceName: '', resourceIcon: '', totalNodes: 0, totalYield: 0,
        totalSflValue: 0, totalFertilized: 0, totalBonusRewards: {}, totalBeeSwarms: 0
    };

    // Usa a variável de preços carregada no início.
    const prices = sflPrices?.data?.p2p || {};

    matchingElements.forEach(element => {
        if (!element.dataset.resourceInfo) return;

        try {
            const resource = JSON.parse(element.dataset.resourceInfo);
            const analysisData = resource.analysis;
            if (!analysisData) return;

            // NOVO: Lógica específica para a Estufa
            if (resource.type === 'Greenhouse' && analysisData.pots) {
                summary.sourceType = 'Greenhouse';
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
                summary.sourceType = 'Plot';
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

    // NOVO: Calcula a taxa de imposto com base no tipo de ilha e status VIP do usuário.
    const taxInfo = getResourceTax(islandType, isVip);
    
    // Aplica a taxa ao valor total. O valor final é o que o jogador recebe após a venda.
    const finalSflValue = summary.totalSflValue * (1 - taxInfo.finalRate);
    summary.totalSflValue = finalSflValue;

    populateAndShowSummaryCard(summary, triggerElement, taxInfo, matchingElements);
}

/**
 * Popula o card de resumo com os dados calculados e o exibe.
 * @param summaryData Objeto contendo todos os dados de resumo.
 */
function populateAndShowSummaryCard(summaryData: SummaryData | CropMachineSummaryData, triggerElement: HTMLElement, taxInfo: TaxInfo, matchingElements: NodeListOf<HTMLElement>): void {
    const card = document.getElementById('floating-summary-card');
    const cardTitle = document.getElementById('summary-card-title');
    const cardIcon = document.getElementById('summary-card-icon') as HTMLImageElement;
    const cardBody = document.getElementById('summary-card-body');
    const statTemplate = document.getElementById('resource-card-stat-template') as HTMLTemplateElement;

    if (!card || !cardTitle || !cardIcon || !cardBody || !statTemplate) return;

    // NOVO: Verifica se é um resumo da Crop Machine para renderizar o card correto.
    const isCropMachine = 'isCropMachine' in summaryData && summaryData.isCropMachine;

    cardTitle.textContent = isCropMachine
        ? `Resumo: ${summaryData.resourceName} (${summaryData.packs.length} pacotes)`
        : `Resumo: ${summaryData.resourceName}`;

    cardIcon.src = summaryData.resourceIcon.startsWith('/static/') ? summaryData.resourceIcon : `/static/${summaryData.resourceIcon}`;
    cardBody.innerHTML = '';

    if (isCropMachine) {
        const packDetailsContainer = document.createElement('div');
        packDetailsContainer.id = 'pack-details-container';

        const renderPackDetails = (pack: CropMachinePack) => {
            console.log("Dados do Pacote para Renderização:", pack);
            packDetailsContainer.innerHTML = ''; // Limpa os detalhes anteriores
            const list = document.createElement('ul');
            list.className = 'list-group list-group-flush';

            const addStat = (label: string, value: string | HTMLElement, iconPath?: string) => {
                const clone = statTemplate.content.cloneNode(true) as DocumentFragment;
                const labelEl = clone.querySelector('.stat-label')!;
                if (iconPath) {
                    labelEl.innerHTML = `<img src="${iconPath}" class="icon icon-1x me-2" alt="${label}" style="vertical-align: text-bottom;"> ${label}`;
                } else {
                    labelEl.textContent = label;
                }
                const valueEl = clone.querySelector('.stat-value')!;
                if (typeof value === 'string') {
                    valueEl.textContent = value;
                } else {
                    valueEl.innerHTML = ''; // Limpa o texto para adicionar o elemento HTML
                    valueEl.appendChild(value);
                }
                list.appendChild(clone);
            };

            const yieldAmount = pack.yield_info?.final_deterministic || 0;
            // Usa o valor de média já calculado pelo backend.
            const averageYield = pack.yield_info?.average_yield_per_seed || 0;

            const prices = sflPrices?.data?.p2p || {};
            const price = parseFloat(prices[pack.crop] || '0');
            const rawValue = yieldAmount * price;
            const finalValue = rawValue * (1 - taxInfo.finalRate);

            addStat('Rendimento Total', yieldAmount.toFixed(2));
            addStat('Rendimento Médio/Semente', averageYield.toFixed(2));

            if (window.currencyConverter && finalValue > 0) {
                const valueHtml = window.currencyConverter.generateCurrencyHTML(finalValue, '~');
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = valueHtml;
                addStat('Valor (Após Taxa)', tempDiv.firstElementChild as HTMLElement);
            } else if (finalValue > 0) {
                addStat('Valor (Após Taxa)', `~${finalValue.toFixed(2)} Flower`);
            }

            packDetailsContainer.appendChild(list);

            // Adiciona o rodapé com informações de taxas e disclaimer
            const cardFooter = document.createElement('div');
            cardFooter.className = 'mt-3';

            if (rawValue > 0 && taxInfo.finalRate > 0) {
                const taxDisclaimer = document.createElement('div');
                taxDisclaimer.className = 'small tax-disclaimer-badges mb-2 text-end';
                const formatPercentage = (rate: number): string => {
                    const percentage = rate * 100;
                    return Number.isInteger(percentage) ? percentage.toFixed(0) : percentage.toFixed(1);
                };
                let taxHtml = '';
                if (taxInfo.finalRate === 1) {
                    taxHtml = `<span class="badge bg-danger-subtle text-danger-emphasis">Venda desativada nesta ilha</span>`;
                } else {
                    const originalRatePercent = formatPercentage(taxInfo.originalRate);
                    const finalRatePercent = formatPercentage(taxInfo.finalRate);
                    taxHtml = `<span class="badge bg-secondary-subtle text-dark-emphasis" title="Taxa base da ilha">Taxa ${taxInfo.islandName}: ${originalRatePercent}%</span>`;
                    if (taxInfo.vipDiscount > 0) {
                        const vipDiscountPercent = formatPercentage(taxInfo.vipDiscount);
                        taxHtml += ` <span class="badge bg-info-subtle text-info-emphasis" title="Desconto VIP">(-${vipDiscountPercent}% VIP)</span>`;
                    }
                    taxHtml += ` <strong class="mx-1">=</strong> <span class="badge bg-primary-subtle text-primary-emphasis" title="Taxa final aplicada ao valor total">${finalRatePercent}% Aplicada</span>`;
                }
                taxDisclaimer.innerHTML = taxHtml;
                cardFooter.appendChild(taxDisclaimer);
            }

            const priceDisclaimer = document.createElement('p');
            priceDisclaimer.className = 'small mb-0 p-2 bg-secondary-subtle text-secondary-emphasis border border-secondary-subtle rounded';
            priceDisclaimer.textContent = '*Preços estimados via sfl.world e podem variar.';
            cardFooter.appendChild(priceDisclaimer);

            if (cardFooter.hasChildNodes()) {
                packDetailsContainer.appendChild(cardFooter);
            }
        };

        if (summaryData.packs.length > 1) {
            const paginationContainer = document.createElement('div');
            // Usa btn-group para um visual mais compacto
            paginationContainer.className = 'btn-group btn-group-sm d-flex flex-wrap justify-content-center mb-3';
            paginationContainer.setAttribute('role', 'group');

            summaryData.packs.forEach((pack: CropMachinePack, index: number) => {
                const tab = document.createElement('button');
                tab.className = 'btn btn-sm btn-outline-secondary';
                // Usa o pack_index original para o rótulo, que corresponde ao que o jogador vê na máquina.
                tab.textContent = `Pacote ${pack.pack_index + 1}`;
                
                if (index === 0) tab.classList.add('active');

                tab.addEventListener('click', () => {
                    paginationContainer.querySelectorAll('button').forEach(btn => btn.classList.remove('active'));
                    tab.classList.add('active');
                    renderPackDetails(pack);
                });

                paginationContainer.appendChild(tab);
            });
            cardBody.appendChild(paginationContainer);
        }

        cardBody.appendChild(packDetailsContainer);

        if (summaryData.packs.length > 0) {
            renderPackDetails(summaryData.packs[0]);
        } else {
            packDetailsContainer.innerHTML = '<p class="text-muted small text-center">Nenhum pacote desta cultura na fila.</p>';
        }
    } else {
        const statsList = document.createElement('ul');
        statsList.className = 'list-group list-group-flush';

        const addStat = (label: string, value: string | number) => {
            let displayLabel = label;
            if ((summaryData as SummaryData).sourceType === 'Crop Machine' && label === 'Nós') {
                displayLabel = 'Pacotes';
            }
            if (value === 0 && label !== 'Nós' && label !== 'Pacotes') return;
            const clone = statTemplate.content.cloneNode(true) as DocumentFragment;
            clone.querySelector('.stat-label')!.textContent = displayLabel;
            clone.querySelector('.stat-value')!.textContent = String(value);
            statsList.appendChild(clone);
        };

        addStat('Nós', (summaryData as SummaryData).totalNodes);
        addStat('Rendimento Total', (summaryData as SummaryData).totalYield.toFixed(2));

        if ((summaryData as SummaryData).totalNodes > 1) {
            const averageYield = (summaryData as SummaryData).totalYield / (summaryData as SummaryData).totalNodes;
            addStat('Rendimento Médio/Nó', averageYield.toFixed(2));
        }

        if ((summaryData as SummaryData).totalSflValue > 0) {
            const totalValueStat = statTemplate.content.cloneNode(true) as DocumentFragment;
            const labelEl = totalValueStat.querySelector('.stat-label')!;
            const valueEl = totalValueStat.querySelector('.stat-value')!;
            labelEl.innerHTML = `Valor Total`;
            if (window.currencyConverter) {
                valueEl.innerHTML = window.currencyConverter.generateCurrencyHTML((summaryData as SummaryData).totalSflValue, '~');
            } else {
                valueEl.textContent = `~${(summaryData as SummaryData).totalSflValue.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} Flower`;
            }
            statsList.appendChild(totalValueStat);
        }
        
        if ((summaryData as SummaryData).totalFertilized > 0) {
            addStat('Fertilizados', `${(summaryData as SummaryData).totalFertilized} de ${(summaryData as SummaryData).totalNodes}`);
        }

        

        if (Object.keys((summaryData as SummaryData).totalBonusRewards).length > 0) {
            const rewardsStr = Object.entries((summaryData as SummaryData).totalBonusRewards)
                .map(([item, amount]) => `+${amount} ${item}`)
                .join(', ');
            addStat('Recompensas Extra', rewardsStr);
        }

        cardBody.appendChild(statsList);

        const cardFooter = document.createElement('div');
        cardFooter.className = 'mt-3';

        if ((summaryData as SummaryData).totalSflValue > 0 && taxInfo.finalRate > 0) {
            const taxDisclaimer = document.createElement('div');
            taxDisclaimer.className = 'small tax-disclaimer-badges mb-2 text-end';
            const formatPercentage = (rate: number): string => {
                const percentage = rate * 100;
                return Number.isInteger(percentage) ? percentage.toFixed(0) : percentage.toFixed(1);
            };
            let taxHtml = '';
            if (taxInfo.finalRate === 1) {
                taxHtml = `<span class="badge bg-danger-subtle text-danger-emphasis">Venda desativada nesta ilha</span>`;
            } else {
                const originalRatePercent = formatPercentage(taxInfo.originalRate);
                const finalRatePercent = formatPercentage(taxInfo.finalRate);
                taxHtml = `<span class="badge bg-secondary-subtle text-dark-emphasis" title="Taxa base da ilha">Taxa ${taxInfo.islandName}: ${originalRatePercent}%</span>`;
                if (taxInfo.vipDiscount > 0) {
                    const vipDiscountPercent = formatPercentage(taxInfo.vipDiscount);
                    taxHtml += ` <span class="badge bg-info-subtle text-info-emphasis" title="Desconto VIP">(-${vipDiscountPercent}% VIP)</span>`;
                }
                taxHtml += ` <strong class="mx-1">=</strong> <span class="badge bg-primary-subtle text-primary-emphasis" title="Taxa final aplicada ao valor total">${finalRatePercent}% Aplicada</span>`;
            }
            taxDisclaimer.innerHTML = taxHtml;
            cardFooter.appendChild(taxDisclaimer);
        }

        const priceDisclaimer = document.createElement('p');
        priceDisclaimer.className = 'small mb-0 p-2 bg-secondary-subtle text-secondary-emphasis border border-secondary-subtle rounded';
        priceDisclaimer.textContent = '*Preços estimados via sfl.world e podem variar.';
        cardFooter.appendChild(priceDisclaimer);

        if (cardFooter.hasChildNodes()) {
            cardBody.appendChild(cardFooter);
        }
    }

    // --- LÓGICA DE POSICIONAMENTO CENTRALIZADA ---
    // A rolagem do mapa é assíncrona. Um pequeno timeout garante que o posicionamento
    // seja calculado após o início da rolagem. A nova função usa a lista completa
    // de elementos destacados para evitar sobreposição.
    setTimeout(() => positionCardAroundGroup(card!, matchingElements), 50);
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