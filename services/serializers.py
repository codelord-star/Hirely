from rest_framework import serializers

from services.models import Category, Service


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [ 
            'id',
            'title', 
            'description', 
            'category', 
            'price_ksh', 
            'pricing_type', 
            'service_image', 
            'duration_min', 
            'duration_max', 
            'duration_unit', 
            'is_available',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        if self.instance is not None:
            duration_min = data.get('duration_min', self.instance.duration_min)
            duration_max = data.get('duration_max', self.instance.duration_max)
            duration_unit = data.get('duration_unit', self.instance.duration_unit)
        else:
            duration_min = data.get('duration_min')
            duration_max = data.get('duration_max')
            duration_unit = data.get('duration_unit')

        # Conditions
        if duration_min is not None and duration_max is not None:
            if duration_min > duration_max:
                raise serializers.ValidationError("duration_min cannot be greater than duration_max.")

        if duration_min is not None or duration_max is not None:
            if not duration_unit:
                raise serializers.ValidationError("duration_unit must be provided if duration_min or duration_max is provided.")
            
        if duration_min is not None and duration_min <= 0:
            raise serializers.ValidationError("duration_min must be greater than zero.")
        
        if duration_max is not None and duration_max <= 0:
            raise serializers.ValidationError("duration_max must be greater than zero.")

        if duration_min is None and duration_max is None and duration_unit:
            raise serializers.ValidationError("duration_unit cannot be provided without duration_min or duration_max.")

        return data