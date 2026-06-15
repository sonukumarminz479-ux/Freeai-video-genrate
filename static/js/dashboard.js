// Dashboard specific functionality

let currentGenerationType = 'video';
const generatorConfig = {
    video: {
        title: 'Generate Video',
        description: 'Create stunning AI-generated videos from text prompts',
        defaultDuration: 30,
        maxDuration: 120
    },
    image: {
        title: 'Generate Image',
        description: 'Create beautiful, high-quality images from text descriptions',
        maxResolution: '4096x4096'
    },
    model3d: {
        title: 'Generate 3D Model',
        description: 'Create 3D models from text descriptions',
        exportFormats: ['obj', 'gltf', 'fbx']
    }
};

// Load user info
window.addEventListener('load', () => {
    // Get username from localStorage or fetch from server
    const username = localStorage.getItem('username') || 'User';
    document.getElementById('username').textContent = username;
    
    loadHistory();
});

// Handle generator type selection
document.querySelectorAll('.menu-item').forEach(item => {
    item.addEventListener('click', (e) => {
        document.querySelectorAll('.menu-item').forEach(m => m.classList.remove('active'));
        item.classList.add('active');
        
        currentGenerationType = item.dataset.type;
        updateGeneratorPanel();
    });
});

function updateGeneratorPanel() {
    const config = generatorConfig[currentGenerationType];
    document.getElementById('generatorTitle').textContent = config.title;
    document.getElementById('generatorDescription').textContent = config.description;
    
    // Reset form
    document.getElementById('generatorForm').reset();
}

// Handle form submission
document.getElementById('generatorForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const prompt = document.getElementById('prompt').value;
    
    if (!prompt.trim()) {
        showError('Please enter a prompt');
        return;
    }
    
    // Show progress
    document.getElementById('progressSection').style.display = 'block';
    
    try {
        const endpoint = `/api/generate/${currentGenerationType}`;
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Simulate progress
            simulateProgress();
            
            setTimeout(() => {
                document.getElementById('progressSection').style.display = 'none';
                document.getElementById('generatorForm').reset();
                loadHistory();
                showSuccess(`${currentGenerationType.charAt(0).toUpperCase() + currentGenerationType.slice(1)} generation started!`);
            }, 3000);
        } else {
            showError(data.error || 'Generation failed');
        }
    } catch (error) {
        showError('An error occurred. Please try again.');
    }
}
);

function simulateProgress() {
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 30;
        if (progress > 100) progress = 100;
        
        document.getElementById('progressFill').style.width = progress + '%';
        document.getElementById('progressPercentage').textContent = Math.round(progress) + '%';
        
        if (progress === 100) clearInterval(interval);
    }, 500);
}

async function loadHistory() {
    try {
        const response = await fetch('/api/history');
        const data = await response.json();
        
        const grid = document.getElementById('recentGrid');
        
        if (data.items.length === 0) {
            grid.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-sparkles"></i>
                    <p>No generations yet. Create your first one!</p>
                </div>
            `;
            return;
        }
        
        grid.innerHTML = data.items.map(item => `
            <div class="recent-item" data-id="${item.id}">
                <div class="recent-preview">
                    ${getPreviewIcon(item.type)}
                </div>
                <div class="recent-info">
                    <p class="recent-type">${item.type}</p>
                    <p class="recent-prompt">${item.prompt.substring(0, 50)}...</p>
                    <p class="recent-status">${item.status}</p>
                </div>
            </div>
        `).join('');
        
        // Update stats
        updateStats(data.items);
    } catch (error) {
        console.error('Failed to load history:', error);
    }
}

function updateStats(items) {
    let videoCount = 0, imageCount = 0, modelCount = 0;
    
    items.forEach(item => {
        if (item.type === 'video') videoCount++;
        else if (item.type === 'image') imageCount++;
        else if (item.type === 'model3d') modelCount++;
    });
    
    document.getElementById('videoCount').textContent = videoCount;
    document.getElementById('imageCount').textContent = imageCount;
    document.getElementById('modelCount').textContent = modelCount;
}

function getPreviewIcon(type) {
    const icons = {
        video: '<i class="fas fa-film"></i>',
        image: '<i class="fas fa-image"></i>',
        model3d: '<i class="fas fa-cube"></i>'
    };
    return icons[type] || icons.video;
}

function showSuccess(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'success';
    messageDiv.innerHTML = `<i class="fas fa-check-circle"></i><span>${message}</span>`;
    messageDiv.style.position = 'fixed';
    messageDiv.style.top = '20px';
    messageDiv.style.right = '20px';
    messageDiv.style.zIndex = '1000';
    document.body.appendChild(messageDiv);
    
    setTimeout(() => messageDiv.remove(), 3000);
}

function showError(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'error-message';
    messageDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i><span>${message}</span>`;
    messageDiv.style.position = 'fixed';
    messageDiv.style.top = '20px';
    messageDiv.style.right = '20px';
    messageDiv.style.zIndex = '1000';
    document.body.appendChild(messageDiv);
    
    setTimeout(() => messageDiv.remove(), 3000);
}

// Refresh history every 30 seconds if generation is in progress
setInterval(() => {
    const progressSection = document.getElementById('progressSection');
    if (progressSection && progressSection.style.display !== 'none') {
        loadHistory();
    }
}, 30000);
