from django.db import models
from django.utils import timezone


class UsuarioModel(models.Model):
    usuId = models.AutoField(
        db_column='usu_id', primary_key=True, unique=True, null=False)
    usuCorreo = models.EmailField(db_column='usu_correo', unique=True)
    usuNombre = models.CharField(
        db_column='usu_nombre', null=True, max_length=50)
    usuCel = models.CharField(db_column='usu_cel', default='', max_length=13)
    password = models.TextField(db_column='usu_pass')

    class Meta:
        db_table = 't_usuario'


class TipoCPEModel(models.Model):
    tipocpeId = models.AutoField(
        db_column='tipocpe_id', primary_key=True, unique=True, null=False)
    tipocpeDesc = models.CharField(db_column='tipocpe_desc', max_length=50)
    tipocpeCod = models.CharField(db_column='tipocpe_cod', max_length=3)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 't_tipocpe'


class TipoDOCModel(models.Model):
    tipodocId = models.AutoField(
        db_column='tipodoc_id', primary_key=True, unique=True, null=False)
    tipodocDesc = models.CharField(db_column='tipodoc_desc', max_length=50)
    tipodocCod = models.CharField(db_column='tipodoc_cod', max_length=3)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 't_tipodoc'


class EstadoModel(models.Model):
    estadoId = models.AutoField(
        db_column='estado_id', primary_key=True, unique=True, null=False)
    estadoDesc = models.CharField(db_column='estado_desc', max_length=30)
    estadoCod = models.CharField(db_column='estado_cod', max_length=3)
    estadoTipo = models.CharField(db_column='estado_tipo', max_length=3)
    estadoCond = models.CharField(db_column='estado_cond', max_length=3)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 't_estado'


class SucursalModel(models.Model):
    sucursalId = models.AutoField(
        db_column='sucursal_id', primary_key=True, unique=True, null=False)
    sucursalDesc = models.CharField(db_column='sucursal_desc', max_length=50)
    sucursalCod = models.CharField(db_column='sucursal_cod', max_length=3)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 't_sucursal'


class EmisorModel(models.Model):
    emisorId = models.AutoField(
        db_column='emisor_id', primary_key=True, unique=True, null=False)
    emisorNroDoc = models.CharField(db_column='emisor_nrodoc', max_length=20)
    emisorRazonSocial = models.CharField(
        db_column='emisor_razonsocial', max_length=100)
    emisorUsuarioSunat = models.CharField(
        db_column='emisor_usuariosunat', max_length=20)
    emisorClaveSunat = models.CharField(
        db_column='emisor_clavesunat', max_length=20)
    emisorClave = models.CharField(db_column='emisor_clave', max_length=50)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 't_emisor'

# Create your models here.


class EmisorUsuarioModel(models.Model):
    emisorusuarioId = models.AutoField(
        db_column='emisorusuario_id', primary_key=True, unique=True, null=False)
    emisorId = models.ForeignKey(
        EmisorModel, on_delete=models.PROTECT, db_column='emisor_id')
    usuId = models.ForeignKey(UsuarioModel, on_delete=models.PROTECT,
                              db_column='usu_id', related_name='UsuarioEmisor')
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 't_emisorusuario'


class ReceptorModel(models.Model):
    receptorId = models.AutoField(
        db_column='receptor_id', primary_key=True, unique=True, null=False)
    tipodocId = models.ForeignKey(
        TipoDOCModel, on_delete=models.PROTECT, db_column='tipodoc_id')
    receptorNroDoc = models.CharField(
        db_column='receptor_nrodoc', max_length=20)
    receptorRazonSocial = models.CharField(
        db_column='receptor_razonsocial', max_length=100)

    class Meta:
        db_table = 't_receptor'


class CPEModel(models.Model):
    cpeId = models.AutoField(
        db_column='cpe_id', primary_key=True, unique=True, null=False)
    serieCpe = models.CharField(db_column='cpe_serie', max_length=4, null=True)
    numeroCpe = models.CharField(
        db_column='cpe_numero', max_length=8, null=True)
    fechaCpe = models.DateField(db_column='cpe_fecha', null=True)
    fechavencCpe = models.DateField(db_column='cpe_fechavenc', null=True)
    totalCpe = models.DecimalField(
        db_column='cpe_total', max_digits=14, decimal_places=2, null=True)
    importeCpe = models.DecimalField(
        db_column='cpe_immporte', max_digits=14, decimal_places=2, null=True)
    fechapublicacionCpe = models.DateTimeField(
        db_column='cpe_fechapublicacion', null=True)
    monedaCpe = models.CharField(
        db_column='cpe_moneda', max_length=8, null=True)

    serierefCpe = models.CharField(
        db_column='cpe_serieref', max_length=4, null=True)
    numerorefCpe = models.CharField(
        db_column='cpe_numeroref', max_length=8, null=True)
    fecharefCpe = models.DateField(db_column='cpe_fecharef', null=True)
    tipocperefId = models.ForeignKey(
        TipoCPEModel, on_delete=models.PROTECT, db_column='tipocperef_id', null=True)

    XmlCpe = models.TextField(db_column='cpe_xml', null=True)
    CdrCpe = models.TextField(db_column='cpe_cdr', null=True)
    PdfCpe = models.TextField(db_column='cpe_pdf', null=True)

    idCdr = models.CharField(db_column='cdr_id', max_length=20, null=True)
    fechaCdr = models.DateField(db_column='cdr_fecha', null=True)
    horaCdr = models.CharField(db_column='cdr_hora', max_length=10, null=True)
    statusCdr = models.CharField(
        db_column='cdr_status', max_length=5, null=True)
    mensajeCdr = models.TextField(db_column='cdr_mensaje', null=True)

    tipocpeId = models.ForeignKey(
        TipoCPEModel, on_delete=models.PROTECT, db_column='tipocpe_id', related_name='TipoCpeCpe')
    emisorId = models.ForeignKey(
        EmisorModel, on_delete=models.PROTECT, db_column='emisor_id')
    receptorId = models.ForeignKey(
        ReceptorModel, on_delete=models.PROTECT, db_column='receptor_id')
    estadoId = models.ForeignKey(
        EstadoModel, on_delete=models.PROTECT, db_column='estado_id')
    sucursalId = models.ForeignKey(
        SucursalModel, on_delete=models.PROTECT, db_column='sucursal_id', null=True)
    usuId = models.ForeignKey(UsuarioModel, on_delete=models.PROTECT,
                              db_column='usu_id', related_name='UsuarioCpe')

    createAt = models.DateTimeField(db_column='created_at', auto_now_add=True)
    updateAt = models.DateTimeField(db_column='updated_at', auto_now=True)

    class Meta:
        db_table = 't_cpe'


class EventosCPEModel(models.Model):
    eventoscpeId = models.AutoField(
        db_column='eventoscpe_id', primary_key=True, unique=True, null=False)
    cpeId = models.ForeignKey(
        CPEModel, on_delete=models.PROTECT, db_column='cpe_id')
    descripcionEventosCpe = models.CharField(
        db_column='eventoscpe_descripcion', max_length=100)
    observacionEventosCpe = models.CharField(
        db_column='eventoscpe_observacion', max_length=2000)
    fechaEventosCpe = models.CharField(
        db_column='eventoscpe_fecha', max_length=100)

    class Meta:
        db_table = 't_eventoscpe'


class ResumenModel(models.Model):
    resumenId = models.AutoField(
        db_column='resumen_id', primary_key=True, unique=True, null=False)

    ID = models.CharField(db_column='ID', max_length=20)
    fechaemisionresumen = models.DateField(db_column='resumen_fechaemision')
    fechageneracionresumen = models.DateField(
        db_column='resumen_fechageneracion')
    fechapublicacionresumen = models.DateTimeField(
        db_column='resumen_fechapublicacion')
    ticketresumen = models.CharField(db_column='resumen_ticket', max_length=20)

    XmlCpe = models.TextField(db_column='resumen_xml')
    CdrCpe = models.TextField(db_column='resumen_cdr', null=True)
    PdfCpe = models.TextField(db_column='resumen_pdf', null=True)
    idCdr = models.CharField(db_column='cdr_id', max_length=20)
    fechaCdr = models.DateField(db_column='cdr_fecha', null=True)
    horaCdr = models.CharField(db_column='cdr_hora', max_length=10, null=True)
    statusCdr = models.CharField(
        db_column='cdr_status', max_length=5, null=True)
    mensajeCdr = models.TextField(db_column='cdr_mensaje', null=True)

    tipocpeId = models.ForeignKey(
        TipoCPEModel, on_delete=models.PROTECT, db_column='tipocpe_id')
    emisorId = models.ForeignKey(
        EmisorModel, on_delete=models.PROTECT, db_column='emisor_id')
    estadoId = models.ForeignKey(
        EstadoModel, on_delete=models.PROTECT, db_column='estado_id')
    usuId = models.ForeignKey(UsuarioModel, on_delete=models.PROTECT,
                              db_column='usu_id', related_name='UsuarioResumen')

    createAt = models.DateTimeField(db_column='created_at', auto_now_add=True)
    updateAt = models.DateTimeField(db_column='updated_at', auto_now=True)

    class Meta:
        db_table = 't_resumen'


class EventosResumenModel(models.Model):
    eventosresumenId = models.AutoField(
        db_column='eventosresumen_id', primary_key=True, unique=True, null=False)
    resumenId = models.ForeignKey(
        ResumenModel, on_delete=models.PROTECT, db_column='resumen_id')
    descripcionEventosCpe = models.CharField(
        db_column='eventoscpe_descripcion', max_length=100)
    observacionEventosCpe = models.CharField(
        db_column='eventoscpe_observacion', max_length=2000)
    fechaEventosCpe = models.CharField(
        db_column='eventoscpe_fecha', max_length=100)

    class Meta:
        db_table = 't_eventosresumen'


class CPEResumenModel(models.Model):
    cperesumenId = models.AutoField(
        db_column='cperesumen_id', primary_key=True, unique=True, null=False)
    resumenId = models.ForeignKey(
        ResumenModel, on_delete=models.PROTECT, db_column='resumen_id')
    serierefCpe = models.CharField(
        db_column='cperesumen_serieref', max_length=4, null=True)
    numerorefCpe = models.CharField(
        db_column='cperesumen_numeroref', max_length=8, null=True)
    tipocperefId = models.ForeignKey(
        TipoCPEModel, on_delete=models.PROTECT, db_column='tipocperef_id', null=True)

    class Meta:
        db_table = 't_cperesumen'
