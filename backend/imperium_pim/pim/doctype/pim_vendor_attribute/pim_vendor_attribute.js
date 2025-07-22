// Copyright (c) 2025, Imperium Systems & Consulting and contributors
// For license information, please see license.txt

frappe.ui.form.on("PIM Vendor Attribute", {
	refresh(frm) {
		// Show vendor_attribute_code field when it has a value
		if (frm.doc.vendor_attribute_code) {
			frm.set_df_property('vendor_attribute_code', 'hidden', false);
			frm.set_df_property('vendor_attribute_code', 'read_only', true);
			frm.refresh_field('vendor_attribute_code');
		}
	},
	
	after_save(frm) {
		// Check if we need to navigate back to the vendor form
		const return_vendor = localStorage.getItem('pim_vendor_return_to');
		const return_doctype = localStorage.getItem('pim_vendor_return_doctype');
		
		if (return_vendor && return_doctype === 'PIM Vendor Attribute') {
			// Clear the stored values
			localStorage.removeItem('pim_vendor_return_to');
			localStorage.removeItem('pim_vendor_return_doctype');
			
			// Navigate back to the vendor form
			frappe.set_route("Form", "PIM Vendor", return_vendor);
			
			// Show success message
			setTimeout(() => {
				frappe.show_alert({
					message: __("Vendor Attribute created successfully. Returned to mapping table."),
					indicator: 'green'
				});
			}, 500);
		}
	}
});
