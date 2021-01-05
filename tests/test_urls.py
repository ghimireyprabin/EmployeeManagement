from django.test import SimpleTestCase
from django.urls import reverse, resolve
from core.views import index, ManagerDashboard, profile


class TestUrls(SimpleTestCase):


	def test_index_url(self):
		url = reverse('core:index')
		self.assertEqual(resolve(url).func, index)

	def test_profile_url(self):
		url = reverse('core:profile')
		self.assertEqual(resolve(url).func, profile)


	# def test_EPIC_url(self):
	# 	url = reverse('core:add-personal-info')
	# 	print(resolve(url))
	# 	self.assertEqual(resolve(url).func, EPICreateView.as_view())


	# def test_about_url(self):
	# 	url = reverse('about')
	# 	self.assertEqual(resolve(url).func, about)


	# def test_compare_url(self):
	# 	url = reverse('compare')
	# 	self.assertEqual(resolve(url).func, compare)


	# def test_reference_url(self):
	# 	url = reverse('reference')
	# 	self.assertEqual(resolve(url).func, reference)
