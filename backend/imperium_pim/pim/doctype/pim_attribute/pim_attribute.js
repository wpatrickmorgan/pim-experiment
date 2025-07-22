// Copyright (c) 2025, Imperium Systems & Consulting and contributors
// For license information, please see license.txt

frappe.ui.form.on("PIM Attribute", {
	refresh(frm) {
		// Set up real-time validation for attribute_code field
		frm.set_df_property('attribute_code', 'description', 
			'Only lowercase letters (a-z), numbers (0-9), and underscores (_) are allowed');
	},
	
	attribute_code(frm) {
		// Validate attribute_code in real-time as user types
		validate_attribute_code(frm);
	},
	
	after_save(frm) {
		// Check if we need to navigate back to the vendor form
		const return_vendor = localStorage.getItem('pim_vendor_return_to');
		const return_doctype = localStorage.getItem('pim_vendor_return_doctype');
		
		if (return_vendor && return_doctype === 'PIM Attribute') {
			// Clear the stored values
			localStorage.removeItem('pim_vendor_return_to');
			localStorage.removeItem('pim_vendor_return_doctype');
			
			// Navigate back to the vendor form
			frappe.set_route("Form", "PIM Vendor", return_vendor);
			
			// Show success message
			setTimeout(() => {
				frappe.show_alert({
					message: __("PIM Attribute created successfully. Returned to mapping table."),
					indicator: 'green'
				});
			}, 500);
		}
	}
});

function validate_attribute_code(frm) {
	const attribute_code = frm.doc.attribute_code;
	
	if (!attribute_code) {
		// Clear any previous validation messages
		frm.set_df_property('attribute_code', 'description', 
			'Only lowercase letters (a-z), numbers (0-9), and underscores (_) are allowed');
		return;
	}
	
	// Check if the attribute_code matches the required pattern
	const pattern = /^[a-z0-9_]+$/;
	
	if (!pattern.test(attribute_code)) {
		// Find invalid characters for helpful error message
		const invalid_chars = [];
		for (let char of attribute_code) {
			if (!/[a-z0-9_]/.test(char) && !invalid_chars.includes(char)) {
				invalid_chars.push(char);
			}
		}
		
		let error_msg = 'Invalid format! Only lowercase letters (a-z), numbers (0-9), and underscores (_) are allowed.';
		
		if (invalid_chars.length > 0) {
			if (invalid_chars.length === 1) {
				error_msg += ` Invalid character: '${invalid_chars[0]}'`;
			} else {
				error_msg += ` Invalid characters: ${invalid_chars.map(char => `'${char}'`).join(', ')}`;
			}
		}
		
		// Show error message in field description
		frm.set_df_property('attribute_code', 'description', 
			`<span style="color: red;">${error_msg}</span>`);
		
		// Optionally show a toast message for immediate feedback
		frappe.show_alert({
			message: error_msg,
			indicator: 'red'
		}, 3);
		
	} else {
		// Valid format - show success message
		frm.set_df_property('attribute_code', 'description', 
			'<span style="color: green;">✓ Valid format</span>');
	}
}
