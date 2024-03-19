# Copyright (c) 2024, Iwex Informatics and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CustomDefaultValues(Document):
	pass
	def validate(self):
		if self.default_values:
			for i in self.default_values:
				if i.tax_category in ["Overseas", "Export"]:
					i.country = ""
		# Get a list of items
		items = frappe.get_all("Item", fields=["name"])
		# Iterate over each item
		for item in items:
			item_name = item.name
			# Fetch the child table data for the current item
			item_defaults = frappe.db.get_all("Item Default", filters={"parent": item_name}, fields=["name", "company"])
			# print("item_defaults", item_defaults)
			# Iterate over each row in the child table
			for default_row in item_defaults:
				if default_row.company == "CAITS Group of Companies":
					# Delete the row if the company matches the specified value
					frappe.db.delete("Item Default", default_row.name)

		# company_not_grp = frappe.db.get_list("Company", filters = {"is_group":0}, fields = ["name", "abbr"])
		# tax_category = frappe.db.get_list("Tax Category", pluck = "name")
		# tax_list = []
		# if company_not_grp and tax_category:
		# 	for com in company_not_grp:
		# 		print(com)
		# 		for tax in tax_category:
		# 			tax_list.append({"company":com.get("name"), "abbr":com.get("abbr"), "tax_category":tax})
		# if len(tax_list) > 0:
		# 	self.taxes = []
		# 	for t in tax_list:
		# 		self.append("taxes", {"company" : t.get('company'), "abbr" :t.get('abbr'), "tax_category" :t.get('tax_category')})