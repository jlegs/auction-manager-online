from django.test import TestCase

# Create your tests here.
from manager.models import Invoice, Attendee, MergedInvoice, AuctionItem


class AttendeeTestCase(TestCase):
	def setUp(self):
		self.attendee = Attendee.objects.create(first_name='Josh', last_name='Brown', table_assignment='A', bid_number=1)
		self.invoice = self.attendee.create_invoice()
		self.item1 = AuctionItem.objects.create(description='A test item', retail_value=5.00, selling_price=10.50, starting_value=5.00, increment_amount=5.00, item_number=20)
		self.item2 = AuctionItem.objects.create(description='A second test item', retail_value=5.00, selling_price=10.50, starting_value=5.00, increment_amount=5.00, item_number=20)

	def test_attendee_has_invoice(self):
		'''Checks for existence of Invoice after an Attendee is created and Attendee.create_invoice() is called'''
		self.assertTrue(self.attendee.invoice)
		self.assertEqual(self.invoice.attendee, self.attendee)
		self.assertEqual(self.invoice.attendee.first_name, 'Josh')
		self.assertEqual(self.invoice.id, 1)



class InvoiceTestCase(TestCase):
	def setUp(self):
		self.attendee = Attendee.objects.create(first_name='Josh', last_name='Brown', table_assignment='A', bid_number=1)
		self.invoice = self.attendee.create_invoice()
		self.item1 = AuctionItem.objects.create(description='A test item', retail_value=5.00, selling_price=10.50, starting_value=5.00, increment_amount=5.00, item_number=20)
		self.item2 = AuctionItem.objects.create(description='A second test item', retail_value=5.00, selling_price=10.50, starting_value=5.00, increment_amount=5.00, item_number=20)


	def test_invoice_add_and_remove_item(self):
		'''Tests whether adding an item and then removing it works correctly, as well as whether it works simultaneously.'''
		self.invoice.update_invoice(add_item=self.item1)
		self.assertEqual(self.invoice.items.all()[0], self.item1)

		self.invoice.update_invoice(add_item=self.item2, remove_item=self.item1)
		self.assertEqual(self.invoice.items.all()[0], self.item2)
		self.assertEqual(len(self.invoice.items.all()), 1)

		self.invoice.update_invoice(remove_item=self.item2)
		self.assertFalse(self.invoice.items.all())


