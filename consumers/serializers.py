from rest_framework import serializers

from consumers import models


class ReviewerSerializer(serializers.Serializer):
    """ Companymodel serializer. """

    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length=100)


class CompanySerializer(serializers.ModelSerializer):
    """ Companymodel serializer. """

    class Meta:
        model = models.Company
        fields = "__all__"


class ReviewNestedSerializer(serializers.ModelSerializer):
    """ Review nested model serializer. """

    company = CompanySerializer()
    reviewer = ReviewerSerializer()

    class Meta:
        model = models.Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """ Review model serializer. """

    class Meta:
        model = models.Review
        fields = "__all__"
