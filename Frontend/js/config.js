const CONFIG = {
    getApiUrl() {
        const stored = localStorage.getItem('api_base_url');
        if (stored) return stored.replace(/\/$/, ''); // Remove trailing slash if any
        
        // Auto-detect localhost
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return 'http://localhost:5002';
        }
        
        // Default Render server URL (Placeholder)
        return 'https://job-recommendation-system-ml-nlp.onrender.com';
    },
    
    setApiUrl(url) {
        if (!url) {
            localStorage.removeItem('api_base_url');
        } else {
            localStorage.setItem('api_base_url', url);
        }
    }
};

// Check API health
async function checkApiHealth() {
    const url = CONFIG.getApiUrl();
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 4000); // 4s timeout
        
        // We ping /api/health endpoint which responds fast and safely
        const response = await fetch(`${url}/api/health`, { 
            method: 'GET', 
            signal: controller.signal 
        });
        clearTimeout(timeoutId);
        // Any response code signifies the server is up and CORS is configured
        return response.status >= 200 && response.status < 500;
    } catch (e) {
        console.warn('API health check failed:', e);
        return false;
    }
}

