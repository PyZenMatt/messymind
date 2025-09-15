/*! Theme Toggle - extracted for deferred loading */

// NOTE: Copy of `_includes/theme-toggle.js` to be loaded via <script src="/assets/js/theme-toggle.js" defer>

const themeManager = {
    init() {
        console.debug('themeManager: init');
        this.applyTheme();
        this.bindEvents();
    },
    applyTheme() {
        const saved = localStorage.getItem('theme');
        let theme;
        if (saved === 'dark' || saved === 'light') {
            theme = saved;
        } else if (saved === 'auto') {
            theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        } else {
            theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        }
        this.setTheme(theme, false);
    },
    setTheme(theme, save = true) {
        const html = document.documentElement;
        if (theme === 'dark') {
            html.classList.add('dark');
        } else {
            html.classList.remove('dark');
        }
        this.updateIcon(theme);
        if (save) localStorage.setItem('theme', theme);
    },
    updateIcon(theme) {
        const icon = document.getElementById('theme-icon');
        if (icon) {
            icon.textContent = theme === 'dark' ? '☀️' : '🌙';
        }
    },
    toggleTheme() {
        const isDark = document.documentElement.classList.contains('dark');
        const newTheme = isDark ? 'light' : 'dark';
        console.debug('themeManager: toggleTheme ->', newTheme);
        this.setTheme(newTheme, true);
    },
    bindEvents() {
        const toggle = document.getElementById('theme-toggle');
        if (toggle) {
            if (!toggle.dataset.themeAttached) {
                toggle.addEventListener('click', (e) => {
                // shift+click = reset to 'auto' (follow system)
                if (e.shiftKey) {
                    try { localStorage.setItem('theme', 'auto'); } catch (err){}
                    this.applyTheme();
                    console.debug('themeManager: reset to auto via shift+click');
                    return;
                }
                this.toggleTheme();
                });
                toggle.dataset.themeAttached = '1';
            }
        }
        const mq = window.matchMedia('(prefers-color-scheme: dark)');
        if (mq && typeof mq.addEventListener === 'function') {
            mq.addEventListener('change', (e) => {
                const saved = localStorage.getItem('theme');
                if (saved === null || saved === 'auto') {
                    this.setTheme(e.matches ? 'dark' : 'light', false);
                    console.debug('themeManager: system preference changed ->', e.matches ? 'dark' : 'light');
                }
            });
        }
    }
};

// Expose a small API for optional external attach
window.themeToggle = {
    attach: function(el){
        if (!el) return;
        if (el.dataset && el.dataset.themeAttached) return;
        el.addEventListener('click', function(e){
            if (e.shiftKey) {
                try { localStorage.setItem('theme','auto'); } catch(err){}
                themeManager.applyTheme();
                console.debug('themeToggle.attach: reset to auto via shift+click');
                return;
            }
            themeManager.toggleTheme();
        });
        try { el.dataset.themeAttached = '1'; } catch(e){}
    },
    init: function(){ themeManager.init(); }
};

// Initialize now
themeManager.init();
