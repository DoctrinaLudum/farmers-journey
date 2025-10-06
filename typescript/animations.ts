interface AnimatedCharacter {
    type: string;
    name: string;
}

let idleTimer: number;
let lastMousePosition = { x: 0, y: 0 };

/**
 * Busca a lista de personagens animados da API do backend.
 * @returns Uma promessa que resolve para uma lista de personagens ou uma lista vazia em caso de erro.
 */
async function fetchAnimatedCharacters(): Promise<AnimatedCharacter[]> {
    try {
        const response = await fetch('/api/animated-characters');
        if (!response.ok) {
            console.error('Falha ao buscar personagens animados:', response.statusText);
            return [];
        }
        const characters: AnimatedCharacter[] = await response.json();
        return characters;
    } catch (error) {
        console.error('Erro de rede ao buscar personagens animados:', error);
        return [];
    }
}

/**
 * Cria e exibe um personagem animado na tela.
 * @param container O elemento HTML onde o personagem será adicionado.
 * @param characters A lista de personagens disponíveis para escolher.
 */
function spawnRandomCharacter(container: Element, characters: AnimatedCharacter[]) {
    const walkingCharacters = characters.filter(c => !c.name.includes('_asleep'));

    if (walkingCharacters.length === 0) {
        console.log("Nenhum personagem animado para exibir (após filtrar).");
        return;
    }

    const randomCharacter = walkingCharacters[Math.floor(Math.random() * walkingCharacters.length)];
    
    const walker = document.createElement('div');
    const characterImage = document.createElement('img');

    const imageUrl = `/static/images/${randomCharacter.type}/${randomCharacter.name}`;
    
    characterImage.src = imageUrl;
    characterImage.alt = `Animated character: ${randomCharacter.name.split('.')[0]}`;
    
    let directionClass = 'walk-ltr';
    if (randomCharacter.type === 'pets' || randomCharacter.type === 'animals') {
        directionClass = 'walk-rtl';
    }
    walker.className = `walking-character ${directionClass}`;

    const randomDuration = Math.random() * 15 + 15;
    const randomDelay = Math.random() * 5;

    walker.style.animationDuration = `${randomDuration}s`;
    walker.style.animationDelay = `${randomDelay}s`;

    walker.style.opacity = '0';
    walker.addEventListener('animationstart', () => {
        walker.style.opacity = '1';
    }, { once: true });

    walker.appendChild(characterImage);
    container.appendChild(walker);

    walker.addEventListener('animationend', () => {
        walker.remove();
    });
}

/**
 * Aciona a animação de pulo para um personagem, fazendo-o desviar para frente.
 * @param walkerElement O elemento 'walker' do personagem que deve pular.
 */
function triggerJump(walkerElement: HTMLElement) {
    if (walkerElement.classList.contains('reacting')) return;

    const imageElement = walkerElement.querySelector('img');
    if (!imageElement) return;

    walkerElement.classList.add('reacting');

    const JUMP_DURATION_MS = 1500; // Duração de 1.5s como solicitado.
    const isRTL = walkerElement.classList.contains('walk-rtl');
    
    const jumpForwardsX = isRTL ? 'translateX(-150px)' : 'translateX(150px)';
    const jumpUpY = 'translateY(-110px)';

    imageElement.style.transition = `transform ${JUMP_DURATION_MS / 2}ms ease-out`;
    imageElement.style.transform = `${jumpUpY} ${jumpForwardsX}`;

    setTimeout(() => {
        imageElement.style.transition = `transform ${JUMP_DURATION_MS / 2}ms ease-in`;
        imageElement.style.transform = `translateY(0) ${jumpForwardsX}`;
    }, JUMP_DURATION_MS / 2);

    setTimeout(() => {
        imageElement.style.transition = '';
        walkerElement.classList.remove('reacting');
    }, JUMP_DURATION_MS);
}

/**
 * Aciona a animação de fuga para um personagem.
 * @param walkerElement O elemento 'walker' do personagem que deve fugir.
 */
function triggerFlee(walkerElement: HTMLElement) {
    if (walkerElement.classList.contains('reacting')) return;

    walkerElement.classList.add('reacting');
    walkerElement.style.animationPlayState = 'paused';

    const imageElement = walkerElement.querySelector('img');
    if (!imageElement) {
        walkerElement.remove();
        return;
    }

    imageElement.style.transition = 'transform 0.4s ease-in';
    walkerElement.style.transition = 'opacity 0.4s ease-in';

    const isRTL = walkerElement.classList.contains('walk-rtl');
    const jumpBackDirection = isRTL ? 'translateX(60px)' : 'translateX(-60px)';

    imageElement.style.transform = `${jumpBackDirection} translateY(-30px)`;
    walkerElement.style.opacity = '0';

    setTimeout(() => {
        walkerElement.remove();
    }, 400);
}

/**
 * Verifica continuamente por colisões entre animais e NPCs.
 */
function checkCollisions() {
    const allWalkers = document.querySelectorAll('.walking-character');
    const animals: HTMLElement[] = [];
    const npcs: HTMLElement[] = [];

    allWalkers.forEach((walker) => {
        const htmlWalker = walker as HTMLElement;
        if (htmlWalker.classList.contains('walk-rtl')) {
            animals.push(htmlWalker);
        } else {
            npcs.push(htmlWalker);
        }
    });

    animals.forEach(animal => {
        if (animal.classList.contains('reacting')) return;

        const animalRect = animal.getBoundingClientRect();

        npcs.forEach(npc => {
            const npcRect = npc.getBoundingClientRect();

            const horizontalOverlap = animalRect.left < npcRect.right && animalRect.right > npcRect.left;
            const verticalOverlap = Math.abs(animalRect.top - npcRect.top) < 20;

            if (horizontalOverlap && verticalOverlap) {
                const action = Math.random() < 0.5 ? 'jump' : 'flee';
                if (action === 'jump') {
                    triggerJump(animal);
                } else {
                    triggerFlee(animal);
                }
            }
        });
    });
}

/**
 * Cria e anima partículas 'zzz' para um pet dormindo.
 * @param container O elemento container do pet.
 */
function createZzzParticles(container: HTMLElement) {
    for (let i = 0; i < 3; i++) {
        const particle = document.createElement('span');
        particle.className = 'zzz-particle';
        particle.textContent = 'z';
        particle.style.animationDelay = `${i * 0.5}s`;
        particle.style.left = `${Math.random() * 40 - 20}px`;
        container.appendChild(particle);
    }
}

/**
 * Aciona a sequência de 'acordar' para um pet.
 * @param event O evento de clique.
 */
function wakeUpPet(event: MouseEvent) {
    const petContainer = (event.currentTarget as HTMLElement);
    
    petContainer.removeEventListener('click', wakeUpPet);
    petContainer.style.cursor = 'default';

    const particles = petContainer.querySelectorAll('.zzz-particle');
    particles.forEach(p => p.remove());

    const image = petContainer.querySelector('img');
    const petPath = petContainer.dataset.petPath;

    if (!image || !petPath) return;

    const imageUrl = `/static/images/pets/${petPath}.webp`;
    image.src = imageUrl;

    petContainer.classList.add('is-waking-up');

    setTimeout(() => {
        petContainer.style.transition = 'opacity 0.5s';
        petContainer.style.opacity = '0';
        setTimeout(() => petContainer.remove(), 500);
    }, 900);
}

/**
 * Cria e exibe um pet dormindo em um local aleatório.
 * @param container O container principal de animações.
 * @param characters A lista de todos os personagens.
 */
function spawnSleepingPet(container: Element, characters: AnimatedCharacter[]) {
    const pets = characters.filter(c => c.type === 'pets' && c.name.endsWith('.webp'));
    if (pets.length === 0) return;

    const randomPet = pets[Math.floor(Math.random() * pets.length)];
    
    const petPath = randomPet.name;
    const basePetPath = petPath.replace('_asleep.webp', '').replace('.webp', '');
    const basePetName = basePetPath.substring(basePetPath.lastIndexOf('/') + 1);

    const petContainer = document.createElement('div');
    petContainer.className = 'sleeping-pet';
    petContainer.dataset.petPath = basePetPath;

    petContainer.style.top = `${Math.random() * 70 + 10}%`;
    petContainer.style.left = `${Math.random() * 70 + 10}%`;

    const characterImage = document.createElement('img');
    characterImage.src = `/static/images/pets/${basePetPath}_asleep.webp`;
    characterImage.alt = `Sleeping pet: ${basePetName}`;

    petContainer.appendChild(characterImage);
    
    createZzzParticles(petContainer);
    petContainer.addEventListener('click', wakeUpPet, { once: true });
    container.appendChild(petContainer);
}

/**
 * Faz o pet que está brincando fugir.
 * @param petElement O elemento do pet que está brincando.
 */
function makePlayingPetFlee(petElement: HTMLElement) {
    if (petElement.classList.contains('fleeing')) return;
    petElement.classList.add('fleeing');

    const removeTimerId = parseInt(petElement.dataset.removeTimerId || '0', 10);
    if (removeTimerId) {
        clearTimeout(removeTimerId);
    }

    const image = petElement.querySelector('img');
    if (image) {
        image.style.animation = 'none'; // Para a animação de 'brincar'
    }

    petElement.style.transition = 'opacity 0.3s ease-out, transform 0.3s ease-out';
    petElement.style.opacity = '0';
    petElement.style.transform = 'translateY(40px) scale(0.7)'; // Foge para baixo

    setTimeout(() => petElement.remove(), 300);
}

/**
 * Cria e exibe um pet brincando perto da última posição do mouse.
 * @param container O container principal de animações.
 * @param characters A lista de todos os personagens.
 * @param position A posição {x, y} onde o pet deve aparecer.
 */
function spawnPlayingPet(container: Element, characters: AnimatedCharacter[], position: { x: number, y: number }) {
    if (document.querySelector('.playing-pet')) {
        return;
    }

    const playfulPets = characters.filter(c => 
        c.type === 'pets' && 
        (c.name.includes('cat') || c.name.includes('dog')) &&
        !c.name.includes('_asleep')
    );

    if (playfulPets.length === 0) {
        console.log("Nenhum pet 'brincalhão' (gato/cachorro) encontrado.");
        return;
    }

    const randomPet = playfulPets[Math.floor(Math.random() * playfulPets.length)];
    const petName = randomPet.name.split('.')[0];

    const petContainer = document.createElement('div') as HTMLElement;
    petContainer.className = 'playing-pet';

    petContainer.style.left = `${position.x}px`;
    petContainer.style.top = `${position.y}px`;

    const characterImage = document.createElement('img');
    characterImage.src = `/static/images/${randomPet.type}/${randomPet.name}`;
    characterImage.alt = `Playing pet: ${petName}`;

    petContainer.appendChild(characterImage);
    container.appendChild(petContainer);

    const removeTimer = setTimeout(() => {
        petContainer.remove();
    }, 4000);
    petContainer.dataset.removeTimerId = String(removeTimer);
}

/**
 * Inicia a cena onde um pet segue o cursor do mouse.
 * @param container O container principal de animações.
 * @param characters A lista de todos os personagens.
 */
function startFollowingScene(container: Element, characters: AnimatedCharacter[]) {
    const pets = characters.filter(c => c.type === 'pets' && !c.name.includes('_asleep'));
    if (pets.length === 0) return;

    const randomPet = pets[Math.floor(Math.random() * pets.length)];
    const petName = randomPet.name.split('.')[0];

    const petElement = document.createElement('div');
    petElement.className = 'following-pet';

    const characterImage = document.createElement('img');
    characterImage.src = `/static/images/${randomPet.type}/${randomPet.name}`;
    characterImage.alt = `Following pet: ${petName}`;
    petElement.appendChild(characterImage);
    
    petElement.style.opacity = '0';
    container.appendChild(petElement);

    let petX = Math.random() * window.innerWidth;
    let petY = Math.random() * window.innerHeight;
    petElement.style.transform = `translate(${petX}px, ${petY}px)`;

    const speed = 0.05;
    let animationFrameId: number;
    let lastDirection = 1; // Assumindo que a imagem base vira para a esquerda (padrão)

    function followLoop() {
        const dx = lastMousePosition.x - petX;
        const dy = lastMousePosition.y - petY;

        petX += dx * speed;
        petY += dy * speed;

        petElement.style.transform = `translate(${petX}px, ${petY}px)`;

        let desiredScale = lastDirection;
        if (dx > 5) { // Movendo para a direita
            desiredScale = -1; // Vira para a direita (scaleX: -1)
        } else if (dx < -5) { // Movendo para a esquerda
            desiredScale = 1;  // Vira para a esquerda (scaleX: 1)
        }

        if (desiredScale !== lastDirection) {
            characterImage.style.transform = `scaleX(${desiredScale})`;
            lastDirection = desiredScale;
        }

        animationFrameId = requestAnimationFrame(followLoop);
    }

    // Atraso de 3 segundos antes de iniciar a cena
    const START_DELAY_MS = 3000;
    setTimeout(() => {
        petElement.style.opacity = '1';
        followLoop();
    }, START_DELAY_MS);

    const SCENE_DURATION_MS = 20000; // 20 segundos
    // O tempo total de vida do elemento inclui o atraso inicial
    setTimeout(() => {
        cancelAnimationFrame(animationFrameId);
        petElement.style.opacity = '0';
        setTimeout(() => petElement.remove(), 500);
    }, SCENE_DURATION_MS + START_DELAY_MS);
}

document.addEventListener('DOMContentLoaded', async () => {
    const animatedContainer = document.querySelector('.animated-npc-container');

    if (!animatedContainer) {
        console.log('Animation container not found, skipping animation.');
        return;
    }

    const characters = await fetchAnimatedCharacters();
    if (characters.length === 0) {
        console.log('No animated characters found.');
        return;
    }

    const scenes: ('walk' | 'sleep' | 'follow' | 'idle')[] = ['walk', 'sleep', 'follow', 'idle'];
    const sceneType = scenes[Math.floor(Math.random() * scenes.length)];
    console.log(`Scene type chosen: ${sceneType}`);

    const IDLE_TIMEOUT_MS = 5000;
    document.addEventListener('mousemove', (event) => {
        lastMousePosition = { x: event.clientX, y: event.clientY };

        if (sceneType === 'idle') {
            const playingPet = document.querySelector<HTMLElement>('.playing-pet');
            if (playingPet) {
                makePlayingPetFlee(playingPet);
                clearTimeout(idleTimer);
                return;
            }
            clearTimeout(idleTimer);
            idleTimer = window.setTimeout(() => {
                console.log('Mouse is idle, spawning a playing pet.');
                spawnPlayingPet(animatedContainer, characters, lastMousePosition);
            }, IDLE_TIMEOUT_MS);
        }
    }, { passive: true });

    if (sceneType === 'walk') {
        console.log('Scene type: Walking Characters.');
        const maxWalkingCharacters = 2;

        setInterval(() => {
            const currentWalkers = animatedContainer.querySelectorAll('.walking-character').length;
            
            if (currentWalkers < maxWalkingCharacters) {
                console.log(`Walkers: ${currentWalkers}/${maxWalkingCharacters}. Spawning one more.`);
                spawnRandomCharacter(animatedContainer, characters);
            }
        }, 5000);

        setInterval(checkCollisions, 100);
    } else if (sceneType === 'sleep') {
        console.log('Scene type: Sleeping Pet.');
        spawnSleepingPet(animatedContainer, characters);
    } else if (sceneType === 'follow') {
        console.log('Scene type: Follow Mouse.');
        startFollowingScene(animatedContainer, characters);
    } else if (sceneType === 'idle') {
        console.log("Idle scene active. Waiting for mouse to stop to spawn a pet.");
    }
});