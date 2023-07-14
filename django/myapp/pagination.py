import math
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        prev = self.get_previous_link()
        next = self.get_next_link()
        print(prev)
        print(next)
        # current = 1
        if not prev:
            print(prev)
            current = 1
        elif not next:
            print(next)
            current = int(prev.split('=')[1]) + 1
        else:
            print('here:')
            print(prev)
            print(next)
            try:
                current = int( ( int(prev.split('=')[1]) + int(next.split('=')[1]) ) / 2 )
            except IndexError:
                current = int(next.split('=')[1]) - 1
        return Response({
            'currentPage': current,
            'items': data,
            'totalItems': self.page.paginator.count,
            'totalPages': math.ceil(self.page.paginator.count/settings.REST_FRAMEWORK['PAGE_SIZE']),
            # 'links': {
            #     'next': self.get_next_link(),
            #     'previous': self.get_previous_link()
            # },
            # 'count': self.page.paginator.count,
            # 'results': data
        })