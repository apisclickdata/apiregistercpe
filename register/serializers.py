from rest_framework import serializers
from .models import CPEModel, ReceptorModel, EmisorModel, TipoCPEModel, TipoDOCModel, ResumenModel, CPEResumenModel, EstadoModel

class RegistroCPESerializer(serializers.ModelSerializer):
    class Meta:
        model = CPEModel
        exclude = ['CdrCpe','idCdr','fechaCdr','horaCdr','statusCdr','mensajeCdr']

class RegistroResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumenModel
        exclude = ['CdrCpe','idCdr','fechaCdr','horaCdr','statusCdr','mensajeCdr', 'ticketresumen']
 
 
class ActualizacionTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumenModel
        exclude = ['ID','emisorId','fechaemisionresumen','fechageneracionresumen','fechapublicacionresumen','XmlCpe','CdrCpe', 'PdfCpe','idCdr','fechaCdr','horaCdr','statusCdr','mensajeCdr','tipocpeId','estadoId','usuId'] 
    def update(self): 
        self.instance.ticketresumen = self.validated_data.get('ticketresumen', self.instance.ticketresumen) 
        self.instance.save()
        return self.instance

class ActualizacionCPESerializer(serializers.ModelSerializer):
    class Meta:
        model = CPEModel
        exclude = ['serieCpe', 'numeroCpe','fechaCpe','totalCpe','XmlCpe','tipocpeId','emisorId', 'receptorId','fechapublicacionCpe','monedaCpe','fechavencCpe','usuId'] 
    def update(self):
        self.instance.idCdr = self.validated_data.get('idCdr', self.instance.idCdr) 
        self.instance.fechaCdr = self.validated_data.get('fechaCdr', self.instance.idCdr) 
        self.instance.horaCdr = self.validated_data.get('horaCdr', self.instance.idCdr) 
        self.instance.statusCdr = self.validated_data.get('statusCdr', self.instance.idCdr) 
        self.instance.estadoId = self.validated_data.get('estadoId', self.instance.idCdr) 
        self.instance.mensajeCdr = self.validated_data.get('mensajeCdr', self.instance.idCdr) 
        self.instance.CdrCpe = self.validated_data.get('CdrCpe', self.instance.CdrCpe) 
        self.instance.save()
        return self.instance

class ActualizacionResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumenModel
        exclude = ['ID','emisorId','fechaemisionresumen','fechageneracionresumen','fechapublicacionresumen','XmlCpe',  'PdfCpe','tipocpeId','usuId','ticketresumen'] 
    def update(self):
        self.instance.idCdr = self.validated_data.get('idCdr', self.instance.idCdr) 
        self.instance.fechaCdr = self.validated_data.get('fechaCdr', self.instance.idCdr) 
        self.instance.horaCdr = self.validated_data.get('horaCdr', self.instance.idCdr) 
        self.instance.statusCdr = self.validated_data.get('statusCdr', self.instance.idCdr) 
        self.instance.estadoId = self.validated_data.get('estadoId', self.instance.idCdr) 
        self.instance.mensajeCdr = self.validated_data.get('mensajeCdr', self.instance.idCdr) 
        self.instance.CdrCpe = self.validated_data.get('CdrCpe', self.instance.CdrCpe) 
        self.instance.save()
        return self.instance

class EmisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmisorModel
        fields = '__all__' 

class ReceptorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceptorModel
        fields = '__all__' 

class TipoCPESerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCPEModel
        fields = '__all__' 

class TipoDOCSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDOCModel
        fields = '__all__' 

class CPESerializer(serializers.ModelSerializer):
    class Meta:
        model = CPEModel
        fields = '__all__' 

class CPEResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPEResumenModel
        fields = '__all__' 

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoModel
        fields = '__all__' 

class CPEListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPEModel
        exclude = ['createAt','updateAt', 'emisorId','XmlCpe','PdfCpe','CdrCpe','idCdr','fechaCdr','horaCdr']