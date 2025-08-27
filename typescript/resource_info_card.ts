// typescript/resource_info_card.ts
import { positionCard } from './card_positioner.js';

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
    private populateCard(data: any) {
        const analysisData = data.analysis;
        const resourceName = analysisData.crop_name || analysisData.fruit_name || analysisData.tree_name || analysisData.resource_name || analysisData.name || 'Recurso';
        this.cardTitle!.textContent = resourceName;

        const iconPath = data.base_building_icon || data.icon;

        if (iconPath) {
            this.cardIcon!.src = `/static/${iconPath}`;
        } else {
            this.cardIcon!.src = ''; // Fallback para evitar erros
        }
        
        this.cardBody!.innerHTML = ''; // Limpa o corpo do card

        const statTemplate = document.getElementById('resource-card-stat-template') as HTMLTemplateElement;
        const buffTemplate = document.getElementById('resource-card-buff-template') as HTMLTemplateElement;
        const statsList = document.createElement('ul');
        statsList.className = 'list-group list-group-flush';

        const renderBuffsToList = (buffs: any[], targetList: HTMLElement) => {
            if (!buffs || buffs.length === 0) return;

            const sourceTypeToLabel: { [key: string]: string } = {
                skill: '(Skill)',
                skill_legacy: '(Skill Legacy)',
                collectible: '(Collectible)',
                wearable: '(Wearable)',
                bud: '(Bud)',
                game_mechanic: '(Nativo)',
                fertiliser: '(Fertilizante)',
                tool: '(Ferramenta)'
            };

            buffs.forEach(buff => {
                const clone = buffTemplate.content.cloneNode(true) as DocumentFragment;
                
                const prefix = sourceTypeToLabel[buff.source_type] || '';
                const typeClass = buff.source_type ? `is-type-${buff.source_type}` : '';
                const prefixTag = prefix ? `<span class="buff-source-tag ${typeClass}">${prefix}</span>` : '';
                const buffCount = buff.count > 1 ? ` (x${buff.count})` : '';

                clone.querySelector('.buff-source')!.innerHTML = `${prefixTag} ${buff.source_item}${buffCount}`.trim();
                let valueText = '';
                const buffValue = buff.value;

                if (typeof buffValue === 'number') {
                    if (buff.operation === 'add') valueText = `+${buffValue.toFixed(2)}`;
                    else if (buff.operation === 'multiply') valueText = `x${buffValue.toFixed(2)}`;
                    else if (buff.operation === 'percentage') valueText = `${(buffValue * 100).toFixed(0)}%`;
                    else valueText = String(buffValue);
                } else {
                    valueText = String(buffValue);
                }

                const valueEl = clone.querySelector('.buff-value')!;
                valueEl.textContent = valueText;
                if (typeof buffValue === 'number') {
                    valueEl.classList.add(buffValue > 0 ? 'text-success' : 'text-danger');
                }

                targetList.appendChild(clone);
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

        const addBuffs = (title: string, buffs: any[]) => {
            if (!buffs || buffs.length === 0) return;
            
            const titleEl = document.createElement('h6');
            titleEl.className = 'mt-2 mb-1 small text-muted';
            titleEl.textContent = title;
            statsList.appendChild(titleEl);
            
            renderBuffsToList(buffs, statsList);
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
                // Menos de 10 minutos (mais crítico)
                if (remainingSeconds < 10 * 60) {
                    criticalityClass = 'text-danger fw-bold';
                } 
                // Menos de 1 hora
                else if (remainingSeconds < 60 * 60) {
                    criticalityClass = 'text-warning fw-bold';
                }
                // Menos de 12 horas (aviso)
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
            // Para cogumelos e outros recursos que não usam a estrutura 'calculations'
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
            addBuffs('Bônus de Rendimento', analysisData.calculations.yield.applied_buffs);
        }
        const recoveryBuffs = analysisData.calculations?.recovery?.applied_buffs || analysisData.calculations?.growth?.applied_buffs;
        if (recoveryBuffs) {
            addBuffs('Bônus de Tempo', recoveryBuffs);
        }

        // NOVO: Adiciona a lista de bônus aplicados para cogumelos (padronizado)
        if (analysisData.applied_boosts && analysisData.applied_boosts.length > 0) { // analysisData.applied_boosts já é uma lista de objetos
            // Usa a função helper padrão para exibir os bônus com o título correto e as tags de origem.
            addBuffs('Bônus de Rendimento', analysisData.applied_boosts);
        }

        // NOVO: Adiciona o resumo de spawn para cogumelos com data/hora completa
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
            const pots = Object.values(analysisData.pots as any[]);
            const plantsInPots = pots.map((pot: any) => pot.plant_name).filter(Boolean);
            const uniquePlants = [...new Set(plantsInPots)];

            if (uniquePlants.length === 0) {
                this.cardTitle!.textContent = 'Greenhouse (Vazia)';
            } else {
                if (uniquePlants.length === 1) {
                    this.cardTitle!.textContent = `Greenhouse (${uniquePlants[0]})`;
                } else {
                    this.cardTitle!.textContent = `Greenhouse (${uniquePlants.length} plantas diferentes)`;
                }
            }

            if (pots.length === 0) {
                const noItemsEl = document.createElement('p');
                noItemsEl.className = 'text-muted small mt-2 mb-0';
                noItemsEl.textContent = 'Nenhum vaso com plantas.';
                this.cardBody!.appendChild(noItemsEl);
            } else {
                const groupedPots = new Map<string, any[]>();
                pots.forEach((pot: any) => {
                    const yieldValue = (pot.calculations?.yield?.final_deterministic ?? 0).toFixed(2);
                    const readyTime = this.timeRemaining(pot.ready_at_timestamp_ms);
                    const groupKey = `${pot.plant_name}|${pot.state_name}|${yieldValue}|${readyTime}`;

                    if (!groupedPots.has(groupKey)) {
                        groupedPots.set(groupKey, []);
                    }
                    groupedPots.get(groupKey)!.push(pot);
                });

                let firstGroup = true;
                Array.from(groupedPots.values()).forEach((potGroup: any[], groupIndex: number) => {
                    if (!firstGroup) {
                        this.cardBody!.appendChild(document.createElement('hr'));
                    }
                    firstGroup = false;

                    const firstPot = potGroup[0];
                    const potIds = potGroup.map(p => `#${p.id}`).join(', ');

                    const potHeader = document.createElement('h6');
                    potHeader.className = 'd-flex align-items-center small mt-2';
                    potHeader.innerHTML = `
                        <img src="/static/${firstPot.icon_path}" class="icon icon-2x me-2">
                        <span>${firstPot.plant_name} (Vaso ${potIds})</span>
                    `;
                    this.cardBody!.appendChild(potHeader);

                    const potStatsList = document.createElement('ul');
                    potStatsList.className = 'list-group list-group-flush';

                    const addPotStat = (label: string, value: string | number | undefined | null) => {
                        if (value === undefined || value === null) return;
                        const clone = statTemplate.content.cloneNode(true) as HTMLElement;
                        clone.querySelector('.stat-label')!.textContent = label;
                        clone.querySelector('.stat-value')!.textContent = String(value);
                        potStatsList.appendChild(clone);
                    };
                    
                    addPotStat('Estado', firstPot.state_name);
                    addPotStat('Rendimento/Vaso', firstPot.calculations.yield.final_deterministic.toFixed(2));
                    if (firstPot.state_name !== 'Pronta') {
                        addPotStat('Pronta em', this.timeRemaining(firstPot.ready_at_timestamp_ms));
                    }

                    if (potGroup.length > 1) {
                        const totalYield = potGroup.reduce((sum, p) => sum + p.calculations.yield.final_deterministic, 0);
                        addPotStat('Rendimento Total (Grupo)', totalYield.toFixed(2));
                    }
                    this.cardBody!.appendChild(potStatsList);

                    const yieldBuffs = firstPot.calculations?.yield?.applied_buffs || [];
                    const timeBuffs = firstPot.calculations?.growth?.applied_buffs || [];
                    const allBuffs = [...yieldBuffs, ...timeBuffs];

                    if (allBuffs.length > 0) {
                        const accordionId = `pot-buffs-collapse-${groupIndex}`;
                        const accordionParentId = `accordion-pot-${groupIndex}`;

                        const accordionItem = document.createElement('li');
                        accordionItem.className = 'list-group-item px-0 py-1';
                        accordionItem.innerHTML = `
                            <div class="accordion accordion-flush" id="${accordionParentId}">
                            <div class="accordion-item bg-transparent">
                                <h2 class="accordion-header">
                                    <button class="accordion-button accordion-button-sm collapsed py-1" type="button" data-bs-toggle="collapse" data-bs-target="#${accordionId}">
                                        Bônus Aplicados (${allBuffs.length})
                                    </button>
                                </h2>
                                <div id="${accordionId}" class="accordion-collapse collapse" data-bs-parent="#${accordionParentId}">
                                    <div class="accordion-body pt-1 pb-0">
                                        <!-- As seções de bônus serão renderizadas aqui -->
                                    </div>
                                </div>
                            </div>
                        `;
                        
                        const accordionBody = accordionItem.querySelector('.accordion-body') as HTMLElement;

                        const renderBuffSection = (title: string, buffs: any[], targetElement: HTMLElement) => {
                            if (buffs.length === 0) return;
                            const titleEl = document.createElement('h6');
                            titleEl.className = 'mt-2 mb-1 small text-muted';
                            titleEl.textContent = title;
                            targetElement.appendChild(titleEl);

                            const buffList = document.createElement('ul');
                            buffList.className = 'list-group list-group-flush';
                            renderBuffsToList(buffs, buffList);
                            targetElement.appendChild(buffList);
                        };

                        renderBuffSection('Bônus de Rendimento', yieldBuffs, accordionBody);
                        renderBuffSection('Bônus de Tempo', timeBuffs, accordionBody);

                        potStatsList.appendChild(accordionItem);
                    }
                });
            }
        }

        if (data.type === 'Crop Machine' && analysisData.queue) {
            const queueCrops = analysisData.queue.map((pack: any) => pack.crop);
            const uniqueCrops = [...new Set(queueCrops)];

            if (uniqueCrops.length === 0) {
                this.cardTitle!.textContent = 'Crop Machine (Vazia)';
            } else if (uniqueCrops.length === 1) {
                this.cardTitle!.textContent = `Crop Machine (${uniqueCrops[0]})`;
            } else {
                this.cardTitle!.textContent = `Crop Machine (${uniqueCrops.length} plantas diferentes)`;
            }

            const queue = analysisData.queue as any[];
            if (queue.length === 0) {
                const noItemsEl = document.createElement('p');
                noItemsEl.className = 'text-muted small mt-2 mb-0';
                noItemsEl.textContent = 'Nenhum pacote na fila.';
                this.cardBody!.appendChild(noItemsEl);
            } else {
                queue.forEach((pack: any, index: number) => {
                    if (index > 0) {
                        this.cardBody!.appendChild(document.createElement('hr'));
                    }

                    const packHeader = document.createElement('h6');
                    packHeader.className = 'd-flex align-items-center small mt-2';
                    packHeader.innerHTML = `
                        <img src="/static/${pack.icon_path}" class="icon icon-2x me-2">
                        <span>${pack.crop}</span>
                    `;
                    this.cardBody!.appendChild(packHeader);

                    const packStatsList = document.createElement('ul');
                    packStatsList.className = 'list-group list-group-flush';

                    const addPackStat = (label: string, value: string | number | undefined | null) => {
                        if (value === undefined || value === null) return;
                        const clone = statTemplate.content.cloneNode(true) as HTMLElement;
                        clone.querySelector('.stat-label')!.textContent = label;
                        clone.querySelector('.stat-value')!.textContent = String(value);
                        packStatsList.appendChild(clone);
                    };
                    
                    addPackStat('Estado', pack.is_ready ? 'Pronto' : 'Processando');
                    addPackStat('Sementes', pack.seeds);
                    addPackStat('Rendimento Previsto', (pack.yield_info?.final_deterministic ?? 0).toFixed(2));
                    if (pack.oil_cost) {
                        addPackStat('Custo de Óleo', pack.oil_cost.toLocaleString('pt-BR', { maximumFractionDigits: 0 }));
                    }
                    if (!pack.is_ready) {
                        const readyDate = new Date(pack.readyAt).toLocaleString('pt-BR');
                        addPackStat('Pronto em', readyDate);
                    }

                    if (pack.yield_info?.applied_buffs?.length > 0) {
                        const allBuffs = pack.yield_info.applied_buffs;

                        const yieldBuffs = allBuffs.filter((b: any) => b.type === 'YIELD' || b.type === 'BONUS_YIELD_CHANCE');
                        const timeBuffs = allBuffs.filter((b: any) => b.type === 'RECOVERY_TIME' || b.type === 'GROWTH_TIME');

                        if (yieldBuffs.length > 0 || timeBuffs.length > 0) {
                            const accordionId = `pack-buffs-collapse-${index}`;
                            const accordionParentId = `accordion-pack-${index}`;

                            const accordionItem = document.createElement('li');
                            accordionItem.className = 'list-group-item px-0 py-1';
                            accordionItem.innerHTML = `
                                <div class="accordion accordion-flush" id="${accordionParentId}">
                                <div class="accordion-item bg-transparent">
                                    <h2 class="accordion-header">
                                        <button class="accordion-button accordion-button-sm collapsed py-1" type="button" data-bs-toggle="collapse" data-bs-target="#${accordionId}">
                                            Bônus Aplicados (${allBuffs.length})
                                        </button>
                                    </h2>
                                    <div id="${accordionId}" class="accordion-collapse collapse" data-bs-parent="#${accordionParentId}">
                                        <div class="accordion-body pt-1 pb-0">
                                            <!-- As seções de bônus serão renderizadas aqui -->
                                        </div>
                                    </div>
                                </div>
                            `;
                            
                            const accordionBody = accordionItem.querySelector('.accordion-body') as HTMLElement;

                            const renderBuffSection = (title: string, buffs: any[], targetElement: HTMLElement) => {
                                if (buffs.length === 0) return;
                                const titleEl = document.createElement('h6');
                                titleEl.className = 'mt-2 mb-1 small text-muted';
                                titleEl.textContent = title;
                                targetElement.appendChild(titleEl);

                                const buffList = document.createElement('ul');
                                buffList.className = 'list-group list-group-flush';
                                renderBuffsToList(buffs, buffList);
                                targetElement.appendChild(buffList);
                            };

                            renderBuffSection('Bônus de Rendimento', yieldBuffs, accordionBody);
                            renderBuffSection('Bônus de Tempo', timeBuffs, accordionBody);

                            packStatsList.appendChild(accordionItem);
                        };
                    }
                    this.cardBody!.appendChild(packStatsList);
                });
            }
        }
    }
}