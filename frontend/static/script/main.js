document.addEventListener('DOMContentLoaded', function() {
    // --- Validation (existing) ---
    document.querySelector('form').addEventListener('submit', function(e) {
        const inputs = this.querySelectorAll('input[required]');
        let valid = true;
        inputs.forEach(input => {
            if (!input.checkValidity()) {
                input.classList.add('is-invalid');
                valid = false;
            }
        });
        if (!valid) e.preventDefault();
    });

    document.querySelectorAll('input').forEach(input => {
        input.addEventListener('input', () => {
            if (input.checkValidity()) {
                input.classList.remove('is-invalid');
            }
        });
    });

    // --- Input override checkboxes ---
    const limits = {
        'fixed_acidity': [4.6, 15.9],
        'volatile_acidity': [0.12, 1.58],
        'citric_acid': [0.0, 1.0],
        'residual_sugar': [0.9, 15.5],
        'chlorides': [0.012, 0.611],
        'free_sulfur_dioxide': [1.0, 72.0],
        'total_sulfur_dioxide': [6.0, 289.0],
        'density': [0.99007, 1.00369],
        'pH': [2.74, 4.01],
        'sulphates': [0.33, 2.0],
        'alcohol': [8.4, 14.9]
    };

    Object.keys(limits).forEach(field => {
        const input = document.getElementById(field);
        if (!input) return;
        // Create override checkbox
        const wrapper = document.createElement('div');
        wrapper.className = "form-check mt-1";
        wrapper.innerHTML = `
            <input class="form-check-input" type="checkbox" id="${field}_override">
            <label class="form-check-label small" for="${field}_override">
                Allow any value
            </label>
        `;
        input.parentNode.appendChild(wrapper);

        // Checkbox logic
        const checkbox = document.getElementById(`${field}_override`);
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                input.removeAttribute('min');
                input.removeAttribute('max');
            } else {
                input.setAttribute('min', limits[field][0]);
                input.setAttribute('max', limits[field][1]);
            }
        });
    });

    // --- Rebuild Model Button ---
    // Add button below form
    const form = document.getElementById('wineForm');
    const rebuildDiv = document.createElement('div');
    rebuildDiv.className = "text-center mt-4";
    rebuildDiv.innerHTML = `
        <button type="button" class="btn btn-warning" id="rebuildModelBtn">
            <i class="fas fa-sync"></i> Rebuild Model
        </button>
        <div id="retrain-status" class="mt-2 small"></div>
    `;
    form.parentNode.appendChild(rebuildDiv);

    document.getElementById('rebuildModelBtn').addEventListener('click', async function() {
        const status = document.getElementById('retrain-status');
        status.textContent = "Retraining model...";
        status.className = 'text-info mt-2 small';
        try {
            const response = await fetch('/retrain', { method: 'POST' });
            const result = await response.json();
            status.textContent = result.message;
            status.className = response.ok ? 'text-success mt-2 small' : 'text-danger mt-2 small';
        } catch (error) {
            status.textContent = "Error: " + error.message;
            status.className = 'text-danger mt-2 small';
        }
    });
});
