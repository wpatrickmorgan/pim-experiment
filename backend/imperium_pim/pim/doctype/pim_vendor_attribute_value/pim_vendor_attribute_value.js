// Copyright (c) 2025, Imperium Systems & Consulting and contributors
// For license information, please see license.txt

frappe.ui.form.on("PIM Vendor Attribute Value", {
	refresh(frm) {
		// Show vendor_attribute_value_code field when it has a value
		if (frm.doc.vendor_attribute_value_code) {
			frm.set_df_property('vendor_attribute_value_code', 'hidden', false);
			frm.set_df_property('vendor_attribute_value_code', 'read_only', true);
			frm.refresh_field('vendor_attribute_value_code');
		}
	}
});
