// AI Bug Reporter - Frontend JavaScript

const form = document.getElementById('bugForm');
const duplicatesSection = document.getElementById('duplicates');
const duplicatesList = document.getElementById('duplicatesList');
const resultSection = document.getElementById('result');
const attachmentsInput = document.getElementById('attachments');
const filePreview = document.getElementById('filePreview');
const squadSelect = document.getElementById('squad');
const bugFormFields = document.getElementById('bugFormFields');
const wipScreen = document.getElementById('wipScreen');

// Store selected files
let selectedFiles = [];

// Squad selection handler
squadSelect.addEventListener('change', function() {
    const selectedSquad = this.value;
    
    if (!selectedSquad) {
        bugFormFields.style.display = 'none';
        wipScreen.style.display = 'none';
        return;
    }
    
    if (selectedSquad === 'loyalty-2.0') {
        // Show the bug form for Loyalty 2.0
        bugFormFields.style.display = 'block';
        wipScreen.style.display = 'none';
    } else {
        // Show WIP screen for other squads
        bugFormFields.style.display = 'none';
        wipScreen.style.display = 'block';
        
        // Set squad name in WIP message
        const squadNames = {
            'loyalty-mission': 'Loyalty Mission Squad',
            'virality': 'Virality Squad',
            'rewards': 'Rewards Squad'
        };
        document.getElementById('wipSquadName').textContent = squadNames[selectedSquad];
    }
});

// Function to reset squad selection
function resetSquadSelection() {
    squadSelect.value = '';
    bugFormFields.style.display = 'none';
    wipScreen.style.display = 'none';
    squadSelect.focus();
}

// Get form data
function getFormData() {
    return {
        title: document.getElementById('title').value.trim(),
        description: document.getElementById('description').value.trim(),
        steps_to_reproduce: document.getElementById('steps_to_reproduce').value.trim(),
        expected_behavior: document.getElementById('expected_behavior').value.trim(),
        actual_behavior: document.getElementById('actual_behavior').value.trim(),
        environment: document.getElementById('environment').value.trim() || 'Not specified',
        priority: document.getElementById('priority').value
    };
}

// Show loading state on button
function setButtonLoading(button, loading) {
    if (loading) {
        button.classList.add('loading');
        button.disabled = true;
    } else {
        button.classList.remove('loading');
        button.disabled = false;
    }
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    return `${Math.floor(diffDays / 30)} months ago`;
}

// Display duplicates
function displayDuplicates(duplicates, warningMessage) {
    if (!duplicates || duplicates.length === 0) {
        duplicatesSection.style.display = 'none';
        return;
    }

    // Update the warning message based on severity
    const heading = duplicatesSection.querySelector('h2');
    const intro = duplicatesSection.querySelector('.duplicates-intro');
    
    // Add count and make collapsible if more than 1
    const count = duplicates.length;
    const isCollapsible = count > 1;
    
    if (duplicates[0].similarity >= 80) {
        heading.innerHTML = `🚨 Very Similar Bugs Found! (${count})${isCollapsible ? ' <span class="toggle-icon">▼</span>' : ''}`;
        intro.innerHTML = 'These bugs are very similar to yours. <strong>Please review them carefully before creating a new ticket:</strong>';
        duplicatesSection.style.backgroundColor = '#fee2e2';
        duplicatesSection.style.borderColor = '#ef4444';
    } else if (duplicates[0].similarity >= 60) {
        heading.innerHTML = `⚠️ Similar Bugs Found (${count})${isCollapsible ? ' <span class="toggle-icon">▼</span>' : ''}`;
        intro.innerHTML = 'We found bugs that might be related to yours:';
        duplicatesSection.style.backgroundColor = '#fef3c7';
        duplicatesSection.style.borderColor = '#f59e0b';
    } else {
        heading.innerHTML = `ℹ️ Possibly Related Bugs (${count})${isCollapsible ? ' <span class="toggle-icon">▼</span>' : ''}`;
        intro.innerHTML = 'These bugs might be related (partial match):';
        duplicatesSection.style.backgroundColor = '#dbeafe';
        duplicatesSection.style.borderColor = '#3b82f6';
    }
    
    // Make heading clickable if collapsible
    if (isCollapsible) {
        heading.style.cursor = 'pointer';
        heading.onclick = toggleDuplicatesList;
    } else {
        heading.style.cursor = 'default';
        heading.onclick = null;
    }

    duplicatesList.innerHTML = '';
    
    duplicates.forEach(duplicate => {
        const card = document.createElement('div');
        card.className = 'duplicate-card';
        
        let similarityClass = '';
        let matchLabel = '';
        
        if (duplicate.similarity >= 80) {
            similarityClass = 'very-high';
            matchLabel = 'Very High Match';
        } else if (duplicate.similarity >= 70) {
            similarityClass = 'high';
            matchLabel = 'High Match';
        } else if (duplicate.similarity >= 50) {
            similarityClass = 'medium';
            matchLabel = 'Medium Match';
        } else {
            similarityClass = 'low';
            matchLabel = 'Partial Match';
        }
        
        card.innerHTML = `
            <div class="duplicate-header">
                <a href="${duplicate.url}" target="_blank" class="duplicate-key">${duplicate.key}</a>
                <span class="duplicate-similarity ${similarityClass}" title="${matchLabel}">
                    ${Math.round(duplicate.similarity)}% match
                </span>
            </div>
            <div class="duplicate-summary">${escapeHtml(duplicate.summary)}</div>
            <div class="duplicate-meta">
                <span>Status: ${duplicate.status}</span>
                <span>Created: ${formatDate(duplicate.created)}</span>
            </div>
        `;
        
        duplicatesList.appendChild(card);
    });
    
    // Start collapsed if more than 1 bug
    if (isCollapsible) {
        duplicatesList.classList.add('collapsed');
        intro.style.display = 'none';
        duplicatesSection.querySelector('.duplicates-actions').style.display = 'none';
    } else {
        duplicatesList.classList.remove('collapsed');
        intro.style.display = 'block';
        duplicatesSection.querySelector('.duplicates-actions').style.display = 'block';
    }
    
    duplicatesSection.style.display = 'block';
    duplicatesSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Toggle duplicates list
function toggleDuplicatesList() {
    const list = duplicatesList;
    const intro = duplicatesSection.querySelector('.duplicates-intro');
    const actions = duplicatesSection.querySelector('.duplicates-actions');
    const toggleIcon = duplicatesSection.querySelector('.toggle-icon');
    
    if (list.classList.contains('collapsed')) {
        // Expand
        list.classList.remove('collapsed');
        intro.style.display = 'block';
        actions.style.display = 'block';
        if (toggleIcon) toggleIcon.textContent = '▼';
    } else {
        // Collapse
        list.classList.add('collapsed');
        intro.style.display = 'none';
        actions.style.display = 'none';
        if (toggleIcon) toggleIcon.textContent = '▶';
    }
}

// Display result message
function displayResult(success, message, jiraUrl = null) {
    resultSection.className = `result-section ${success ? 'success' : 'error'}`;
    
    let content = `<h2>${success ? '✅ Success!' : '❌ Error'}</h2><p>${escapeHtml(message)}</p>`;
    
    if (success && jiraUrl) {
        content += `<a href="${jiraUrl}" target="_blank" class="jira-link">View in JIRA →</a>`;
    }
    
    resultSection.innerHTML = content;
    resultSection.style.display = 'block';
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Validate form
function validateForm(data) {
    const required = ['title', 'description', 'steps_to_reproduce', 'expected_behavior', 'actual_behavior'];
    
    for (const field of required) {
        if (!data[field]) {
            const fieldName = field.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            throw new Error(`${fieldName} is required`);
        }
    }
    
    return true;
}

// Create bug report
async function createBugReport(event) {
    event.preventDefault();
    
    try {
        const data = getFormData();
        validateForm(data);
        
        const submitBtn = event.submitter || form.querySelector('button[type="submit"]');
        setButtonLoading(submitBtn, true);
        resultSection.style.display = 'none';
        
        // Use FormData if there are attachments
        let requestBody;
        let headers = {};
        
        if (selectedFiles.length > 0) {
            const formData = new FormData();
            
            // Add all form fields
            Object.keys(data).forEach(key => {
                formData.append(key, data[key]);
            });
            
            // Add files
            selectedFiles.forEach(file => {
                formData.append('attachments', file);
            });
            
            requestBody = formData;
            // Don't set Content-Type header - browser will set it with boundary
        } else {
            requestBody = JSON.stringify(data);
            headers['Content-Type'] = 'application/json';
        }
        
        const response = await fetch('/api/create-bug', {
            method: 'POST',
            headers: headers,
            body: requestBody
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayResult(true, `Bug ${result.key} created successfully!`, result.url);
            form.reset();
            selectedFiles = [];
            displayFilePreview();
            duplicatesSection.style.display = 'none';
        } else {
            throw new Error(result.error || 'Unknown error');
        }
        
    } catch (error) {
        console.error('Error creating bug:', error);
        displayResult(false, `Failed to create bug: ${error.message}`, null);
    } finally {
        const submitBtn = event.submitter || form.querySelector('button[type="submit"]');
        setButtonLoading(submitBtn, false);
    }
}

// Event listeners
form.addEventListener('submit', createBugReport);
attachmentsInput.addEventListener('change', handleFileSelection);

// Handle file selection
function handleFileSelection(event) {
    const files = Array.from(event.target.files);
    
    // Validate file size (50MB max per file)
    const maxSize = 50 * 1024 * 1024; // 50MB in bytes
    const validFiles = files.filter(file => {
        if (file.size > maxSize) {
            alert(`File "${file.name}" is too large. Maximum size is 50MB.`);
            return false;
        }
        return true;
    });
    
    // Add to selected files
    selectedFiles = [...selectedFiles, ...validFiles];
    
    // Update preview
    displayFilePreview();
    
    // Clear input so same file can be selected again
    event.target.value = '';
}

// Display file preview
function displayFilePreview() {
    filePreview.innerHTML = '';
    
    selectedFiles.forEach((file, index) => {
        const previewItem = document.createElement('div');
        previewItem.className = 'file-preview-item';
        
        // Create remove button
        const removeBtn = document.createElement('button');
        removeBtn.className = 'remove-file';
        removeBtn.innerHTML = '×';
        removeBtn.type = 'button';
        removeBtn.onclick = () => removeFile(index);
        
        // Create file name label
        const fileName = document.createElement('div');
        fileName.className = 'file-name';
        fileName.textContent = file.name;
        
        // Preview based on file type
        if (file.type.startsWith('image/')) {
            const img = document.createElement('img');
            img.src = URL.createObjectURL(file);
            img.onload = () => URL.revokeObjectURL(img.src);
            previewItem.appendChild(img);
        } else if (file.type.startsWith('video/')) {
            const video = document.createElement('video');
            video.src = URL.createObjectURL(file);
            video.controls = false;
            video.muted = true;
            video.onloadedmetadata = () => URL.revokeObjectURL(video.src);
            previewItem.appendChild(video);
            
            // Add play icon overlay
            const playIcon = document.createElement('div');
            playIcon.style.position = 'absolute';
            playIcon.style.top = '50%';
            playIcon.style.left = '50%';
            playIcon.style.transform = 'translate(-50%, -50%)';
            playIcon.style.fontSize = '2rem';
            playIcon.innerHTML = '▶️';
            previewItem.appendChild(playIcon);
        } else {
            const icon = document.createElement('div');
            icon.className = 'file-icon';
            icon.innerHTML = '📎';
            previewItem.appendChild(icon);
        }
        
        previewItem.appendChild(removeBtn);
        previewItem.appendChild(fileName);
        filePreview.appendChild(previewItem);
    });
}

// Remove file from selection
function removeFile(index) {
    selectedFiles.splice(index, 1);
    displayFilePreview();
}

// Auto-check duplicates when title is entered (debounced)
let titleTimeout;
document.getElementById('title').addEventListener('input', (e) => {
    clearTimeout(titleTimeout);
    const title = e.target.value.trim();
    
    // Clear previous results if title is too short
    if (title.length < 3) {
        duplicatesSection.style.display = 'none';
        resultSection.style.display = 'none';
        return;
    }
    
    // Auto-check after user stops typing for 1 second
    if (title.length >= 3) {
        titleTimeout = setTimeout(() => {
            autoCheckDuplicates(title);
        }, 1000); // 1 second delay after user stops typing
    }
});

// Auto-check function (doesn't require description)
async function autoCheckDuplicates(title) {
    try {
        resultSection.style.display = 'none';
        
        const response = await fetch('/api/check-duplicates', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: title,
                description: ''
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.has_duplicates) {
            // Show duplicates section only
            displayDuplicates(result.duplicates, result.warning_message);
        } else {
            // Hide duplicates if none found
            duplicatesSection.style.display = 'none';
        }
        
    } catch (error) {
        console.error('Error auto-checking duplicates:', error);
    }
}

// Initialize
console.log('AI Bug Reporter initialized');

// Theme management
function initTheme() {
    // Check for saved theme preference or default to light mode
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeButton(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeButton(newTheme);
}

function updateThemeButton(theme) {
    const icon = document.getElementById('themeIcon');
    const text = document.getElementById('themeText');
    
    if (theme === 'dark') {
        icon.textContent = '☀️';
        text.textContent = 'Light Mode';
    } else {
        icon.textContent = '🌙';
        text.textContent = 'Dark Mode';
    }
}

// Make toggleTheme available globally
window.toggleTheme = toggleTheme;

// Initialize theme on page load
initTheme();

// Tab switching
function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    if (tabName === 'report') {
        document.getElementById('reportTab').classList.add('active');
        document.querySelector('.tab-button:nth-child(1)').classList.add('active');
    } else if (tabName === 'dashboard') {
        document.getElementById('dashboardTab').classList.add('active');
        document.querySelector('.tab-button:nth-child(2)').classList.add('active');
        
        // Load dashboard if not already loaded or if stale
        const lastUpdate = window.dashboardLastUpdate || 0;
        const now = Date.now();
        if (now - lastUpdate > 60000) { // Refresh if older than 1 minute
            loadDashboardStats();
        }
    }
}

// Make switchTab available globally
window.switchTab = switchTab;

// Load dashboard stats on page load (but don't show it)
loadDashboardStats();

// Auto-refresh dashboard every 15 minutes
let dashboardRefreshInterval;

function startDashboardAutoRefresh() {
    // Clear any existing interval
    if (dashboardRefreshInterval) {
        clearInterval(dashboardRefreshInterval);
    }
    
    // Set up new interval (15 minutes = 900000ms)
    dashboardRefreshInterval = setInterval(() => {
        console.log('Auto-refreshing dashboard...');
        loadDashboardStats();
    }, 900000); // 15 minutes
}

// Start auto-refresh
startDashboardAutoRefresh();

async function loadDashboardStats() {
    try {
        const response = await fetch('/api/epic-stats');
        if (!response.ok) throw new Error('Failed to load stats');
        
        const stats = await response.json();
        displayDashboard(stats);
        
        // Update last refresh time
        window.dashboardLastUpdate = Date.now();
        updateLastRefreshTime();
    } catch (error) {
        console.error('Error loading dashboard:', error);
        document.getElementById('dashboardContent').innerHTML = `
            <p style="color: var(--danger-color);">Failed to load statistics</p>
        `;
    }
}

function updateLastRefreshTime() {
    const lastUpdated = document.getElementById('lastUpdated');
    if (lastUpdated) {
        const now = new Date();
        lastUpdated.textContent = `Last updated: ${now.toLocaleTimeString()} • Auto-refresh: Every 15 minutes`;
    }
}

function displayDashboard(stats) {
    const content = document.getElementById('dashboardContent');
    const jiraBaseUrl = 'https://hellofresh.atlassian.net';
    
    // Helper to create Jira search URL
    const createJiraUrl = (jql) => {
        return `${jiraBaseUrl}/issues/?jql=${encodeURIComponent(jql)}`;
    };
    
    // Get all unique statuses
    const allStatuses = Object.keys(stats.by_status).sort();
    const priorityOrder = ['Critical', 'Urgent', 'High', 'Normal', 'Medium', 'Low', 'None'];
    const priorities = priorityOrder.filter(p => stats.by_priority[p]);
    
    // Calculate insights
    const urgentOpen = Object.entries(stats.priority_status_matrix['Urgent'] || {})
        .filter(([status]) => stats.by_status[status] && status !== 'Closed' && status !== 'Resolved')
        .reduce((sum, [, count]) => sum + count, 0);
    
    const highOpen = Object.entries(stats.priority_status_matrix['High'] || {})
        .filter(([status]) => stats.by_status[status] && status !== 'Closed' && status !== 'Resolved')
        .reduce((sum, [, count]) => sum + count, 0);
    
    content.innerHTML = `
        <button class="refresh-button" onclick="loadDashboardStats(); updateLastRefreshTime();">🔄 Refresh</button>
        
        <div class="stats-grid">
            <div class="stat-card clickable" onclick="window.open('${createJiraUrl('parent = REW-323 AND type = Bug')}', '_blank')">
                <h3>📊 Total Bugs</h3>
                <div class="stat-value">${stats.total_count}</div>
                <div class="stat-label">In Epic REW-323</div>
            </div>
            
            <div class="stat-card clickable" onclick="window.open('${createJiraUrl('parent = REW-323 AND type = Bug AND statusCategory != Done')}', '_blank')">
                <h3>⏳ Open</h3>
                <div class="stat-value" style="color: #f59e0b;">${stats.open_count}</div>
                <div class="stat-label">${Math.round((stats.open_count / stats.total_count) * 100)}% of total</div>
            </div>
            
            <div class="stat-card clickable" onclick="window.open('${createJiraUrl('parent = REW-323 AND type = Bug AND statusCategory = Done')}', '_blank')">
                <h3>✅ Resolved</h3>
                <div class="stat-value" style="color: #10b981;">${stats.closed_count}</div>
                <div class="stat-label">${Math.round((stats.closed_count / stats.total_count) * 100)}% of total</div>
            </div>
            
            <div class="stat-card clickable" onclick="window.open('${createJiraUrl('parent = REW-323 AND type = Bug AND resolution != Unresolved')}', '_blank')">
                <h3>⏱️ Avg Resolution</h3>
                <div class="stat-value" style="color: #8b5cf6;">${stats.avg_resolution_days}</div>
                <div class="stat-label">days to resolve</div>
            </div>
        </div>
        
        <div class="breakdown-section">
            <h3>🎯 Priority × Status Matrix</h3>
            <div class="insights-grid">
                <div class="insight-card" style="border-left-color: #dc2626;">
                    <div class="insight-value" style="color: #dc2626;">${urgentOpen + highOpen}</div>
                    <div class="insight-label">Critical/High Priority Open</div>
                </div>
                <div class="insight-card" style="border-left-color: #10b981;">
                    <div class="insight-value" style="color: #10b981;">${Math.round((stats.closed_count / stats.total_count) * 100)}%</div>
                    <div class="insight-label">Resolution Rate</div>
                </div>
                <div class="insight-card" style="border-left-color: #8b5cf6;">
                    <div class="insight-value" style="color: #8b5cf6;">${stats.avg_resolution_days}</div>
                    <div class="insight-label">Avg Days to Resolve</div>
                </div>
            </div>
            
            <div class="matrix-container">
                <table class="priority-status-matrix">
                    <thead>
                        <tr>
                            <th>Priority \ Status</th>
                            ${allStatuses.map(status => `<th>${status}</th>`).join('')}
                            <th>Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${priorities.map(priority => {
                            const rowData = stats.priority_status_matrix[priority] || {};
                            const rowTotal = Object.values(rowData).reduce((sum, val) => sum + val, 0);
                            
                            return `
                                <tr>
                                    <th>${priority}</th>
                                    ${allStatuses.map(status => {
                                        const count = rowData[status] || 0;
                                        let cellClass = 'matrix-cell';
                                        
                                        if (count === 0) {
                                            cellClass += ' zero';
                                        } else if (count <= 2) {
                                            cellClass += ' low';
                                        } else if (count <= 5) {
                                            cellClass += ' medium';
                                        } else if (count <= 10) {
                                            cellClass += ' high';
                                        } else {
                                            cellClass += ' critical';
                                        }
                                        
                                        const jql = `parent = REW-323 AND type = Bug AND priority = "${priority}" AND status = "${status}"`;
                                        
                                        return `
                                            <td class="${cellClass}" 
                                                onclick="window.open('${createJiraUrl(jql)}', '_blank')"
                                                title="${count} ${priority} bugs in ${status} status">
                                                ${count || '-'}
                                            </td>
                                        `;
                                    }).join('')}
                                    <td class="matrix-cell" style="font-weight: 700; background: var(--background);"
                                        onclick="window.open('${createJiraUrl(`parent = REW-323 AND type = Bug AND priority = "${priority}"`)}', '_blank')">
                                        ${rowTotal}
                                    </td>
                                </tr>
                            `;
                        }).join('')}
                        <tr>
                            <th>Total</th>
                            ${allStatuses.map(status => {
                                const total = stats.by_status[status] || 0;
                                return `
                                    <td class="matrix-cell" style="font-weight: 700; background: var(--background);"
                                        onclick="window.open('${createJiraUrl(`parent = REW-323 AND type = Bug AND status = "${status}"`)}', '_blank')">
                                        ${total}
                                    </td>
                                `;
                            }).join('')}
                            <td style="font-weight: 700; background: linear-gradient(135deg, var(--primary-color), #764ba2); color: white;">
                                ${stats.total_count}
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="breakdown-section" style="margin-top: 2rem;">
            <h3>📈 Bug Creation Trend (Last 10 Days)</h3>
            <div class="chart-container">
                <canvas id="creationTrendChart"></canvas>
            </div>
        </div>
        
        <div class="stats-grid" style="margin-top: 2rem;">
            <div class="stat-card">
                <h3>By Platform</h3>
                <div class="platform-tags">
                    ${Object.entries(stats.by_platform)
                        .sort((a, b) => b[1] - a[1])
                        .map(([platform, count]) => {
                            let label = platform;
                            let searchTerm = '';
                            
                            if (platform.includes('iOS') && platform.includes('Android')) {
                                label = 'iOS + Android';
                                searchTerm = 'iOS Android';
                            } else if (platform.includes('iOS')) {
                                label = 'iOS';
                                searchTerm = 'iOS';
                            } else if (platform.includes('Android')) {
                                label = 'Android';
                                searchTerm = 'Android';
                            } else if (platform.includes('Web')) {
                                label = 'Web';
                                searchTerm = 'web OR website OR browser';
                            } else {
                                label = 'Unknown';
                                return `
                                    <div class="platform-tag" onclick="window.open('${createJiraUrl('parent = REW-323 AND type = Bug')}', '_blank')">
                                        <span>${label}</span>
                                        <span class="count">${count}</span>
                                    </div>
                                `;
                            }
                            
                            return `
                                <div class="platform-tag" onclick="window.open('${createJiraUrl(`parent = REW-323 AND type = Bug AND (summary ~ "${searchTerm}" OR description ~ "${searchTerm}")`)}', '_blank')">
                                    <span>${label}</span>
                                    <span class="count">${count}</span>
                                </div>
                            `;
                        }).join('')}
                </div>
            </div>
        </div>
    `;
    
    // Render creation trend chart
    renderCreationTrendChart(stats.creation_trend);
}

// Chart rendering
let creationTrendChartInstance = null;

function renderCreationTrendChart(creationTrend) {
    const canvas = document.getElementById('creationTrendChart');
    if (!canvas) return;
    
    // Destroy previous chart instance if exists
    if (creationTrendChartInstance) {
        creationTrendChartInstance.destroy();
    }
    
    const ctx = canvas.getContext('2d');
    
    // Generate last 10 days
    const last10Days = [];
    const today = new Date();
    for (let i = 9; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(today.getDate() - i);
        last10Days.push(date.toISOString().split('T')[0]); // Format: YYYY-MM-DD
    }
    
    // Format labels to be more readable (e.g., "Jan 15" or "Mon 15")
    const labels = last10Days.map(dateStr => {
        const date = new Date(dateStr + 'T00:00:00');
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });
    
    const data = last10Days.map(day => creationTrend[day] || 0);
    
    // Detect theme
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const textColor = isDark ? '#e2e8f0' : '#1e293b';
    const gridColor = isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';
    
    creationTrendChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Bugs Created',
                data: data,
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 5,
                pointHoverRadius: 7,
                pointBackgroundColor: '#667eea',
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        color: textColor,
                        font: {
                            size: 13,
                            weight: '600'
                        },
                        padding: 15
                    }
                },
                tooltip: {
                    backgroundColor: isDark ? 'rgba(30, 41, 59, 0.95)' : 'rgba(255, 255, 255, 0.95)',
                    titleColor: textColor,
                    bodyColor: textColor,
                    borderColor: gridColor,
                    borderWidth: 1,
                    padding: 12,
                    displayColors: true,
                    callbacks: {
                        label: function(context) {
                            return `Bugs Created: ${context.parsed.y}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: textColor,
                        font: {
                            size: 12
                        },
                        stepSize: 1
                    },
                    grid: {
                        color: gridColor,
                        drawBorder: false
                    }
                },
                x: {
                    ticks: {
                        color: textColor,
                        font: {
                            size: 11
                        },
                        maxRotation: 45,
                        minRotation: 45
                    },
                    grid: {
                        color: gridColor,
                        drawBorder: false
                    }
                }
            }
        }
    });
}
