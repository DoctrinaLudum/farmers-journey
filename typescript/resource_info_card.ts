// typescript/resource_info_card.ts
import { positionCard } from './card_positioner.js';

// --- INTERFACES DE DADOS ---

/**
 * Representa um bônus ou penalidade que afeta um recurso.
 */
interface Buff {
    source_type: 'skill' | 'skill_legacy' | 'collectible' | 'wearable' | 'bud' | 'game_mechanic' | 'fertiliser' | 'tool' | 'event';
    source_item: string;
    count: number;
    value: number | string;
    operation: 'percentage' | 'multiply' | 'add';
    type?: 'OIL_COST' | 'CROP_MACHINE_GROWTH_TIME';
    total_bonus_yield?: number;
    modifiers?: Modifier[];
}

/**
 * Representa um modificador que altera o efeito de um Buff.
 * Ex: Um Bud que aumenta o bônus de um colecionável.
 */
interface Modifier {
    source_type: string;
    source_item: string;
    value: number | string;
    operation: 'multiply' | 'add';
}

/**
 * Representa um vaso de planta na Estufa (Greenhouse).
 */
interface Pot {
    id: number;
    plant_name: string;
    state_name: string;
    ready_at_timestamp_ms: number;
    calculations: {
        yield: {
            final_deterministic: number;
            applied_buffs: Buff[];
        };
        growth: {
            applied_buffs: Buff[];
        };
    };
}

/**
 * Representa um pacote de sementes na Crop Machine.
 */
interface Pack {
    is_ready: boolean;
    seeds: number;
    yield_info?: {
        final_deterministic: number;
        average_yield_per_seed?: number;
        applied_buffs: Buff[];
    };
    oil_cost?: number;
    readyAt: number;
    icon_path: string;
}

/**
 * Estrutura principal dos dados de análise de um recurso.
 */
interface AnalysisData {
    crop_name?: string;
    fruit_name?: string;
    tree_name?: string;
    resource_name?: string;
    name?: string;
    state_name: string;
    ready_at_timestamp_ms?: number;
    crimstone_reset_at_ms?: number;
    base_amount?: number;
    mines_left?: number;
    harvests_left?: number;
    beeSwarm?: boolean;
    bonus_reward?: { [key: string]: number };
    calculations?: {
        yield: {
            final_deterministic: number;
            applied_buffs: Buff[];
        };
        recovery?: {
            applied_buffs: Buff[];
        };
        growth?: {
            applied_buffs: Buff[];
        };
    };
    applied_boosts?: Buff[];
    summary?: {
        next_wild_spawn_at?: number;
        next_magic_spawn_at?: number;
    };
    pots?: { [key: string]: Pot };
    global_oil_buffs?: any; // Manter como 'any' por enquanto devido à estrutura complexa
    global_time_buffs?: any; // Manter como 'any' por enquanto
    grouped_queue?: { [key: string]: Pack[] };
    max_queue_size?: number;
    used_queue_size?: number;
}

/**
 * Estrutura completa dos dados passados para o card.
 */
interface ResourceData {
    type: 'Greenhouse' | 'Crop Machine' | string;
    analysis: AnalysisData;
    base_building_icon?: string;
    icon?: string;
}


/**
 * Configura o card flutuante que exibe informações detalhadas sobre um recurso
 * quando ele é clicado no mapa da fazenda.
 */
export class ResourceInfoCard {
    private mapWrapper: HTMLElement | null;
    private card: HTMLElement | null;
    private cardHeader: HTMLElement | null;
    private cardTitle: HTMLElement | null;
    private cardIcon: HTMLImageElement | null;
    private cardBody: HTMLElement | null;
    private closeBtn: HTMLElement | null;

    constructor() {
        this.mapWrapper = document.querySelector<HTMLElement>('.farm-layout-map');
        this.card = document.getElementById('floating-resource-card');
        this.cardHeader = document.getElementById('floating-resource-card-header');
        this.cardTitle = document.getElementById('resource-card-title');
        this.cardIcon = document.getElementById('resource-card-icon') as HTMLImageElement;
        this.cardBody = document.getElementById('resource-card-body');
        this.closeBtn = document.getElementById('resource-card-close-btn');
    }

    public init() {
        if (!this.mapWrapper || !this.card || !this.cardHeader || !this.cardTitle || !this.cardIcon || !this.cardBody || !this.closeBtn) {
            console.warn("ResourceInfoCard: Um ou mais elementos necessários não foram encontrados no DOM. O card não será inicializado.");
            return;
        }

        this.setupEventListeners();
    }

    private setupEventListeners() {
        // --- Lógica para mostrar e popular o card ---
        this.mapWrapper!.addEventListener('click', (e: Event) => {
            const target = e.target as HTMLElement;
            const trigger = target.closest<HTMLElement>('.resource-info-trigger');

            if (!trigger || !trigger.dataset.resourceInfo) {
                return;
            }

            try {
                this.populateCard(JSON.parse(trigger.dataset.resourceInfo));
                // Usa a função utilitária para posicionar o card
                positionCard(this.card!, trigger);

            } catch (err) {
                console.error("Falha ao analisar os dados do recurso:", err);
            }
        });

        // --- Lógica para fechar o card ---
        this.closeBtn!.addEventListener('click', () => {
            this.card!.style.display = 'none';
        });

        // --- Lógica para arrastar o card ---
        this.cardHeader!.addEventListener('mousedown', (e: MouseEvent) => {
            e.preventDefault();
            document.body.classList.add('is-dragging-card');

            const rect = this.card!.getBoundingClientRect();
            const offsetX = e.clientX - rect.left;
            const offsetY = e.clientY - rect.top;

            const onMouseMove = (moveEvent: MouseEvent) => {
                let newLeft = moveEvent.clientX - offsetX;
                let newTop = moveEvent.clientY - offsetY;
            
                newLeft = Math.max(0, Math.min(newLeft, window.innerWidth - this.card!.offsetWidth));
                newTop = Math.max(0, Math.min(newTop, window.innerHeight - this.card!.offsetHeight));
            
                this.card!.style.left = `${newLeft}px`;
                this.card!.style.top = `${newTop}px`;
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

    /**
     * Função auxiliar para calcular e formatar o tempo restante.
     * @param timestampMs O timestamp final em milissegundos.
     * @returns Uma string formatada (ex: "1h 15m", "Pronta").
     */
    private timeRemaining(timestampMs: number): string {
        if (!timestampMs) return "N/A";
        const nowMs = Date.now();
        const remainingSeconds = (timestampMs - nowMs) / 1000;

        if (remainingSeconds <= 0) return "Pronta";

        const days = Math.floor(remainingSeconds / 86400);
        const hours = Math.floor((remainingSeconds % 86400) / 3600);
        const minutes = Math.floor((remainingSeconds % 3600) / 60);

        let parts = [];
        if (days > 0) parts.push(`${days}d`);
        if (hours > 0) parts.push(`${hours}h`);
        if (minutes > 0) parts.push(`${minutes}m`);
        return parts.join(' ') || 'Pronta';
    }

    private formatFullDateTime(timestamp: number): string {
        if (!timestamp) return '';
        const date = new Date(timestamp);
        // Pad with '0' to ensure two digits
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0'); // Month is 0-indexed
        const year = date.getFullYear();
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');
        return `${day}/${month}/${year}, ${hours}:${minutes}:${seconds}`;
    }

    // --- Função principal para popular o card com dados ---
    private populateCard(data: ResourceData) {
        // Limpeza de elementos dinâmicos de execuções anteriores
        this.cardHeader!.querySelector('.global-buffs-btn')?.remove();
        document.getElementById('global-buffs-panel')?.remove();

        const analysisData = data.analysis;
        const resourceName = analysisData.crop_name || analysisData.fruit_name || analysisData.tree_name || analysisData.resource_name || analysisData.name || 'Recurso';
        this.cardTitle!.textContent = resourceName;

        const iconPath = data.base_building_icon || data.icon;

        if (iconPath) {
            this.cardIcon!.src = `/static/${iconPath}`;
        } else {
            this.cardIcon!.src = ''; // Fallback para evitar erros
        }
        
        this.cardBody!.innerHTML = ''; 

        const statTemplate = document.getElementById('resource-card-stat-template') as HTMLTemplateElement;
        const buffTemplate = document.getElementById('resource-card-buff-template') as HTMLTemplateElement;
        const statsList = document.createElement('ul');
        statsList.className = 'list-group list-group-flush';

        const renderBuffsToList = (buffs: Buff[], targetList: HTMLElement, isTimeBonus: boolean = false) => {
            if (!buffs || buffs.length === 0) return;

            const sourceTypeToLabel: { [key: string]: string } = {
                skill: '(Skill)',
                skill_legacy: '(Skill Legacy)',
                collectible: '(Collectible)',
                wearable: '(Wearable)',
                bud: '(Bud)',
                game_mechanic: '(Nativo)',
                fertiliser: '(Fertiliser)',
                tool: '(Ferramenta)',
                event: '(Evento)'
            };

            buffs.forEach((buff: Buff) => {
                const clone = buffTemplate.content.cloneNode(true) as DocumentFragment;
                
                const prefix = sourceTypeToLabel[buff.source_type] || '';
                let sourceItem = buff.source_item;
                if (buff.source_type === 'bud' && sourceItem.startsWith('Bud ')) {
                    sourceItem = sourceItem.substring(4);
                }
                const typeClass = buff.source_type ? `is-type-${buff.source_type}` : '';
                const prefixTag = prefix ? `<span class="buff-source-tag ${typeClass}">${prefix}</span>` : '';
                const buffCount = buff.count > 1 ? ` (x${buff.count})` : '';

                clone.querySelector('.buff-source')!.innerHTML = `${prefixTag} ${sourceItem}${buffCount}`.trim();
                let valueText = '';
                const buffValue = buff.value;
                const numericBuffValue = Number(buffValue);

                if (!isNaN(numericBuffValue)) {
                    let formattedValue: string;
                    let operator = '';

                    // Lógica de formatação refatorada para evitar erros de tipo
                    if (buff.type === 'CROP_MACHINE_GROWTH_TIME') {
                        if (buff.operation === 'multiply') {
                            formattedValue = ((1 - numericBuffValue) * 100).toFixed(0);
                            valueText = `-${formattedValue}%`;
                        } else if (buff.operation === 'percentage') {
                            formattedValue = (numericBuffValue * 100).toFixed(0);
                            operator = numericBuffValue > 0 ? '+' : '';
                            valueText = `${operator}${formattedValue}%`;
                        } else if (buff.operation === 'add') { // 'add'
                            formattedValue = numericBuffValue.toFixed(2);
                            operator = numericBuffValue >= 0 ? '+' : '';
                            valueText = `${operator}${formattedValue}`;
                        }
                    } else if (buff.type === 'OIL_COST') {
                        formattedValue = (numericBuffValue * 100).toFixed(0);
                        operator = numericBuffValue >= 0 ? '+' : '';
                        valueText = `${operator}${formattedValue}%`;
                    } else if (buff.operation === 'percentage') {
                        formattedValue = (numericBuffValue * 100).toFixed(0);
                        operator = numericBuffValue > 0 ? '+' : '';
                        valueText = `${operator}${formattedValue}%`;
                    } else if (buff.operation === 'multiply') {
                        if (isTimeBonus && numericBuffValue < 1) {
                            formattedValue = ((1 - numericBuffValue) * 100).toFixed(0);
                            valueText = `-${formattedValue}%`;
                        } else {
                            formattedValue = numericBuffValue.toFixed(2);
                            operator = 'x';
                            if (!isTimeBonus && numericBuffValue > 1 && !buff.source_item.includes('(Critical Hit)')) {
                                const bonus = (numericBuffValue - 1).toFixed(2);
                                valueText = `${operator}${formattedValue} (+${bonus})`;
                            } else {
                                valueText = `${operator}${formattedValue}`;
                            }
                        }
                    } else if (buff.operation === 'add') { // Default is 'add'
                        formattedValue = numericBuffValue.toFixed(2);
                        operator = numericBuffValue >= 0 ? '+' : '';
                        valueText = `${operator}${formattedValue}`;
                    }
                } else {
                    valueText = String(buffValue);
                }

                const valueEl = clone.querySelector('.buff-value')!;
                valueEl.textContent = valueText;

                if (buff.total_bonus_yield && buff.total_bonus_yield > 0) {
                    const totalBonusEl = document.createElement('span');
                    totalBonusEl.className = 'text-muted small ps-1';
                    totalBonusEl.textContent = `(Total: +${buff.total_bonus_yield.toFixed(2)})`;
                    valueEl.appendChild(totalBonusEl);
                }

                if (!isNaN(numericBuffValue)) {
                    if (isTimeBonus) {
                        const isGoodTimeBonus = numericBuffValue < 0 || (buff.operation === 'multiply' && numericBuffValue < 1);
                        valueEl.classList.add(isGoodTimeBonus ? 'text-success' : 'text-danger');
                    } else {
                        valueEl.classList.add(numericBuffValue > 0 ? 'text-success' : 'text-danger');
                    }
                }

                targetList.appendChild(clone);

                if (buff.modifiers && Array.isArray(buff.modifiers)) {
                    buff.modifiers.forEach((modBuff: Modifier) => {
                        const modifierEl = document.createElement('div');
                        modifierEl.className = 'modifier-buff d-flex align-items-center small text-muted ms-3';
                        
                        const modPrefix = sourceTypeToLabel[modBuff.source_type] || '';
                        const modTypeClass = modBuff.source_type ? `is-type-${modBuff.source_type}` : '';
                        const modPrefixTag = modPrefix ? `<span class="buff-source-tag ${modTypeClass}">${modPrefix}</span>` : '';
                        const iconHtml = '<i class="bi bi-stars me-1"></i>';

                        let modifierText = '';
                        const modValueStr = String(modBuff.value);

                        if (modBuff.operation === 'multiply') {
                            modifierText = `${modPrefixTag} ${modBuff.source_item}: ${modValueStr}`;
                        } else {
                            modifierText = `<span class="buff-source-tag is-type-special">Modificado por</span> ${modPrefixTag} ${modBuff.source_item}`;
                        }

                        modifierEl.innerHTML = `${iconHtml} ${modifierText}`.trim();
                        targetList.appendChild(modifierEl);
                    });
                }
            });
        };

        const addStat = (label: string, value: string | number | undefined | null, valueClass?: string) => {
            if (value === undefined || value === null) return;

            const clone = statTemplate.content.cloneNode(true) as DocumentFragment;
            clone.querySelector('.stat-label')!.textContent = label;
            const valueEl = clone.querySelector('.stat-value')!;
            valueEl.textContent = String(value);

            if (valueClass) {
                valueEl.classList.add(...valueClass.split(' '));
            }
            statsList.appendChild(clone);
        };

        const addBonusRewards = (rewards: { [key: string]: number }) => {
            if (!rewards || Object.keys(rewards).length === 0) return;

            const titleEl = document.createElement('h6');
            titleEl.className = 'mt-2 mb-1 small text-muted';
            titleEl.textContent = 'Recompensas Bônus';
            statsList.appendChild(titleEl);

            for (const [itemName, amount] of Object.entries(rewards)) {
                const clone = buffTemplate.content.cloneNode(true) as HTMLElement;
                clone.querySelector('.buff-source')!.textContent = itemName;
                const valueEl = clone.querySelector('.buff-value')!;
                valueEl.textContent = `+${amount}`;
                valueEl.classList.add('text-success');
                statsList.appendChild(clone);
            }
        };

        const addBuffs = (buffs: Buff[] | undefined, title: string, isTimeBonus: boolean = false) => {
            if (!buffs || buffs.length === 0) return; 
            
            const titleEl = document.createElement('h6');
            titleEl.className = 'mt-2 mb-1 small text-muted';
            titleEl.textContent = title;
            statsList.appendChild(titleEl);
            
            renderBuffsToList(buffs, statsList, isTimeBonus);
        };

        addStat('Estado', analysisData.state_name);
        const isReady = analysisData.state_name === 'Pronta' || analysisData.state_name === 'Pronto';
        if (analysisData.ready_at_timestamp_ms && !isReady) {
            const readyDate = new Date(analysisData.ready_at_timestamp_ms).toLocaleString('pt-BR');
            addStat('Pronto em', readyDate);
        }
        if (analysisData.crimstone_reset_at_ms) {
            const resetTimeRemaining = this.timeRemaining(analysisData.crimstone_reset_at_ms);
            if (resetTimeRemaining !== 'Pronta') {
                const nowMs = Date.now();
                const remainingSeconds = (analysisData.crimstone_reset_at_ms - nowMs) / 1000;
                
                let criticalityClass = '';
                if (remainingSeconds < 10 * 60) {
                    criticalityClass = 'text-danger fw-bold';
                } 
                else if (remainingSeconds < 60 * 60) {
                    criticalityClass = 'text-warning fw-bold';
                }
                else if (remainingSeconds < 12 * 60 * 60) {
                    criticalityClass = 'text-warning';
                }

                addStat('Reinício em', resetTimeRemaining, criticalityClass);
            }
        }
        const yieldAmount = analysisData.calculations?.yield?.final_deterministic;
        if (yieldAmount !== undefined && yieldAmount !== null) {
            addStat('Rendimento Previsto', yieldAmount.toFixed(2));
        } else if (analysisData.base_amount !== undefined) {
            addStat('Rendimento Previsto', analysisData.base_amount?.toFixed(2));
        }

        addStat('Minas Restantes', analysisData.mines_left);
        addStat('Colheitas Restantes', analysisData.harvests_left);

        if (analysisData.beeSwarm) {
            addStat('Beeswarm', 'Sim', 'text-success');
        }

        this.cardBody!.appendChild(statsList);

        if (analysisData.bonus_reward) {
            addBonusRewards(analysisData.bonus_reward);
        }

        if (analysisData.calculations?.yield?.applied_buffs) {
            const buffs = analysisData.calculations.yield.applied_buffs;
            addBuffs(buffs, 'Bônus de Rendimento');

            const shouldShowDisclaimer = buffs.some((b: Buff) => 
                b.operation === 'multiply' && 
                b.source_item.includes('(Critical Hit)') && 
                b.total_bonus_yield && b.total_bonus_yield > 0
            );

            if (shouldShowDisclaimer) {
                const disclaimer = this.createDisclaimer(
                    `<i class="bi bi-info-circle me-1"></i> <strong>Nota:</strong> O valor 'Total' de um 'Critical Hit' é o ganho real, calculado após a aplicação de outros bônus multiplicativos.`
                );
                statsList.appendChild(disclaimer);
            }
        }
        const recoveryBuffs = analysisData.calculations?.recovery?.applied_buffs || analysisData.calculations?.growth?.applied_buffs;
        if (recoveryBuffs) {
            addBuffs(recoveryBuffs, 'Bônus de Tempo', true);
        }

        if (analysisData.applied_boosts && analysisData.applied_boosts.length > 0) {
            addBuffs(analysisData.applied_boosts, 'Bônus de Rendimento');
        }

        if (analysisData.summary) {
            let spawnTimestamp: number | undefined;

            if (analysisData.name === 'Wild Mushroom') {
                spawnTimestamp = analysisData.summary.next_wild_spawn_at;
            } else if (analysisData.name === 'Magic Mushroom') {
                spawnTimestamp = analysisData.summary.next_magic_spawn_at;
            }

            if (spawnTimestamp) {
                addStat('Próximo Spawn', this.formatFullDateTime(spawnTimestamp));
            }
        }

        if (data.type === 'Greenhouse' && analysisData.pots) {
            const pots = Object.values(analysisData.pots).filter(p => p.plant_name);

            if (pots.length === 0) {
                this.cardTitle!.textContent = 'Greenhouse (Vazia)';
                const noItemsEl = document.createElement('p');
                noItemsEl.className = 'text-muted small mt-2 mb-0';
                noItemsEl.textContent = 'Nenhum vaso com plantas.';
                this.cardBody!.appendChild(noItemsEl);
            } else {
                this.cardTitle!.textContent = `Greenhouse`;

                const navContainer = document.createElement('div');
                navContainer.className = 'nav nav-pills nav-pills-sm mb-2 d-flex align-items-center';
                
                const navLabel = document.createElement('span');
                navLabel.className = 'text-muted small me-2';
                navLabel.textContent = 'Vaso:';
                navContainer.appendChild(navLabel);

                const detailsContainer = document.createElement('div');
                detailsContainer.className = 'pot-details-content';

                pots.forEach((pot: Pot, index: number) => {
                    const button = document.createElement('button');
                    button.className = 'nav-link';
                    button.textContent = `${pot.plant_name} #${pot.id}`;
                    button.dataset.potIndex = String(index);
                    if (index === 0) {
                        button.classList.add('active');
                    }
                    navContainer.appendChild(button);
                });

                this.cardBody!.appendChild(navContainer);
                this.cardBody!.appendChild(detailsContainer);

                navContainer.addEventListener('click', (e) => {
                    const target = e.target as HTMLElement;
                    if (target.tagName === 'BUTTON' && target.dataset.potIndex) {
                        navContainer.querySelector('.active')?.classList.remove('active');
                        target.classList.add('active');
                        
                        const potIndex = parseInt(target.dataset.potIndex, 10);
                        const selectedPot = pots[potIndex];
                        
                        this.renderPotDetails(selectedPot, detailsContainer, statTemplate, buffTemplate, renderBuffsToList);
                    }
                });

                if (pots.length > 0) {
                    this.renderPotDetails(pots[0], detailsContainer, statTemplate, buffTemplate, renderBuffsToList);
                }
            }
        }

        if (data.type === 'Crop Machine' && analysisData) {
            try {
                const oilBuffsExist = analysisData.global_oil_buffs && (analysisData.global_oil_buffs.increases.length > 0 || analysisData.global_oil_buffs.decreases.length > 0);
                const timeBuffsExist = analysisData.global_time_buffs && analysisData.global_time_buffs.buffs.length > 0;
                
                if (oilBuffsExist || timeBuffsExist) {
                    const globalBuffsBtn = document.createElement('button');
                    globalBuffsBtn.className = 'btn btn-outline-info btn-sm global-buffs-btn';
                    globalBuffsBtn.innerHTML = '<i class="bi bi-stars"></i> Bônus Globais';
                    this.cardHeader!.appendChild(globalBuffsBtn);

                    const globalBuffsPanel = document.createElement('div');
                    globalBuffsPanel.id = 'global-buffs-panel';
                    globalBuffsPanel.className = 'global-buffs-panel card';
                    
                    globalBuffsPanel.style.position = 'absolute';
                    globalBuffsPanel.style.top = '0';
                    globalBuffsPanel.style.left = 'calc(100% + 10px)';
                    globalBuffsPanel.style.width = '350px';
                    globalBuffsPanel.style.display = 'none';
                    globalBuffsPanel.style.zIndex = '10';

                    const panelBody = document.createElement('div');
                    panelBody.className = 'card-body';
                    const panelList = document.createElement('ul');
                    panelList.className = 'list-group list-group-flush';

                    if (analysisData.max_queue_size) {
                        const usedQueue = analysisData.used_queue_size ?? 0;
                        const maxQueue = analysisData.max_queue_size;
                        const queueStatEl = document.createElement('li');
                        queueStatEl.className = 'list-group-item d-flex justify-content-between align-items-center';
                        queueStatEl.innerHTML = `<span class="stat-label">Fila de Pacotes:</span> <span class="stat-value"><strong>${usedQueue} / ${maxQueue}</strong></span>`;
                        panelList.appendChild(queueStatEl);
                        
                        const hr = document.createElement('hr');
                        hr.className = 'my-1';
                        panelList.appendChild(hr);
                    }

                    const sourceTypeToLabel: { [key: string]: string } = {
                        skill: '(Skill)', collectible: '(Collectible)',
                    };

                    const renderGroupedBuffs = (title: string, buffsData: any, targetList: HTMLElement) => {
                        if (!buffsData) return;
                        const buffs = buffsData.increases ? [...buffsData.increases, ...buffsData.decreases] : buffsData.buffs;
                        if (!buffs || buffs.length === 0) return;

                        const titleEl = document.createElement('h6');
                        titleEl.className = 'mt-2 mb-1 small text-muted';
                        titleEl.textContent = title;
                        targetList.appendChild(titleEl);

                        const buffTemplate = (document.getElementById('resource-card-buff-template') as HTMLTemplateElement).content;
                        buffs.forEach((buff: any) => {
                            const clone = buffTemplate.cloneNode(true) as DocumentFragment;
                            const buffSourceEl = clone.querySelector('.buff-source')!;
                            const buffValueEl = clone.querySelector('.buff-value')!;
                            const prefix = sourceTypeToLabel[buff.source_type] || '';
                            const typeClass = buff.source_type ? `is-type-${buff.source_type}` : '';
                            const prefixTag = prefix ? `<span class="buff-source-tag ${typeClass}">${prefix}</span>` : '';
                            buffSourceEl.innerHTML = `${prefixTag} ${buff.source_item}`.trim();
                            buffValueEl.textContent = buff.effect_str.replace(/\\n/g, '');
                            if (buff.sentiment === 'positive') {
                                buffValueEl.classList.add('text-success');
                            } else if (buff.sentiment === 'negative') {
                                buffValueEl.classList.add('text-danger');
                            }
                            targetList.appendChild(clone);
                        });

                        if (buffsData.rate) {
                            const rate = Number(buffsData.rate);
                            const rateEl = document.createElement('li');
                            rateEl.className = 'list-group-item d-flex justify-content-between align-items-center';
                            rateEl.innerHTML = `<span class="stat-label">Consumo Final:</span> <span class="stat-value"><strong>${rate.toFixed(2)} Oil/hora</strong></span>`;
                            targetList.appendChild(rateEl);
                        }

                        if (buffsData.disclaimer) {
                            const disclaimerEl = document.createElement('p');
                            disclaimerEl.className = 'small mb-0 mt-2 p-2 bg-secondary-subtle text-secondary-emphasis border border-secondary-subtle rounded';
                            
                            if (buffsData.rate) {
                                disclaimerEl.innerHTML = `<i class="bi bi-info-circle me-1"></i> O consumo de óleo é constante. Adicionar óleo aumenta o tempo de operação da máquina.`;
                            } else {
                                disclaimerEl.innerHTML = `<i class="bi bi-info-circle me-1"></i> ${buffsData.disclaimer}`;
                            }
                            
                            targetList.appendChild(disclaimerEl);
                            const hr = document.createElement('hr');
                            hr.className = 'my-2';
                            targetList.appendChild(hr);
                        }
                    };

                    renderGroupedBuffs('Bônus de Custo de Óleo (Máquina)', analysisData.global_oil_buffs, panelList);
                    renderGroupedBuffs('Bônus de Tempo (Máquina)', analysisData.global_time_buffs, panelList);

                    if (panelList.lastElementChild?.tagName === 'HR') {
                        panelList.removeChild(panelList.lastElementChild);
                    }

                    panelBody.appendChild(panelList);
                    globalBuffsPanel.appendChild(panelBody);
                    this.card!.appendChild(globalBuffsPanel);

                    globalBuffsBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        const isVisible = globalBuffsPanel.style.display === 'block';
                        globalBuffsPanel.style.display = isVisible ? 'none' : 'block';
                    });
                }
            } catch (error) {
                console.error("ResourceInfoCard: Erro ao renderizar o painel de bônus globais da Crop Machine.", error);
            }

            try {
                const groupedQueue = analysisData.grouped_queue;
                if (!groupedQueue) {
                    this.cardTitle!.textContent = 'Crop Machine (Vazia)';
                    const noItemsEl = document.createElement('p');
                    noItemsEl.className = 'text-muted small mt-2 mb-0';
                    noItemsEl.textContent = 'Nenhum pacote na fila.';
                    this.cardBody!.appendChild(noItemsEl);
                    return;
                }

                const cropGroups = Object.keys(groupedQueue);

                if (cropGroups.length === 0) {
                    this.cardTitle!.textContent = 'Crop Machine (Vazia)';
                    const noItemsEl = document.createElement('p');
                    noItemsEl.className = 'text-muted small mt-2 mb-0';
                    noItemsEl.textContent = 'Nenhum pacote na fila.';
                    this.cardBody!.appendChild(noItemsEl);
                } else {
                    if (cropGroups.length > 3) {
                        this.cardTitle!.textContent = `Crop Machine (${cropGroups.slice(0, 3).join(', ')}, ...)`;
                    } else {
                        this.cardTitle!.textContent = `Crop Machine (${cropGroups.join(', ')})`;
                    }

                    if (cropGroups.length > 1) {
                        const filterBar = document.createElement('div');
                        filterBar.className = 'd-flex flex-wrap gap-1 mb-3 pb-2 border-bottom sticky-filter-bar';

                        cropGroups.forEach(cropName => {
                            const packs = groupedQueue[cropName];
                            const iconPath = packs[0]?.icon_path;

                            const badge = document.createElement('a');
                            badge.className = 'badge text-decoration-none bg-info-subtle text-info-emphasis d-flex align-items-center gap-1';
                            
                            let badgeHTML = '';
                            if (iconPath) {
                                badgeHTML += `<img src="/static/${iconPath}" class="item-icon-sm" alt="${cropName} icon" style="height: 1em; width: 1em;">`;
                            }
                            badgeHTML += `<span>${cropName}</span>`;

                            badge.innerHTML = badgeHTML;
                            badge.href = `#crop-group-${cropName.replace(/\s+/g, '-')}`;
                            filterBar.appendChild(badge);
                        });
                        
                        this.cardBody!.appendChild(filterBar);

                        filterBar.addEventListener('click', (e) => {
                            const anchor = (e.target as HTMLElement).closest('a');
                            if (anchor && anchor.hash) {
                                e.preventDefault();
                                const targetId = anchor.hash.substring(1);
                                const targetElement = document.getElementById(targetId);
                                if (targetElement) {
                                    const scrollContainer = this.cardBody!;
                                    const offset = filterBar.offsetHeight + 45; 
                                    
                                    scrollContainer.scrollTo({
                                        top: targetElement.offsetTop - offset,
                                        behavior: 'smooth'
                                    });
                                }
                            }
                        });
                    }

                    Object.entries(groupedQueue).forEach(([cropName, packs]: [string, Pack[]], groupIndex) => {
                        try {
                            if (groupIndex > 0) {
                                const hr = document.createElement('hr');
                                hr.className = 'my-3';
                                this.cardBody!.appendChild(hr);
                            }

                            const groupWrapper = document.createElement('div');
                            groupWrapper.className = 'crop-machine-group';
                            groupWrapper.id = `crop-group-${cropName.replace(/\s+/g, '-')}`;

                            const groupHeader = document.createElement('h6');
                            groupHeader.className = 'd-flex align-items-center small mt-2';
                            groupHeader.innerHTML = `<img src="/static/${packs[0].icon_path}" class="icon icon-2x me-2"> <span>${cropName}</span>`;
                            groupWrapper.appendChild(groupHeader);

                            const detailsContainer = document.createElement('div');
                            detailsContainer.className = 'pack-details-content';

                            if (packs.length > 1) {
                                const navContainer = document.createElement('div');
                                navContainer.className = 'nav nav-pills nav-pills-sm mb-2';
                                packs.forEach((pack: Pack, index: number) => {
                                    const button = document.createElement('button');
                                    button.className = 'nav-link';
                                    button.textContent = `Pct ${index + 1}`;
                                    button.dataset.packIndex = String(index);
                                    if (index === 0) button.classList.add('active');
                                    navContainer.appendChild(button);
                                });
                                groupWrapper.appendChild(navContainer);

                                navContainer.addEventListener('click', (e) => {
                                    const target = e.target as HTMLElement;
                                    if (target.tagName === 'BUTTON') {
                                        navContainer.querySelector('.active')?.classList.remove('active');
                                        target.classList.add('active');
                                        const packIndex = parseInt(target.dataset.packIndex!, 10);
                                        this.renderPackDetails(packs[packIndex], detailsContainer, statTemplate, buffTemplate, renderBuffsToList);
                                    }
                                });
                            }
                            
                            groupWrapper.appendChild(detailsContainer);
                            this.renderPackDetails(packs[0], detailsContainer, statTemplate, buffTemplate, renderBuffsToList);
                            this.cardBody!.appendChild(groupWrapper);
                        } catch (innerError) {
                            console.error(`ResourceInfoCard: Erro ao renderizar o grupo de packs '${cropName}' da Crop Machine.`, innerError);
                        }
                    });
                }
            } catch (error) {
                console.error("ResourceInfoCard: Erro ao renderizar a fila de pacotes da Crop Machine.", error);
            }
        }
    }

    private renderPackDetails(pack: Pack, container: HTMLElement, statTemplate: HTMLTemplateElement, buffTemplate: HTMLTemplateElement, renderBuffsToList: Function) {
        container.innerHTML = '';
        const statsList = document.createElement('ul');
        statsList.className = 'list-group list-group-flush';

        const addStat = (label: string, value: string | number | undefined | null, valueClass?: string) => {
            if (value === undefined || value === null) return;
            const clone = statTemplate.content.cloneNode(true) as DocumentFragment;
            clone.querySelector('.stat-label')!.textContent = label;
            const valueEl = clone.querySelector('.stat-value')! as HTMLElement;
            valueEl.textContent = String(value);
            if (valueClass) valueEl.classList.add(...valueClass.split(' '));
            statsList.appendChild(clone);
        };

        const addBuffs = (buffs: Buff[] | undefined, title: string, isTimeBonus: boolean = false) => {
            if (!buffs || buffs.length === 0) return;
            const titleEl = document.createElement('h6');
            titleEl.className = 'mt-3 mb-1 small text-muted';
            titleEl.textContent = title;
            statsList.appendChild(titleEl);
            renderBuffsToList(buffs, statsList, isTimeBonus);
        };

        addStat('Estado', pack.is_ready ? 'Pronto' : 'Processando');
        addStat('Sementes', pack.seeds);
        addStat('Rendimento Previsto', (pack.yield_info?.final_deterministic ?? 0).toFixed(2));
        if (pack.yield_info?.average_yield_per_seed) {
            addStat('Média por Semente', pack.yield_info.average_yield_per_seed.toFixed(2));
        }
        if (pack.oil_cost) {
            addStat('Custo de Óleo', pack.oil_cost.toLocaleString('pt-BR', { maximumFractionDigits: 2 }));
        }
        if (!pack.is_ready) {
            addStat('Pronto em', this.formatFullDateTime(pack.readyAt));
        }

        container.appendChild(statsList);

        const yieldBuffs = pack.yield_info?.applied_buffs;
        addBuffs(yieldBuffs, 'Bônus de Rendimento', false);

        if (yieldBuffs) {
            const shouldShowDisclaimer = yieldBuffs.some((b: Buff) => 
                b.operation === 'multiply' && 
                b.source_item.includes('(Critical Hit)') && 
                b.total_bonus_yield && b.total_bonus_yield > 0
            );

            if (shouldShowDisclaimer) {
                const disclaimer = this.createDisclaimer(
                    `<i class="bi bi-info-circle me-1"></i> <strong>Nota:</strong> O valor 'Total' de um 'Critical Hit' é o ganho real, calculado após a aplicação de outros bônus multiplicativos.`
                );
                statsList.appendChild(disclaimer);
            }
        }
    }

    private renderPotDetails(pot: Pot, container: HTMLElement, statTemplate: HTMLTemplateElement, buffTemplate: HTMLTemplateElement, renderBuffsToList: Function) {
        container.innerHTML = '';
        const potStatsList = document.createElement('ul');
        potStatsList.className = 'list-group list-group-flush';

        const addPotStat = (label: string, value: string | number | undefined | null) => {
            if (value === undefined || value === null) return;
            const clone = statTemplate.content.cloneNode(true) as HTMLElement;
            clone.querySelector('.stat-label')!.textContent = label;
            clone.querySelector('.stat-value')!.textContent = String(value);
            potStatsList.appendChild(clone);
        };
        
        addPotStat('Estado', pot.state_name);
        addPotStat('Rendimento/Vaso', pot.calculations.yield.final_deterministic.toFixed(2));
        if (pot.state_name !== 'Pronta') {
            addPotStat('Pronta em', this.timeRemaining(pot.ready_at_timestamp_ms));
        }

        container.appendChild(potStatsList);

        const yieldBuffs = pot.calculations?.yield?.applied_buffs || [];
        const timeBuffs = pot.calculations?.growth?.applied_buffs || [];

        const renderBuffSection = (title: string, buffs: Buff[], targetList: HTMLElement, isTimeBonus: boolean = false) => {
            if (buffs.length === 0) return;
            const titleEl = document.createElement('h6');
            titleEl.className = 'mt-2 mb-1 small text-muted';
            titleEl.textContent = title;
            targetList.appendChild(titleEl);

            const buffList = document.createElement('ul');
            buffList.className = 'list-group list-group-flush';
            renderBuffsToList(buffs, buffList, isTimeBonus);
            targetList.appendChild(buffList);
        };

        renderBuffSection('Bônus de Rendimento', yieldBuffs, potStatsList, false);

        if (yieldBuffs && yieldBuffs.length > 0) {
            const shouldShowDisclaimer = yieldBuffs.some((b: Buff) => 
                b.operation === 'multiply' && 
                b.source_item.includes('(Critical Hit)') && 
                b.total_bonus_yield && b.total_bonus_yield > 0
            );

            if (shouldShowDisclaimer) {
                const disclaimer = this.createDisclaimer(
                    `<i class="bi bi-info-circle me-1"></i> <strong>Nota:</strong> O valor 'Total' de um 'Critical Hit' é o ganho real, calculado após a aplicação de outros bônus multiplicativos.`
                );
                disclaimer.classList.add('list-group-item');
                potStatsList.appendChild(disclaimer);
            }
        }

        renderBuffSection('Bônus de Tempo', timeBuffs, potStatsList, true);
    }

    /**
     * Cria um elemento de disclaimer padronizado.
     * @param innerHTML O conteúdo HTML a ser inserido no disclaimer.
     * @returns O elemento HTMLElement do disclaimer.
     */
    private createDisclaimer(innerHTML: string): HTMLElement {
        const disclaimer = document.createElement('p');
        disclaimer.className = 'small mb-0 mt-2 p-2 bg-secondary-subtle text-secondary-emphasis border border-secondary-subtle rounded';
        disclaimer.innerHTML = innerHTML;
        return disclaimer;
    }
}
