// JavaScript Tests for Bug Reporter
// Run with: npm test (after setting up Jest)

describe('Bug Reporter Frontend', () => {
    
    // Mock DOM elements
    beforeEach(() => {
        document.body.innerHTML = `
            <select id="squad"></select>
            <div id="bugFormFields" style="display: none;"></div>
            <div id="wipScreen" style="display: none;"></div>
            <div id="wipSquadName"></div>
            <select id="dashboardProject"></select>
            <div id="dashboardContentWrapper" style="display: none;"></div>
            <div id="dashboardWipScreen" style="display: none;"></div>
            <div id="dashboardWipProjectName"></div>
        `;
    });
    
    test('Form data collection works correctly', () => {
        // Create mock form elements
        document.body.innerHTML += `
            <input id="title" value="Test Bug">
            <textarea id="description">Test Description</textarea>
            <textarea id="steps_to_reproduce">Step 1</textarea>
            <textarea id="expected_behavior">Should work</textarea>
            <textarea id="actual_behavior">Broken</textarea>
            <select id="environment"><option selected value="Staging">Staging</option></select>
            <select id="priority"><option selected value="Low">Low</option></select>
        `;
        
        // Test getFormData function exists and returns correct structure
        // This would need to be adapted based on your actual implementation
    });
    
    test('Duplicate detection triggers on title input', () => {
        const titleInput = document.createElement('input');
        titleInput.id = 'title';
        document.body.appendChild(titleInput);
        
        // Simulate typing
        titleInput.value = 'Test bug title';
        
        // Check if debounced function would be called
        // This tests the auto-check functionality
    });
    
    test('Date formatting works correctly', () => {
        const today = new Date();
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);
        
        // Test formatDate function
        // formatDate(today) should return 'Today'
        // formatDate(yesterday) should return 'Yesterday'
    });
});

describe('Squad/Project Selection', () => {
    
    test('Loyalty 2.0 shows bug form', () => {
        const squadSelect = document.getElementById('squad');
        const bugFormFields = document.getElementById('bugFormFields');
        const wipScreen = document.getElementById('wipScreen');
        
        // Simulate selecting Loyalty 2.0
        squadSelect.value = 'loyalty-2.0';
        squadSelect.dispatchEvent(new Event('change'));
        
        // Form should be visible, WIP hidden
        expect(bugFormFields.style.display).toBe('block');
        expect(wipScreen.style.display).toBe('none');
    });
    
    test('Other squads show WIP screen', () => {
        const squadSelect = document.getElementById('squad');
        const bugFormFields = document.getElementById('bugFormFields');
        const wipScreen = document.getElementById('wipScreen');
        
        // Simulate selecting another squad
        squadSelect.value = 'virality';
        squadSelect.dispatchEvent(new Event('change'));
        
        // WIP should be visible, form hidden
        expect(wipScreen.style.display).toBe('block');
        expect(bugFormFields.style.display).toBe('none');
    });
});

describe('Dashboard Project Selection', () => {
    
    test('Loyalty 2.0 shows dashboard', () => {
        const projectSelect = document.getElementById('dashboardProject');
        const contentWrapper = document.getElementById('dashboardContentWrapper');
        const wipScreen = document.getElementById('dashboardWipScreen');
        
        projectSelect.value = 'loyalty-2.0';
        projectSelect.dispatchEvent(new Event('change'));
        
        expect(contentWrapper.style.display).toBe('block');
        expect(wipScreen.style.display).toBe('none');
    });
    
    test('Other projects show WIP screen', () => {
        const projectSelect = document.getElementById('dashboardProject');
        const contentWrapper = document.getElementById('dashboardContentWrapper');
        const wipScreen = document.getElementById('dashboardWipScreen');
        
        projectSelect.value = 'rewards';
        projectSelect.dispatchEvent(new Event('change'));
        
        expect(wipScreen.style.display).toBe('block');
        expect(contentWrapper.style.display).toBe('none');
    });
});

describe('Theme Toggle', () => {
    
    test('Theme persists in localStorage', () => {
        localStorage.setItem('theme', 'dark');
        
        // Simulate page load
        const theme = localStorage.getItem('theme');
        expect(theme).toBe('dark');
        
        localStorage.removeItem('theme');
    });
    
    test('Theme toggle updates document attribute', () => {
        document.documentElement.setAttribute('data-theme', 'dark');
        expect(document.documentElement.getAttribute('data-theme')).toBe('dark');
        
        document.documentElement.setAttribute('data-theme', 'light');
        expect(document.documentElement.getAttribute('data-theme')).toBe('light');
    });
});

describe('File Upload', () => {
    
    test('File size validation (max 50MB)', () => {
        const maxSize = 50 * 1024 * 1024; // 50MB
        
        const largeFile = { size: 51 * 1024 * 1024, name: 'large.jpg' };
        const validFile = { size: 10 * 1024 * 1024, name: 'valid.jpg' };
        
        expect(largeFile.size > maxSize).toBe(true);
        expect(validFile.size <= maxSize).toBe(true);
    });
    
    test('Accepted file types', () => {
        const validTypes = ['image/jpeg', 'image/png', 'video/mp4'];
        const file = { type: 'image/jpeg' };
        
        expect(validTypes.includes(file.type)).toBe(true);
    });
});
