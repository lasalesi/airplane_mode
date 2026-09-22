# Copyright (c) 2026, libracore AG and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import random


class AirplaneTicket(Document):
	def before_save(self):
		# calculate total
		total_amount = self.flight_price
		for ao in self.add_ons:
			total_amount += ao.amount
		self.total_amount = total_amount
		
		# if no seat is assigned, assign a random seat
		if not self.seat:
			self.seat = generate_random_code()
			
		return
		
	def validate(self):
		# check no duplicates on add-ons
		seen_add_ons = []
		unique_add_ons = []
		for ao in self.add_ons:
			if ao.add_on_type not in seen_add_ons:
				seen_add_ons.append(ao.add_on_type)
				unique_add_ons.append(ao)
		self.add_ons = unique_add_ons
		return

	def on_submit(self):
		if self.status != "Boarded":
			frappe.throw("You can only submit the ticket once the passenger has boarded the airplane. Please update the status first")
		return

def generate_random_code():
    # Generate a random integer from 0 to 99
    number = random.randint(0, 99)
    
    # Choose a random capital letter from A to E
    letter = random.choice(['A', 'B', 'C', 'D', 'E'])
    
    # Combine and return the result
    return f"{number}{letter}"
