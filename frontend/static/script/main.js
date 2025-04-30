const OVERRIDE_LABEL_TEXT = "Any Value";


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
        const checkbox = document.getElementById(field + '_override');
        if (input && checkbox) {
            checkbox.addEventListener('change', function() {
                if (this.checked) {
                    input.removeAttribute('min');
                    input.removeAttribute('max');
                } else {
                    input.setAttribute('min', limits[field][0]);
                    input.setAttribute('max', limits[field][1]);
                }
            });
        }
    });
});

document.querySelectorAll('.form-check-label').forEach(label => {
    label.textContent = OVERRIDE_LABEL_TEXT;
});
