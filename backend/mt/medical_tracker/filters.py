from rest_framework.filters import OrderingFilter

class MyOrderingFilter(OrderingFilter):
    ordering_param = 'sort' 