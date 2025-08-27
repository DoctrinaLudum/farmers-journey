import { Currency, CurrencyConverter } from "./currency_converter.js";

const CURRENCY_STORAGE_KEY = 'preferredCurrency';

export class FloatingControlPanel {
    private converter: CurrencyConverter;
    private container: HTMLElement | null;
    private toggleButton: HTMLElement | null;
    private refreshButton: HTMLElement | null;
    private idleTimer?: number;

    constructor(converter: CurrencyConverter) {
        this.converter = converter;
        this.container = document.querySelector('.floating-controls-container');
        this.toggleButton = document.getElementById('floating-controls-toggle');
        this.refreshButton = document.getElementById('refresh-farm-data');
    }

    public init(): void {
        if (!this.container || !this.toggleButton) return;

        this.setupEventListeners();
        this.loadAndApplyPreferredCurrency();
        this.setupIdleTimer();
    }

    private setupEventListeners(): void {
        this.toggleButton?.addEventListener('click', () => {
            this.container?.classList.toggle('open');
        });

        document.querySelectorAll<HTMLInputElement>('input[name="currency-selector"]').forEach(radio => {
            radio.addEventListener('change', (event) => {
                const target = event.target as HTMLInputElement;
                const newCurrency = target.value as Currency;
                this.applyCurrencyClass(newCurrency);
                localStorage.setItem(CURRENCY_STORAGE_KEY, newCurrency);
            });
        });

        this.refreshButton?.addEventListener('click', () => {
            // Lógica para a chamada de API de atualização virá aqui
            this.refreshButton?.classList.add('loading');
            console.log("Atualizando dados...");
            // Simula uma chamada de API
            setTimeout(() => {
                this.refreshButton?.classList.remove('loading');
                console.log("Dados atualizados!");
            }, 2000);
        });
    }

    private loadAndApplyPreferredCurrency(): void {
        const preferredCurrency = localStorage.getItem(CURRENCY_STORAGE_KEY) as Currency || 'Flower';
        const radio = document.getElementById(`currency-${preferredCurrency.toLowerCase()}`) as HTMLInputElement;
        if (radio) {
            radio.checked = true;
        }
        this.applyCurrencyClass(preferredCurrency);
    }

    /**
     * NOVO: Aplica a classe de moeda ao body para controlar a visibilidade via CSS.
     */
    private applyCurrencyClass(currency: Currency): void {
        const body = document.body;
        // Remove qualquer classe de moeda anterior (ex: 'show-usd', 'show-brl')
        body.className = body.className.replace(/\bshow-\w+/g, '').trim();
        // Adiciona a nova classe
        body.classList.add(`show-${currency.toLowerCase()}`);
    }

    /**
     * NOVO: Configura um temporizador para esmaecer o painel após um período de inatividade.
     */
    private setupIdleTimer(): void {
        const IDLE_TIMEOUT = 5000; // 5 segundos

        const setIdle = () => {
            this.container?.classList.add('is-idle');
        };

        const resetIdleTimer = () => {
            this.container?.classList.remove('is-idle');
            window.clearTimeout(this.idleTimer);
            this.idleTimer = window.setTimeout(setIdle, IDLE_TIMEOUT);
        };

        // Eventos que indicam atividade do usuário
        ['mousemove', 'mousedown', 'keydown', 'scroll', 'touchstart'].forEach(event => {
            document.addEventListener(event, resetIdleTimer, { passive: true });
        });

        resetIdleTimer(); // Inicia o temporizador
    }
}
