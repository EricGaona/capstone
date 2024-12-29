# from django.test import TestCase

# Create your tests here.
# from django.test import TestCase, Client
# from django.contrib.auth import get_user_model

# class SendMoneyTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.User = get_user_model()

#         # Create sender and recipient users
#         self.sender = self.User.objects.create_user(
#             username='ana@example.com',
#             email='ana@example.com',
#             password='123',
#             account_number='8115761330',
#             balance=1000
#         )
#         self.recipient = self.User.objects.create_user(
#             username='popo@gmail.com',
#             email='popo@gmail.com',
#             password='123',
#             account_number='6285362259',
#             balance=500
#         )

#     def test_send_money_success(self):
#         response = self.client.post('/send_money/', {
#             'senderAccountNumber': '8115761330',
#             'recipientAccountNumber': '6285362259',
#             'amount': 200
#         }, content_type='application/json')

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(self.sender.balance - 200, self.User.objects.get(account_number='1234567890').balance)
#         self.assertEqual(self.recipient.balance + 200, self.User.objects.get(account_number='0987654321').balance)
#         self.assertJSONEqual(str(response.content, encoding='utf8'), {
#             'message': 'Money sent successfully!'
#         })

#     def test_send_money_insufficient_funds(self):
#         response = self.client.post('/send_money/', {
#             'senderAccountNumber': '8115761330',
#             'recipientAccountNumber': '6285362259',
#             'amount': 1500
#         }, content_type='application/json')

#         self.assertEqual(response.status_code, 400)
#         self.assertJSONEqual(str(response.content, encoding='utf8'), {
#             'error': 'Insufficient funds.'
#         })

#     def test_send_money_invalid_account(self):
#         response = self.client.post('/send_money/', {
#             'senderAccountNumber': '8115761330',
#             'recipientAccountNumber': 'INVALID',
#             'amount': 100
#         }, content_type='application/json')

#         self.assertEqual(response.status_code, 400)
#         self.assertJSONEqual(str(response.content, encoding='utf8'), {
#             'error': 'One or both account numbers are invalid.'
#         })
