// Copyright (c) 2025, Imperium Systems & Consulting and contributors
// For license information, please see license.txt

frappe.ui.form.on('PIM Item', {
	refresh: function(frm) {
		// Add custom buttons or actions if needed
		if (frm.doc.sku && !frm.is_new()) {
			frm.add_custom_button(__('Validate SKU'), function() {
				validate_sku_uniqueness(frm);
			});
		}
		
		// Ensure SKU field is always read-only and visible
		ensure_sku_always_readonly(frm);
		
		// Show SKU preview if vendor_code and vendor_sku are set
		update_sku_preview(frm);
	},
	
	vendor_code: function(frm) {
		update_sku_preview(frm);
		
		// Get vendor information
		if (frm.doc.vendor_code) {
			frappe.call({
				method: 'imperium_pim.pim.doctype.pim_item.pim_item.get_vendor_info',
				args: {
					vendor_code: frm.doc.vendor_code
				},
				callback: function(r) {
					if (r.message && r.message.success) {
						if (!r.message.vendor_active) {
							frappe.msgprint({
								title: __('Warning'),
								message: __('Selected vendor is not active'),
								indicator: 'orange'
							});
						}
					}
				}
			});
		}
	},
	
	vendor_sku: function(frm) {
		update_sku_preview(frm);
	},
	
	upc: function(frm) {
		validate_upc_format(frm);
	},
	
	before_save: function(frm) {
		// Final validation before save
		if (frm.doc.upc) {
			validate_upc_format(frm);
		}
		
		// Ensure SKU is properly set before save
		if (!frm.doc.sku && frm.doc.vendor_code && frm.doc.vendor_sku) {
			// Temporarily make field editable to set the value
			frm.set_df_property('sku', 'read_only', 0);
			frm.set_value('sku', `${frm.doc.vendor_code}-${frm.doc.vendor_sku}`);
			frm.set_df_property('sku', 'read_only', 1);
		}
		
		// Reset SKU field styling if it was a preview
		if (frm._sku_is_preview) {
			setTimeout(() => {
				if (frm.get_field('sku').$input) {
					frm.get_field('sku').$input.css('color', '');
					frm.get_field('sku').$input.css('font-style', '');
				}
			}, 100);
			frm._sku_is_preview = false;
		}
	},
	
	after_save: function(frm) {
		// Ensure SKU field remains read-only and visible after save
		ensure_sku_always_readonly(frm);
		
		// Clear any preview styling since document is now saved
		clear_sku_preview_styling(frm);
	}
});

function ensure_sku_always_readonly(frm) {
	// SKU field must ALWAYS be read-only (both before and after saving)
	frm.set_df_property('sku', 'read_only', 1);
	
	// Ensure the field is always visible
	frm.set_df_property('sku', 'hidden', 0);
}

function clear_sku_preview_styling(frm) {
	// Clear any preview styling after save
	if (frm._sku_is_preview) {
		setTimeout(() => {
			if (frm.get_field('sku').$input) {
				frm.get_field('sku').$input.css('color', '');
				frm.get_field('sku').$input.css('font-style', '');
			}
		}, 100);
		frm._sku_is_preview = false;
	}
}

function update_sku_preview(frm) {
	// Show preview for new documents only (not saved yet)
	if (frm.is_new()) {
		if (frm.doc.vendor_code && frm.doc.vendor_sku) {
			const preview_sku = `${frm.doc.vendor_code}-${frm.doc.vendor_sku}`;
			
			// Update the SKU field directly since it's read-only
			// We need to temporarily make it editable to update the value
			frm.set_df_property('sku', 'read_only', 0);
			frm.set_value('sku', preview_sku);
			frm.set_df_property('sku', 'read_only', 1);
			
			// Apply preview styling after a short delay
			setTimeout(() => {
				if (frm.get_field('sku').$input) {
					frm.get_field('sku').$input.css('color', '#888');
					frm.get_field('sku').$input.css('font-style', 'italic');
				}
			}, 100);
			
			// Track that this is a preview value
			frm._sku_is_preview = true;
		} else {
			// Clear the preview if vendor fields are cleared
			if (frm._sku_is_preview) {
				frm.set_df_property('sku', 'read_only', 0);
				frm.set_value('sku', '');
				frm.set_df_property('sku', 'read_only', 1);
				frm._sku_is_preview = false;
				
				// Reset field styling
				setTimeout(() => {
					if (frm.get_field('sku').$input) {
						frm.get_field('sku').$input.css('color', '');
						frm.get_field('sku').$input.css('font-style', '');
					}
				}, 100);
			}
		}
	}
}

function validate_sku_uniqueness(frm) {
	if (!frm.doc.sku) {
		frappe.msgprint(__('No SKU to validate'));
		return;
	}
	
	frappe.call({
		method: 'imperium_pim.pim.doctype.pim_item.pim_item.validate_sku_uniqueness',
		args: {
			sku: frm.doc.sku,
			current_name: frm.doc.name
		},
		callback: function(r) {
			if (r.message) {
				const indicator = r.message.valid ? 'green' : 'red';
				frappe.msgprint({
					title: __('SKU Validation'),
					message: r.message.message,
					indicator: indicator
				});
			}
		}
	});
}

function validate_upc_format(frm) {
	if (!frm.doc.upc) return;
	
	const upc = frm.doc.upc.toString().trim();
	const upc_regex = /^\d{12}$/;
	
	if (!upc_regex.test(upc)) {
		frappe.msgprint({
			title: __('Invalid UPC Format'),
			message: __('UPC must be exactly 12 digits. Current value: {0} ({1} characters)', 
				[frm.doc.upc, upc.length]),
			indicator: 'red'
		});
		
		// Highlight the field
		frm.get_field('upc').$input.addClass('has-error');
		
		// Remove error styling after user starts typing
		frm.get_field('upc').$input.on('input', function() {
			$(this).removeClass('has-error');
		});
	} else {
		// Remove any error styling
		frm.get_field('upc').$input.removeClass('has-error');
	}
}
