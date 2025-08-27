// typescript/card_positioner.ts

/**
 * Módulo utilitário para posicionar de forma inteligente um card flutuante na tela.
 * Esta função centraliza a lógica de posicionamento para evitar duplicação de código
 * entre `resource_info_card.ts` e `summary_card.ts`.
 */

/**
 * Calcula e aplica a posição ótima para um card flutuante em relação a um elemento âncora, garantindo que
 * ele permaneça dentro da área visível da janela e não sobreponha a âncora.
 * @param cardElement O elemento do card flutuante a ser posicionado.
 * @param anchorElement O elemento ao qual o card deve se posicionar.
 */
export function positionCard(cardElement: HTMLElement, anchorElement: HTMLElement) {
    // Torna o card mensurável, mas invisível, para obter suas dimensões.
    cardElement.style.visibility = 'hidden';
    cardElement.style.display = 'block';

    const cardRect = cardElement.getBoundingClientRect();
    const anchorRect = anchorElement.getBoundingClientRect();
    const margin = 15; // Espaçamento da âncora e das bordas da tela

    // --- Posicionamento Vertical ---
    // Tenta alinhar o topo do card com o topo da âncora.
    let top = anchorRect.top;
    // Se sair da tela por baixo, alinha sua base com a base da janela.
    if (top + cardRect.height > window.innerHeight - margin) {
        top = window.innerHeight - cardRect.height - margin;
    }
    // Garante que não saia da tela por cima.
    top = Math.max(margin, top);

    // --- Posicionamento Horizontal ---
    // Tenta posicionar à direita da âncora primeiro.
    let left = anchorRect.right + margin;

    // Se sair da tela pela direita, posiciona à esquerda da âncora.
    if (left + cardRect.width > window.innerWidth - margin) {
        left = anchorRect.left - cardRect.width - margin;
    }

    // NOVO: Verificação de sobreposição.
    // Se a posição calculada sobrepõe a âncora (comum em telas estreitas),
    // tenta mover para o outro lado como último recurso.
    const finalCardRect = { x: left, y: top, width: cardRect.width, height: cardRect.height };
    const overlaps = !(
        finalCardRect.x + finalCardRect.width < anchorRect.left ||
        finalCardRect.x > anchorRect.right ||
        finalCardRect.y + finalCardRect.height < anchorRect.top ||
        finalCardRect.y > anchorRect.bottom
    );

    if (overlaps) {
        // Se estava tentando ir para a esquerda (porque não coube na direita) e sobrepôs,
        // força a ida para a direita.
        if (left < anchorRect.left) {
            left = anchorRect.right + margin;
        } 
        // Se estava tentando ir para a direita e sobrepôs (improvável, mas possível),
        // força a ida para a esquerda.
        else {
            left = anchorRect.left - cardRect.width - margin;
        }
    }

    // Garante que o card não saia das bordas da tela no final.
    left = Math.max(margin, Math.min(left, window.innerWidth - cardRect.width - margin));

    // Aplica a posição final e torna o card visível.
    cardElement.style.left = `${left}px`;
    cardElement.style.top = `${top}px`;
    cardElement.style.visibility = 'visible';
}

/**
 * Calcula e aplica a posição ótima para um card flutuante em relação a um GRUPO de elementos,
 * garantindo que ele permaneça dentro da área visível da janela e não sobreponha nenhum dos elementos do grupo.
 * @param cardElement O elemento do card flutuante a ser posicionado.
 * @param targetElements A lista de elementos que o card não deve sobrepor.
 */
export function positionCardAroundGroup(cardElement: HTMLElement, targetElements: NodeListOf<HTMLElement>) {
    if (targetElements.length === 0) {
        cardElement.style.display = 'none';
        return;
    }

    // Torna o card mensurável, mas invisível, para obter suas dimensões.
    cardElement.style.visibility = 'hidden';
    cardElement.style.display = 'block';

    const cardRect = cardElement.getBoundingClientRect();
    const margin = 15;

    // 1. Obtém todos os retângulos delimitadores para os elementos de destino e calcula o retângulo delimitador geral do grupo.
    const elementRects: DOMRect[] = [];
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;

    targetElements.forEach(element => {
        const rect = element.getBoundingClientRect();
        elementRects.push(rect);
        minX = Math.min(minX, rect.left);
        minY = Math.min(minY, rect.top);
        maxX = Math.max(maxX, rect.right);
        maxY = Math.max(maxY, rect.bottom);
    });

    const groupRect = { left: minX, top: minY, right: maxX, bottom: maxY };

    // 2. Define posições candidatas ao redor do grupo.
    const candidatePositions = [
        { left: groupRect.right + margin, top: groupRect.top }, // À direita do grupo
        { left: groupRect.left - cardRect.width - margin, top: groupRect.top }, // À esquerda do grupo
        { left: groupRect.left, top: groupRect.bottom + margin }, // Abaixo
        { left: groupRect.left, top: groupRect.top - cardRect.height - margin } // Acima
    ];

    let bestPosition: { left: number; top: number } | null = null;

    // 3. Encontra a primeira posição candidata que não sobrepõe nenhum elemento individual.
    for (const pos of candidatePositions) {
        const candidateCardRect = { left: pos.left, top: pos.top, width: cardRect.width, height: cardRect.height, right: pos.left + cardRect.width, bottom: pos.top + cardRect.height };

        const overlapsAny = elementRects.some(elementRect => 
            !(candidateCardRect.right < elementRect.left || candidateCardRect.left > elementRect.right || candidateCardRect.bottom < elementRect.top || candidateCardRect.top > elementRect.bottom)
        );

        if (!overlapsAny) {
            bestPosition = pos;
            break;
        }
    }

    // 4. Se todos os candidatos se sobrepõem, usa a primeira posição como fallback.
    if (!bestPosition) bestPosition = candidatePositions[0];

    // 5. Garante que a posição final esteja dentro da tela e aplica.
    const finalLeft = Math.max(margin, Math.min(bestPosition.left, window.innerWidth - cardRect.width - margin));
    const finalTop = Math.max(margin, Math.min(bestPosition.top, window.innerHeight - cardRect.height - margin));

    cardElement.style.left = `${finalLeft}px`;
    cardElement.style.top = `${finalTop}px`;
    cardElement.style.visibility = 'visible';
}