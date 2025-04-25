/**
 * NurAI - Main JavaScript file
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize all popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Handle range input display value
    const rangeInputs = document.querySelectorAll('input[type="range"]');
    rangeInputs.forEach(function(input) {
        const valueDisplay = document.getElementById(input.id + '-value');
        if (valueDisplay) {
            // Set initial value
            valueDisplay.textContent = input.value;
            
            // Update value on change
            input.addEventListener('input', function() {
                valueDisplay.textContent = input.value;
            });
        }
    });
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Confirm dialog for delete actions
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                event.preventDefault();
            }
        });
    });
    
    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Date picker initialization for all date inputs
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(function(input) {
        // Set default value to today if empty
        if (!input.value && !input.hasAttribute('data-no-default')) {
            const today = new Date();
            const yyyy = today.getFullYear();
            const mm = String(today.getMonth() + 1).padStart(2, '0');
            const dd = String(today.getDate()).padStart(2, '0');
            input.value = `${yyyy}-${mm}-${dd}`;
        }
    });
    
    // Dynamic mood emoji display
    const moodRatingInputs = document.querySelectorAll('input[name="mood_rating"]');
    const moodEmojiDisplay = document.getElementById('mood-emoji');
    
    if (moodRatingInputs.length > 0 && moodEmojiDisplay) {
        moodRatingInputs.forEach(function(input) {
            input.addEventListener('input', updateMoodEmoji);
        });
        
        // Initial update
        updateMoodEmoji();
    }
    
    function updateMoodEmoji() {
        const moodValue = document.querySelector('input[name="mood_rating"]').value;
        let emoji = '';
        
        if (moodValue >= 9) {
            emoji = '😁'; // Excellent
        } else if (moodValue >= 7) {
            emoji = '😊'; // Good
        } else if (moodValue >= 5) {
            emoji = '😐'; // Neutral
        } else if (moodValue >= 3) {
            emoji = '😔'; // Sad
        } else {
            emoji = '😢'; // Very sad
        }
        
        moodEmojiDisplay.textContent = emoji;
    }
    
    // Print button functionality
    const printButtons = document.querySelectorAll('.btn-print');
    printButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            window.print();
        });
    });
    
    // Export data to CSV
    const exportButtons = document.querySelectorAll('.btn-export');
    exportButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const tableId = button.getAttribute('data-table');
            const table = document.getElementById(tableId);
            
            if (table) {
                exportTableToCSV(table, 'nurai_export.csv');
            }
        });
    });
    
    function exportTableToCSV(table, filename) {
        const rows = table.querySelectorAll('tr');
        const csv = [];
        
        for (let i = 0; i < rows.length; i++) {
            const row = [], cols = rows[i].querySelectorAll('td, th');
            
            for (let j = 0; j < cols.length; j++) {
                // Clean the text content (remove line breaks, quotes)
                let data = cols[j].textContent.replace(/(\r\n|\n|\r)/gm, '').replace(/(\s\s)/gm, ' ').trim();
                data = data.replace(/"/g, '""'); // Escape double quotes
                row.push('"' + data + '"');
            }
            
            csv.push(row.join(','));
        }
        
        const csvString = csv.join('\n');
        const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
        
        // Create download link
        if (navigator.msSaveBlob) { // IE 10+
            navigator.msSaveBlob(blob, filename);
        } else {
            const link = document.createElement('a');
            if (link.download !== undefined) {
                const url = URL.createObjectURL(blob);
                link.setAttribute('href', url);
                link.setAttribute('download', filename);
                link.style.visibility = 'hidden';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }
        }
    }
    
    // Form field dependencies
    const conditionalFields = document.querySelectorAll('[data-depends-on]');
    conditionalFields.forEach(function(field) {
        const dependsOn = field.getAttribute('data-depends-on');
        const dependsValue = field.getAttribute('data-depends-value');
        const dependentField = document.getElementById(dependsOn);
        
        if (dependentField) {
            // Initial check
            toggleFieldVisibility(dependentField, field, dependsValue);
            
            // Add event listener
            dependentField.addEventListener('change', function() {
                toggleFieldVisibility(dependentField, field, dependsValue);
            });
        }
    });
    
    function toggleFieldVisibility(dependentField, field, dependsValue) {
        const fieldContainer = field.closest('.form-group, .mb-3');
        
        if (dependentField.type === 'checkbox') {
            if ((dependentField.checked && dependsValue === 'true') || 
                (!dependentField.checked && dependsValue === 'false')) {
                fieldContainer.style.display = '';
            } else {
                fieldContainer.style.display = 'none';
            }
        } else {
            if (dependentField.value === dependsValue) {
                fieldContainer.style.display = '';
            } else {
                fieldContainer.style.display = 'none';
            }
        }
    }
});