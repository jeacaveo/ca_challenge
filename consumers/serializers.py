from rest_framework import serializers

from consumers import models


class ReviewSerializer(serializers.ModelSerializer):
    """ Review model serializer. """

    class Meta:
        model = models.Review
        fields = "__all__"
