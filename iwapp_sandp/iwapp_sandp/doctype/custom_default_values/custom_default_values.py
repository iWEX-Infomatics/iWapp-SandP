# Copyright (c) 2024, Iwex Informatics and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class CustomDefaultValues(Document):
	pass
	def validate(self):
		if self.default_values:
			for i in self.default_values:
				if i.tax_category in ["Overseas", "Export"]:
					i.country = ""