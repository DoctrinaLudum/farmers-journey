// typescript/currency_converter.ts

// Define a estrutura de dados para as taxas de câmbio que esperamos da API.
export interface ExchangeRates {
    sfl: {
        // Permite qualquer código de moeda (usd, brl, eur, etc.) como chave
        [currencyCode: string]: number;
    };
    // Pode adicionar outras moedas base aqui, se necessário no futuro
}
// Define os tipos de moeda suportados e a chave para armazenamento local.
export type Currency = 'Flower' | 'BRL'| 'USD';
const CURRENCY_STORAGE_KEY = 'preferredCurrency';

// Mapeia cada moeda para seu símbolo, localidade e HTML da bandeira.
const CURRENCY_SYMBOLS: Record<Currency, { symbol: string, locale: string, flagHtml: string }> = {
    Flower: { symbol: 'Flower', locale: 'en-US', flagHtml: `<span class="fi fi-flower me-1"></span>` },
    USD: { symbol: 'US$', locale: 'en-US', flagHtml: `<span class="fi fi-us me-2"></span>` },
    BRL: { symbol: 'R$', locale: 'pt-BR', flagHtml: `<span class="fi fi-br me-2"></span>` },
};

export class CurrencyConverter {
    // A propriedade 'rates' agora é privada para garantir que seja definida apenas no construtor.
    private rates: ExchangeRates;

    // O construtor agora é privado. A criação de instâncias deve ser feita através do método estático `create`.
    // Isso garante que a instância só seja criada após o carregamento bem-sucedido das taxas.
    constructor(rates: ExchangeRates) {
        this.rates = rates;
    }

    /**
     * NOVO: Método de fábrica estático e assíncrono para criar uma instância do conversor.
     * Centraliza a lógica de busca de dados da API, tornando o componente autossuficiente.
     * @returns Uma promessa que resolve para uma instância de `CurrencyConverter` ou `null` em caso de erro.
     */
    public static async create(): Promise<CurrencyConverter | null> {
        try {
            const response = await fetch('/api/exchange-rates');
            if (!response.ok) {
                throw new Error(`Falha ao buscar taxas de câmbio: ${response.statusText}`);
            }
            const rates: ExchangeRates = await response.json();
            // Verifica se os dados recebidos são válidos antes de criar a instância.
            if (!rates || !rates.sfl) {
                throw new Error("Dados de taxas de câmbio recebidos são inválidos.");
            }
            return new CurrencyConverter(rates);
        } catch (error) {
            console.error("Erro ao criar o CurrencyConverter:", error);
            return null;
        }
    }

    /**
     * Converte um valor de SFL para a moeda de destino.
     * ALTERADO: Retorna `null` se a taxa de conversão não for encontrada.
     */
    private convert(sflValue: number, targetCurrency: Currency): number | null { // Alterado para retornar `number | null`
        if (targetCurrency === 'Flower' || !this.rates.sfl) {
            return sflValue;
        }

        const currencyCode = targetCurrency.toLowerCase();
        const rate = this.rates.sfl[currencyCode];

        if (typeof rate === 'number') {
            return sflValue * rate;
        }

        console.warn(`Taxa de câmbio para ${targetCurrency} não encontrada.`);
        return null; // Retorna null em caso de falha na conversão
    }

    /**
     * Formata um número como uma string de moeda.
     */
    private format(value: number, currency: Currency): string {
        const useMorePrecision = currency !== 'Flower' && value > 0 && value < 0.01;
        const config = CURRENCY_SYMBOLS[currency];
        const formattedValue = new Intl.NumberFormat(config.locale, {
            minimumFractionDigits: useMorePrecision ? 4 : 2,
            maximumFractionDigits: useMorePrecision ? 4 : 2,
        }).format(value);
        return currency === 'Flower' ? `${formattedValue} ${config.symbol}` : `${config.symbol} ${formattedValue}`;
    }

    /**
     * Converte e formata um único valor SFL para a moeda de destino.
     * Ideal para usar em conteúdo gerado dinamicamente.
     */
    public formatSflValue(sflValue: number, targetCurrency: Currency): string {
        const convertedValue = this.convert(sflValue, targetCurrency);
        // Se a conversão falhou, retorna um texto indicativo
        if (convertedValue === null) {
            return "N/A";
        }
        return this.format(convertedValue, targetCurrency);
    }

    /**
     * ALTERADO: Gera uma estrutura HTML completa com todos os valores de moeda pré-calculados.
     * Se uma conversão falhar, exibe "N/A" para essa moeda.
     */
    public generateCurrencyHTML(sflValue: number, prefix: string = ''): string {
        const currencies: Currency[] = ['Flower', 'USD', 'BRL'];

        const valueSpans = currencies.map(currency => {
            const convertedValue = this.convert(sflValue, currency);
            
            // Pega o HTML da bandeira e o texto formatado
            const { flagHtml } = CURRENCY_SYMBOLS[currency];
            const formattedText = (convertedValue !== null) 
                ? this.format(convertedValue, currency)
                : "N/A";
                
            const currencyClass = `currency-${currency.toLowerCase()}`;
            
            return `<span class="currency-value-display ${currencyClass}">${flagHtml}${prefix}${formattedText}</span>`;
        }).join('');

        return `<span class="currency-container">${valueSpans}</span>`;
    }

    /**
     * Retorna a moeda atualmente selecionada pelo usuário, lendo do localStorage.
     * O padrão é SFL.
     */
    public getCurrentCurrency(): Currency {
        return (localStorage.getItem(CURRENCY_STORAGE_KEY) as Currency) || 'Flower';
    }
}