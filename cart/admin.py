from django.contrib import admin
from django.shortcuts import render
from .models import Order, Item
admin.site.register(Order)
admin.site.register(Item)

admin.site.index_template = 'admin/custom-index.html'

def top_buyers(request):
    buyers_by_user = {}

    for order in Order.objects.all():
        user_id = order.user.id

        if user_id not in buyers_by_user:
            buyers_by_user[user_id] = {
                'username': order.user.username,
                'movies_purchased': 0,
                'purchases': [],
                }

        for item in order.item_set.all():
            buyers_by_user[user_id]['movies_purchased'] += item.quantity
            buyers_by_user[user_id]['purchases'].append({
                'movie': item.movie.name,
                'quantity': item.quantity,
                'order_id': item.order.id,
            })

    buyers = sorted(buyers_by_user.values(), key=lambda buyer: buyer['movies_purchased'], reverse=True)
    context = admin.site.each_context(request)
    context['title'] = 'Top Buyers'
    context['buyers'] = buyers

    return render(request, 'admin/top_buyers.html', context)