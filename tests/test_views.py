# from django.test import TestCase, Client
# from django.contrib.auth.models import User
# from django.urls import reverse
# from core.views import index


# class TestViews(TestCase):


# 	def test_index_view_GET(self):
# 		url = reverse('core:index')
# 		self.client = Client()
# 		self.user = User.objects.create_user('test', 'test@gmail.com', 'testpassword')
# 		self.client.login(username='test', password='testpassword')

# 		response = self.client.get(url)
# 		print(response)
		
# 		self.assertEqual(response.status_code, 200)
# 		self.assertTemplateUsed(response, 'core/index.html')
# 		self.assertTemplateUsed(response, 'core/base.html')


# 	# def test_about_view_GET(self):
# 	# 	url = reverse('about')
# 	# 	response = self.client.get(url)
		
# 	# 	self.assertEqual(response.status_code, 200)
# 	# 	self.assertTemplateUsed(response, 'about.html')
# 	# 	self.assertTemplateUsed(response, 'base.html')


# 	# def test_compare_view_GET(self):
# 	# 	url = reverse('compare') + '?concept=data_types&lang1=Python&lang2=Java'
# 	# 	response = self.client.get(url)

# 	# 	self.assertEquals(response.status_code, 200)
# 	# 	self.assertTemplateUsed(response, 'compare.html')
# 	# 	self.assertTemplateUsed(response, 'base.html')


# 	# def test_reference_view_GET(self):
# 	# 	url = reverse('reference') + '?concept=data_types&lang=Python'	
# 	# 	response = self.client.get(url)

# 	# 	self.assertEquals(response.status_code, 200)
# 	# 	self.assertTemplateUsed(response, 'reference.html')
# 	# 	self.assertTemplateUsed(response, 'base.html')