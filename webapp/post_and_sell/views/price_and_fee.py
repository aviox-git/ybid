from django.shortcuts import render, HttpResponseRedirect,HttpResponse
from django.views.generic import View
from login.helper_fun import StaffUserOnly
from post_and_sell.models import Prices, SERVICE_TYPE
import json
from datetime import datetime


class AdminPriceAndFee(StaffUserOnly,View):
	template_name = 'admin-manage-price-and-fee.html'

	def get(self, request, *args, **kwargs):

		prices = Prices.objects.all()
		if prices:
			pass
		else:
			package_type = SERVICE_TYPE
			prices = [Prices(
							package = packg[1],
							service_type = packg[0],
							special_fee  = 20,
							special_minimum_students = 20,
							regular_fee = 20,
							regular_minimum_students = 20,
							discount = 20,
							minimum_students = 20,
							code = "xyz"
							) for packg in package_type]
			Prices.objects.bulk_create(prices)

		return render(request,self.template_name,locals())



	def post(self,request):
		all_arry = json.loads(request.POST.get('all_arry'))
		for price_id in all_arry:
			price_obj = Prices.objects.get(pk = price_id)
			for values in all_arry[price_id]:
				if values['name'] == 'expire_date':
					date = datetime.strptime(values['value'], '%d/%m/%Y')
					price_obj.expire_date = date
				elif values['name'] == 'code':
					price_obj.code = values['value']
				else:
					if values['value']:
						val = float(values['value'])
					else:
						val = None
					setattr(price_obj, values['name'], val)
			price_obj.save()
		return HttpResponse(json.dumps({}),content_type = 'application/json')