display = document.getElementById('tool-display')

async function loadTool(hash) {
    const tool = hash.replace('#', '')
    display.innerHTML = `<iframe src='/tools/${tool}/${tool.content}'></iframe>`
}

window.addEventListener('hashchange', () => void loadTool(window.location.hash))
document.addEventListener('DOMContentLoaded', () => {
    if (!window.location.hash) {
        window.location.hash = 'home'
    }
    void loadTool(window.location.hash || '#home')
})