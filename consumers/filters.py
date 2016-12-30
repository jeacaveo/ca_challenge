from rest_framework import filters


class ReviewEndpointFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(reviewer=request.user)
