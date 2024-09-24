import Alpine from 'alpinejs';

Alpine.data('noscroll', () => ({
    init() {
        if ('scrollRestoration' in history) {
            history.scrollRestoration = 'manual';
        }
    }
}))