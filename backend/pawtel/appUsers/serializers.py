from rest_framework import serializers  # Importamos los serializadores de django
from appUsers.models import AppUser  

class AppUserSerializer(serializers.ModelSerializer):  # Definimos el serializador
    class Meta:
        model = AppUser  # serializador usará el modelo AppUser
        fields = [  
            "id", "username", "first_name", "last_name", "email", "phone",
            "date_joined", "last_login", "is_active", "is_staff", "is_superuser"
        ]
        
        extra_kwargs = {  #validaciones adicionales
            "email": {"required": True},  
            "phone": {"required": True},  
        }

    def to_representation(self, instance):  #instance se refiere a appUser y self al serializador de arriba
        """ 
        Personaliza la salida JSON para que siga el formato `snake_case`.
        DRF llama automáticamente a este método cuando serializa un objeto.
        """
        representation = super().to_representation(instance)  # Obtiene la representacion estandar del json
        
        # Retornamos un diccionario(json) con los nombres de los campos
        return {
            "id": representation["id"],
            "username": representation["username"],
            "first_name": representation["first_name"],
            "last_name": representation["last_name"],
            "email": representation["email"],
            "phone": representation["phone"],
            "date_joined": representation["date_joined"],  
            "last_login": representation["last_login"],  
            "is_active": representation["is_active"],  
            "is_staff": representation["is_staff"], 
            "is_superuser": representation["is_superuser"]  

        }

        #realmente este serializador no cambia nada ya que los atributos de la clase AbstractUser ya vienen en snake_case pero
        #lo hago ya que se quedo que habría un serializador por entidad
