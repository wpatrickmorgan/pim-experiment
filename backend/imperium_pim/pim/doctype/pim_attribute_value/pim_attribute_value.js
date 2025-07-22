// Copyright (c) 2025, Imperium Systems & Consulting and contributors
// For license information, please see license.txt

frappe.ui.form.on("PIM Attribute Value", {
	refresh(frm) {
		// Show attribute_value_code field when it has a value, even though it's read-only
		if (frm.doc.attribute_value_code) {
			frm.set_df_property('attribute_value_code', 'hidden', 0);
		} else {
			frm.set_df_property('attribute_value_code', 'hidden', 1);
		}
	},
	
	// Also check when pim_attribute or attribute_value_name changes
	// as these trigger the auto-generation
	pim_attribute(frm) {
		setTimeout(() => {
			if (frm.doc.attribute_value_code) {
				frm.set_df_property('attribute_value_code', 'hidden', 0);
			}
		}, 100);
	},
	
	attribute_value_name(frm) {
		setTimeout(() => {
			if (frm.doc.attribute_value_code) {
				frm.set_df_property('attribute_value_code', 'hidden', 0);
			}
		}, 100);
	}
});
