/*! Theme Toggle - extracted for deferred loading */

// NOTE: Copy of `_includes/theme-toggle.js` to be loaded via <script src="/assets/js/theme-toggle.js" defer>

const themeManager = {
    init() {
        this.applyTheme();
        this.bindEvents();
    },
    applyTheme() {
        const saved = localStorage.getItem('theme');
        let theme;
        if (saved === 'dark' || saved === 'light') {
            theme = saved;
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
        this.setTheme(newTheme, true);
    },
    bindEvents() {
        const toggle = document.getElementById('theme-toggle');
        if (toggle) {
            toggle.addEventListener('click', () => this.toggleTheme());
        }
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('theme')) {
                this.setTheme(e.matches ? 'dark' : 'light', false);
            }
        });
    }
};

// Expose a small API for optional external attach
window.themeToggle = {
    attach: function(el){ if (!el) return; el.addEventListener('click', function(){ themeManager.toggleTheme(); }); },
    init: function(){ themeManager.init(); }
};

// Initialize now
themeManager.init();
