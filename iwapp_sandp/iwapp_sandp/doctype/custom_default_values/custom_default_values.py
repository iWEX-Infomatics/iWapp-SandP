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