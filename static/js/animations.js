// JS utilities to trigger animations (e.g. width expansions) once loaded

document.addEventListener("DOMContentLoaded", function () {
    // We use a MutationObserver because Streamlit violently destroys and redraws the DOM
    const observer = new MutationObserver((mutationsList, observer) => {

        // 1. Animate Progress Bars
        const progressBars = document.querySelectorAll('.breakdown-bar');
        progressBars.forEach(bar => {
            if (!bar.hasAttribute('data-animated')) {
                // Read the target width stored in a data attribute (we'll set this in Python)
                const targetWidth = bar.getAttribute('data-target-width');
                if (targetWidth) {
                    // Trigger a reflow
                    void bar.offsetWidth;
                    // Apply width to trigger the CSS transition
                    bar.style.width = targetWidth;
                    bar.setAttribute('data-animated', 'true');
                }
            }
        });

        // 2. Wrap Streamlit's main content elements with stagger classes
        // Attempting to inject fade-in to dynamically rendered layout blocks
        const verticalBlocks = document.querySelectorAll('[data-testid="stVerticalBlock"] > div');
        let delayIndex = 0;
        verticalBlocks.forEach((block) => {
            if (block.children.length > 0 && !block.hasAttribute('data-entrance-animated')) {
                if (block.querySelector('.glass-card') || block.querySelector('.dash-card') || block.querySelector('h1')) {
                    block.classList.add('animate-fade-in');
                    delayIndex = (delayIndex % 5) + 1;
                    block.classList.add(`delay-${delayIndex}`);
                    block.setAttribute('data-entrance-animated', 'true');
                }
            }
        });

        // 3. Stagger Forms and Tabs natively
        const stForms = document.querySelectorAll('[data-testid="stForm"], [data-testid="stTabs"]');
        stForms.forEach((el) => {
            if (!el.hasAttribute('data-entrance-animated')) {
                el.classList.add('animate-fade-in');
                delayIndex = (delayIndex % 5) + 1;
                el.classList.add(`delay-${delayIndex}`);
                el.setAttribute('data-entrance-animated', 'true');
            }
        });
    });

    observer.observe(document.body, { childList: true, subtree: true });
});
