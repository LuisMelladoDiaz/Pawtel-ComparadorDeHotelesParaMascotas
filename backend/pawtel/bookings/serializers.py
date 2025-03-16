from pawtel.base_serializer import BaseSerializer
from pawtel.bookings.models import Booking

class BookingSerializer(BaseSerializer):
    fields_required_for_post = ["start_date", "end_date", "total_price", "customer", "room"]
    fields_editable = ["start_date", "end_date", "total_price"]
    fields_not_readable = []

    class Meta:
        model = Booking
        fields = [
            "id",
            "creation_date",
            "start_date",
            "end_date",
            "total_price",
            "customer",
            "room"
        ]
        extra_kwargs = {
            "id": {"read_only": True},  
            "creation_date": {"read_only": True},  
            "start_date": {"allow_null": False},  
            "end_date": {"allow_null": False},  
            "total_price": {
                "min_value": Decimal("1.00"),
                "decimal_places": 2,
                "allow_null": False,
            },
            "customer": {"allow_null": False},  
            "room": {"allow_null": False},  
        }

    def validate_start_date(self, value):
        from datetime import date
        if value <= date.today():
            raise serializers.ValidationError("La fecha de inicio debe ser en el futuro.")
        return value

    def validate_end_date(self, value):
        from datetime import date
        if value <= date.today():
            raise serializers.ValidationError("La fecha de fin debe ser en el futuro.")
        return value
