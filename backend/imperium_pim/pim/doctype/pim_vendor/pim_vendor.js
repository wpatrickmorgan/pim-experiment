// Copyright (c) 2025, Imperium Systems & Consulting and contributors
// For license information, please see license.txt

frappe.ui.form.on("PIM Vendor", {
	refresh(frm) {
		// Set initial visibility based on current auth type
		toggle_auth_fields(frm);
		
		// Load attribute mapping table if we're on the attribute mapping tab
		if (frm.doc.name) {
			load_attribute_mapping_table(frm);
		}
		
		// Set up event listeners for refreshing the table
		setup_table_refresh_listeners(frm);
	},
	
	vendor_api_auth_type(frm) {
		// Toggle fields when auth type changes
		toggle_auth_fields(frm);
	},
	
	show_unmapped_only(frm) {
		// Reload table when filter changes
		load_attribute_mapping_table(frm);
	}
});

function toggle_auth_fields(frm) {
	const auth_type = frm.doc.vendor_api_auth_type;
	const show_basic_fields = auth_type === "Basic";
	
	// Show/hide username and password fields based on auth type
	frm.set_df_property("vendor_api_username", "hidden", !show_basic_fields);
	frm.set_df_property("vendor_api_password", "hidden", !show_basic_fields);
	
	// Also set reqd property - only required when Basic auth is selected
	frm.set_df_property("vendor_api_username", "reqd", show_basic_fields);
	frm.set_df_property("vendor_api_password", "reqd", show_basic_fields);
}

function setup_table_refresh_listeners(frm) {
	// Listen for new PIM Vendor Attribute documents
	frappe.realtime.on("doc_update", function(data) {
		if (data.doctype === "PIM Vendor Attribute" && 
			data.doc && data.doc.pim_vendor === frm.doc.name) {
			// Refresh the table when a vendor attribute is added/updated
			setTimeout(() => load_attribute_mapping_table(frm), 1000);
		}
	});
	
	// Listen for new PIM Attribute documents
	frappe.realtime.on("doc_update", function(data) {
		if (data.doctype === "PIM Attribute") {
			// Refresh the table when a PIM attribute is added/updated
			setTimeout(() => load_attribute_mapping_table(frm), 1000);
		}
	});
}

function load_attribute_mapping_table(frm) {
	if (!frm.doc.name) return;
	
	// Get vendor attributes and their mappings
	frappe.call({
		method: "imperium_pim.pim.doctype.pim_vendor.pim_vendor.get_attribute_mapping_data",
		args: {
			vendor: frm.doc.name,
			show_unmapped_only: frm.doc.show_unmapped_only || 0
		},
		callback: function(r) {
			if (r.message) {
				render_attribute_mapping_table(frm, r.message);
			}
		}
	});
}

function render_attribute_mapping_table(frm, data) {
	const { vendor_attributes, pim_attributes, mappings } = data;
	
	let html = `
		<div class="attribute-mapping-container">
			<style>
				.attribute-mapping-table {
					width: 100%;
					border-collapse: collapse;
					margin-bottom: 20px;
				}
				.attribute-mapping-table th,
				.attribute-mapping-table td {
					padding: 12px;
					text-align: left;
					border-bottom: 1px solid #ddd;
				}
				.attribute-mapping-table th {
					background-color: #f8f9fa;
					font-weight: 600;
				}
				.attribute-mapping-table tr:hover {
					background-color: #f5f5f5;
				}
				.mapping-controls {
					margin-top: 15px;
					padding-top: 15px;
					border-top: 1px solid #ddd;
				}
				.mapping-controls .btn {
					margin-right: 10px;
				}
				
				/* Searchable dropdown styles */
				.searchable-dropdown {
					position: relative;
					width: 100%;
				}
				.searchable-dropdown-input {
					width: 100%;
					padding: 6px 12px;
					border: 1px solid #d1d8dd;
					border-radius: 4px;
					background-color: white;
					cursor: pointer;
					font-size: 13px;
				}
				.searchable-dropdown-input:focus {
					outline: none;
					border-color: #5e72e4;
					box-shadow: 0 0 0 2px rgba(94, 114, 228, 0.1);
				}
				.searchable-dropdown-list {
					position: absolute;
					top: 100%;
					left: 0;
					right: 0;
					background: white;
					border: 1px solid #d1d8dd;
					border-top: none;
					border-radius: 0 0 4px 4px;
					max-height: 200px;
					overflow-y: auto;
					z-index: 1000;
					display: none;
				}
				.searchable-dropdown-list.show {
					display: block;
				}
				.searchable-dropdown-search {
					padding: 8px 12px;
					border-bottom: 1px solid #e9ecef;
					background: #f8f9fa;
				}
				.searchable-dropdown-search input {
					width: 100%;
					padding: 4px 8px;
					border: 1px solid #d1d8dd;
					border-radius: 3px;
					font-size: 12px;
				}
				.searchable-dropdown-search input:focus {
					outline: none;
					border-color: #5e72e4;
				}
				.searchable-dropdown-option {
					padding: 8px 12px;
					cursor: pointer;
					font-size: 13px;
					border-bottom: 1px solid #f1f3f4;
				}
				.searchable-dropdown-option:hover,
				.searchable-dropdown-option.highlighted {
					background-color: #f8f9fa;
				}
				.searchable-dropdown-option.selected {
					background-color: #e3f2fd;
					font-weight: 500;
				}
				.searchable-dropdown-option:last-child {
					border-bottom: none;
				}
				.searchable-dropdown-no-results {
					padding: 12px;
					text-align: center;
					color: #6c757d;
					font-style: italic;
				}
			</style>
			<table class="attribute-mapping-table">
				<thead>
					<tr>
						<th>Vendor Attribute Name</th>
						<th>Mapped PIM Attribute</th>
					</tr>
				</thead>
				<tbody>`;
	
	// Add rows for each vendor attribute
	vendor_attributes.forEach(vendor_attr => {
		const current_mapping = mappings[vendor_attr.name] || '';
		const current_mapping_text = current_mapping ? 
			pim_attributes.find(attr => attr.name === current_mapping)?.attribute_name || 'Select PIM Attribute...' : 
			'Select PIM Attribute...';
		
		html += `
			<tr>
				<td><strong>${vendor_attr.vendor_attribute_name}</strong></td>
				<td>
					<div class="searchable-dropdown" data-vendor-attribute="${vendor_attr.name}">
						<input type="text" 
							   class="searchable-dropdown-input" 
							   value="${current_mapping_text}"
							   placeholder="Select PIM Attribute..."
							   readonly
							   data-selected-value="${current_mapping}">
						<div class="searchable-dropdown-list">
							<div class="searchable-dropdown-search">
								<input type="text" placeholder="Search attributes..." class="search-input">
							</div>
							<div class="dropdown-options">
								<div class="searchable-dropdown-option" data-value="">Select PIM Attribute...</div>
								${pim_attributes.map(attr => 
									`<div class="searchable-dropdown-option ${current_mapping === attr.name ? 'selected' : ''}" 
										  data-value="${attr.name}">${attr.attribute_name}</div>`
								).join('')}
							</div>
						</div>
					</div>
				</td>
			</tr>`;
	});
	
	html += `
				</tbody>
			</table>
			<div class="mapping-controls">
				<button class="btn btn-default btn-sm" onclick="add_vendor_attribute('${frm.doc.name}')">
					<i class="fa fa-plus"></i> Add Vendor Attribute
				</button>
				<button class="btn btn-default btn-sm" onclick="add_pim_attribute()">
					<i class="fa fa-plus"></i> Add PIM Attribute
				</button>
			</div>
		</div>`;
	
	// Set the HTML content
	frm.set_df_property("attribute_mapping_html", "options", html);
	
	// Initialize searchable dropdowns after HTML is set
	setTimeout(() => {
		initialize_searchable_dropdowns(frm.doc.name, pim_attributes);
	}, 100);
}

// Initialize searchable dropdowns
function initialize_searchable_dropdowns(vendor, pim_attributes) {
	const dropdowns = document.querySelectorAll('.searchable-dropdown');
	
	dropdowns.forEach(dropdown => {
		const input = dropdown.querySelector('.searchable-dropdown-input');
		const list = dropdown.querySelector('.searchable-dropdown-list');
		const searchInput = dropdown.querySelector('.search-input');
		const optionsContainer = dropdown.querySelector('.dropdown-options');
		const vendorAttribute = dropdown.getAttribute('data-vendor-attribute');
		
		let highlightedIndex = -1;
		let filteredOptions = [];
		
		// Show dropdown when input is clicked
		input.addEventListener('click', function(e) {
			e.stopPropagation();
			closeAllDropdowns();
			list.classList.add('show');
			searchInput.focus();
			searchInput.value = '';
			filterOptions('');
		});
		
		// Handle search input
		searchInput.addEventListener('input', function() {
			filterOptions(this.value);
			highlightedIndex = -1;
		});
		
		// Handle keyboard navigation
		searchInput.addEventListener('keydown', function(e) {
			const visibleOptions = optionsContainer.querySelectorAll('.searchable-dropdown-option:not([style*="display: none"])');
			
			switch(e.key) {
				case 'ArrowDown':
					e.preventDefault();
					highlightedIndex = Math.min(highlightedIndex + 1, visibleOptions.length - 1);
					updateHighlight(visibleOptions);
					break;
				case 'ArrowUp':
					e.preventDefault();
					highlightedIndex = Math.max(highlightedIndex - 1, 0);
					updateHighlight(visibleOptions);
					break;
				case 'Enter':
					e.preventDefault();
					if (highlightedIndex >= 0 && visibleOptions[highlightedIndex]) {
						selectOption(visibleOptions[highlightedIndex], dropdown, vendor);
					}
					break;
				case 'Escape':
					list.classList.remove('show');
					input.focus();
					break;
			}
		});
		
		// Handle option clicks
		optionsContainer.addEventListener('click', function(e) {
			if (e.target.classList.contains('searchable-dropdown-option')) {
				selectOption(e.target, dropdown, vendor);
			}
		});
		
		// Filter options function
		function filterOptions(searchTerm) {
			const options = optionsContainer.querySelectorAll('.searchable-dropdown-option');
			let hasVisibleOptions = false;
			
			options.forEach(option => {
				const text = option.textContent.toLowerCase();
				const matches = text.includes(searchTerm.toLowerCase());
				option.style.display = matches ? 'block' : 'none';
				if (matches) hasVisibleOptions = true;
			});
			
			// Show/hide no results message
			let noResultsMsg = optionsContainer.querySelector('.searchable-dropdown-no-results');
			if (!hasVisibleOptions && searchTerm) {
				if (!noResultsMsg) {
					noResultsMsg = document.createElement('div');
					noResultsMsg.className = 'searchable-dropdown-no-results';
					noResultsMsg.textContent = 'No attributes found';
					optionsContainer.appendChild(noResultsMsg);
				}
				noResultsMsg.style.display = 'block';
			} else if (noResultsMsg) {
				noResultsMsg.style.display = 'none';
			}
		}
		
		// Update highlight function
		function updateHighlight(visibleOptions) {
			visibleOptions.forEach((option, index) => {
				option.classList.toggle('highlighted', index === highlightedIndex);
			});
		}
		
		// Select option function
		function selectOption(option, dropdown, vendor) {
			const value = option.getAttribute('data-value');
			const text = option.textContent;
			const input = dropdown.querySelector('.searchable-dropdown-input');
			const list = dropdown.querySelector('.searchable-dropdown-list');
			const vendorAttribute = dropdown.getAttribute('data-vendor-attribute');
			
			// Update input
			input.value = text;
			input.setAttribute('data-selected-value', value);
			
			// Update selected state
			dropdown.querySelectorAll('.searchable-dropdown-option').forEach(opt => {
				opt.classList.remove('selected');
			});
			option.classList.add('selected');
			
			// Close dropdown
			list.classList.remove('show');
			
			// Update mapping
			update_attribute_mapping_new(vendor, vendorAttribute, value);
		}
	});
	
	// Close dropdowns when clicking outside
	document.addEventListener('click', closeAllDropdowns);
	
	function closeAllDropdowns() {
		document.querySelectorAll('.searchable-dropdown-list').forEach(list => {
			list.classList.remove('show');
		});
	}
}

// Updated attribute mapping function for searchable dropdowns
function update_attribute_mapping_new(vendor, vendor_attribute, pim_attribute) {
	frappe.call({
		method: "imperium_pim.pim.doctype.pim_vendor.pim_vendor.update_attribute_mapping",
		args: {
			vendor: vendor,
			vendor_attribute: vendor_attribute,
			pim_attribute: pim_attribute
		},
		callback: function(r) {
			if (r.message && r.message.success) {
				frappe.show_alert({
					message: r.message.message,
					indicator: 'green'
				});
			} else if (r.message && r.message.error) {
				frappe.show_alert({
					message: r.message.error,
					indicator: 'red'
				});
				// Reload the table to reset the dropdown
				const frm = cur_frm;
				load_attribute_mapping_table(frm);
			}
		}
	});
}

// Global functions for the HTML controls (kept for backward compatibility)
window.update_attribute_mapping = function(dropdown, vendor) {
	const vendor_attribute = dropdown.getAttribute('data-vendor-attribute');
	const pim_attribute = dropdown.value;
	
	frappe.call({
		method: "imperium_pim.pim.doctype.pim_vendor.pim_vendor.update_attribute_mapping",
		args: {
			vendor: vendor,
			vendor_attribute: vendor_attribute,
			pim_attribute: pim_attribute
		},
		callback: function(r) {
			if (r.message && r.message.success) {
				frappe.show_alert({
					message: r.message.message,
					indicator: 'green'
				});
			} else if (r.message && r.message.error) {
				frappe.show_alert({
					message: r.message.error,
					indicator: 'red'
				});
				// Reload the table to reset the dropdown
				const frm = cur_frm;
				load_attribute_mapping_table(frm);
			}
		}
	});
};

window.add_vendor_attribute = function(vendor) {
	// Store the vendor context for navigation back
	localStorage.setItem('pim_vendor_return_to', vendor);
	localStorage.setItem('pim_vendor_return_doctype', 'PIM Vendor Attribute');
	
	frappe.new_doc("PIM Vendor Attribute", {
		pim_vendor: vendor
	});
};

window.add_pim_attribute = function() {
	const current_vendor = cur_frm ? cur_frm.doc.name : null;
	
	if (current_vendor) {
		// Store the vendor context for navigation back
		localStorage.setItem('pim_vendor_return_to', current_vendor);
		localStorage.setItem('pim_vendor_return_doctype', 'PIM Attribute');
	}
	
	frappe.new_doc("PIM Attribute");
};
