"""
Deprectaed: can be configured on the json directly (and for the assignment, it needs to be set there,
otherwise the validator fails

from frappe import _

def get_data():
   return {
      'fieldname': 'passenger',
      'transactions': [
         {
            'label': _('Connections'),
            'items': ['Airplane Ticket']
         }
      ]
   }

"""
