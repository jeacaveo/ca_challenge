from rest_framework import (
    viewsets, permissions, filters as rest_filters, mixins)

from consumers import models, serializers, filters


class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    Reviews endpoint
    ==========

        Creates and returns consumer reviews.

        Accepts: GET, POST.

    Params:
    -------
    - **nested**: *bool*, queryparam, Indicates if the returned structure must
        agregate data of the related entities.

    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    filter_backends = (filters.ReviewEndpointFilterBackend,
                       rest_filters.DjangoFilterBackend,
                       rest_filters.OrderingFilter,)
    filter_fields = ("company", "reviewer", "rating")
    filter_fields = ("company", "reviewer", "rating")

    # Override
    def get_serializer_class(self):
        """
        Overriding to use custom nested serializer when requested.

        """
        if (self.request.method == "GET" and
                self.request.query_params.get("nested")):
            return serializers.ReviewNestedSerializer
        return serializers.ReviewSerializer

    # Override
    def create(self, request, *args, **kwargs):
        """
        Overriding to add user to request data.

        """
        request.data.update({"reviewer": self.request.user.id,
                             "ip_address": request.META.get('REMOTE_ADDR')})

        return super().create(request, *args, **kwargs)
