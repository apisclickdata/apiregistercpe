from typing import List
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.response import Response
from werkzeug.utils import secure_filename
from datetime import datetime
from .models import CPEModel, EmisorModel, TipoCPEModel, ReceptorModel, TipoDOCModel, EstadoModel, ResumenModel, CPEResumenModel
from .serializers import RegistroCPESerializer, ReceptorSerializer, ActualizacionCPESerializer, TipoCPESerializer, TipoDOCSerializer, CPESerializer, EmisorSerializer, RegistroResumenSerializer, ActualizacionTicketSerializer, ActualizacionResumenSerializer, CPEResumenSerializer, EstadoSerializer, CPEListSerializer
import xmltodict
from botocore.exceptions import ClientError
import boto3
from django.core.files.storage import FileSystemStorage
import os
from .switch import switch

from django.db import connection

os.environ["AWS_ACCESS_KEY_ID"] = "AKIATWLBE4BJTSDWSMUY"
os.environ["AWS_SECRET_ACCESS_KEY"] = "ruc9NdIjJG6KH4f6vRBBWfYQbavmINvDfbIZKh1Z"
bucketaws = 'clickdata'

# Create your views here.


class RegistroCPEView(CreateAPIView):
    queryset = CPEModel.objects.all()
    serializer_class = RegistroCPESerializer

    def post(self, request):
        try:
            #  and ("application/xml" in request.FILES["xml"].content_type)
            if (("xml" in request.FILES) and (request.FILES["xml"])):
                # and ("application/pdf" in request.FILES["pdf"].content_type)
                if (("pdf" in request.FILES) and (request.FILES["pdf"])):
                    fs = FileSystemStorage()
                    s3 = boto3.client('s3')
                    fecha = str(datetime.now().timestamp()).replace('.', '')

                    xml = request.FILES['xml']
                    pdf = request.FILES['pdf']

                    cpe = xmltodict.parse(xml.read())

                    nombreXml = secure_filename(fecha + '-' + xml.name)
                    fs.save('staticfiles/' + nombreXml, xml)

                    nombrePdf = secure_filename(fecha + '-' + pdf.name)
                    fs.save('staticfiles/' + nombrePdf, pdf)

                    tipoDocString = ''
                    for item in cpe:
                        tipoDocString = item

                    # Datos Generales
                    seriecpe = cpe[tipoDocString]['cbc:ID'].split('-')[0]
                    numerocpe = cpe[tipoDocString]['cbc:ID'].split('-')[1]
                    fechacpe = cpe[tipoDocString]['cbc:IssueDate']

                    importecpe = ''
                    tipocpe = ''

                    with switch(tipoDocString) as s:
                        if s.case('Invoice', True):
                            tipocpe = cpe[tipoDocString]['cbc:InvoiceTypeCode']['#text']
                            monedacpe = cpe[tipoDocString]['cbc:DocumentCurrencyCode']['#text']
                            importecpe = cpe[tipoDocString]['cac:LegalMonetaryTotal']['cbc:PayableAmount']['#text']

                            nrodocemisor = cpe[tipoDocString]['cac:AccountingSupplierParty'][
                                'cac:Party']['cac:PartyIdentification']['cbc:ID']['#text']
                            nrodocreceptor = cpe[tipoDocString]['cac:AccountingCustomerParty'][
                                'cac:Party']['cac:PartyIdentification']['cbc:ID']['#text']
                            tipodocreceptor = cpe[tipoDocString]['cac:AccountingCustomerParty'][
                                'cac:Party']['cac:PartyIdentification']['cbc:ID']['@schemeID']
                            razonsocialreceptor = cpe[tipoDocString]['cac:AccountingCustomerParty'][
                                'cac:Party']['cac:PartyLegalEntity']['cbc:RegistrationName']
                        if s.case('CreditNote', True):

                            tipocpe = cpe[tipoDocString]['cbc:CreditNoteTypeCode']['#text']
                            monedacpe = cpe[tipoDocString]['cbc:DocumentCurrencyCode']['#text']
                            importecpe = cpe[tipoDocString]['cac:LegalMonetaryTotal']['cbc:PayableAmount']['#text']

                            nrodocemisor = cpe[tipoDocString]['cac:AccountingSupplierParty'][
                                'cac:Party']['cac:PartyIdentification']['cbc:ID']['#text']
                            nrodocreceptor = cpe[tipoDocString]['cac:AccountingCustomerParty'][
                                'cac:Party']['cac:PartyIdentification']['cbc:ID']['#text']
                            tipodocreceptor = cpe[tipoDocString]['cac:AccountingCustomerParty'][
                                'cac:Party']['cac:PartyIdentification']['cbc:ID']['@schemeID']
                            razonsocialreceptor = cpe[tipoDocString]['cac:AccountingCustomerParty'][
                                'cac:Party']['cac:PartyLegalEntity']['cbc:RegistrationName']

                            serierefCpe = cpe[tipoDocString]['cac:BillingReference']['cac:InvoiceDocumentReference']['cbc:ID'].split(
                                '-')[0]
                            numerorefCpe = cpe[tipoDocString]['cac:BillingReference']['cac:InvoiceDocumentReference']['cbc:ID'].split(
                                '-')[1]
                            tipocperef = cpe[tipoDocString]['cac:BillingReference'][
                                'cac:InvoiceDocumentReference']['cbc:DocumentTypeCode']['#text']
                            tipocperefId = TipoCPEModel.objects.get(
                                tipocpeCod=tipocperef).tipocpeId
                        if s.case('DebitNote', True):
                            tipocpe = '08'
                            monedacpe = cpe[tipoDocString]['cbc:DocumentCurrencyCode']['#text']
                            importecpe = cpe[tipoDocString]['cac:RequestedMonetaryTotal']['cbc:PayableAmount']['#text']

                            nrodocemisor = cpe[tipoDocString]['cac:AccountingSupplierParty'][
                                'cac:Party']['cac:PartyIdentification']['cbc:ID']['#text']
                            nrodocreceptor = cpe[tipoDocString]['cac:AccountingCustomerParty'][
                                'cac:Party']['cac:PartyIdentification']['cbc:ID']['#text']
                            tipodocreceptor = cpe[tipoDocString]['cac:AccountingCustomerParty'][
                                'cac:Party']['cac:PartyIdentification']['cbc:ID']['@schemeID']
                            razonsocialreceptor = cpe[tipoDocString]['cac:AccountingCustomerParty'][
                                'cac:Party']['cac:PartyLegalEntity']['cbc:RegistrationName']
                        if s.case('DespatchAdvice', True):
                            monedacpe = '-'
                            tipocpe = cpe[tipoDocString]['cbc:DespatchAdviceTypeCode']
                            importecpe = 0.00

                            nrodocemisor = cpe[tipoDocString]['cac:DespatchSupplierParty']['cbc:CustomerAssignedAccountID']['#text']
                            nrodocreceptor = cpe[tipoDocString]['cac:DeliveryCustomerParty']['cbc:CustomerAssignedAccountID']['#text']
                            tipodocreceptor = cpe[tipoDocString]['cac:DeliveryCustomerParty'][
                                'cbc:CustomerAssignedAccountID']['@schemeID']
                            razonsocialreceptor = cpe[tipoDocString]['cac:DeliveryCustomerParty'][
                                'cac:Party']['cac:PartyLegalEntity']['cbc:RegistrationName']

                        if s.case('Retention', True):
                            tipocpe = '20'
                            monedacpe = cpe[tipoDocString]['cbc:TotalInvoiceAmount']['@currencyID']
                            importecpe = cpe[tipoDocString]['cbc:TotalInvoiceAmount']['#text']

                            nrodocemisor = cpe[tipoDocString]['cac:AgentParty']['cac:PartyIdentification']['cbc:ID']['#text']
                            nrodocreceptor = cpe[tipoDocString]['cac:ReceiverParty']['cac:PartyIdentification']['cbc:ID']['#text']
                            tipodocreceptor = cpe[tipoDocString]['cac:ReceiverParty'][
                                'cac:PartyIdentification']['cbc:ID']['@schemeID']
                            razonsocialreceptor = cpe[tipoDocString]['cac:ReceiverParty'][
                                'cac:PartyLegalEntity']['cbc:RegistrationName']

                        if s.case('Perception', True):
                            tipocpe = '40'
                            monedacpe = cpe[tipoDocString]['cbc:TotalInvoiceAmount']['@currencyID']
                            importecpe = cpe[tipoDocString]['cbc:TotalInvoiceAmount']['#text']

                            nrodocemisor = cpe[tipoDocString]['cac:AgentParty']['cac:PartyIdentification']['cbc:ID']['#text']
                            nrodocreceptor = cpe[tipoDocString]['cac:ReceiverParty']['cac:PartyIdentification']['cbc:ID']['#text']
                            tipodocreceptor = cpe[tipoDocString]['cac:ReceiverParty'][
                                'cac:PartyIdentification']['cbc:ID']['@schemeID']
                            razonsocialreceptor = cpe[tipoDocString]['cac:ReceiverParty'][
                                'cac:PartyLegalEntity']['cbc:RegistrationName']
                        if s.default():
                            tipocpe = -1

                    emisorId = EmisorModel.objects.get(
                        emisorNroDoc=nrodocemisor).emisorId

                    tipocpeId = TipoCPEModel.objects.get(
                        tipocpeCod=tipocpe).tipocpeId
                    tipodocId = TipoDOCModel.objects.get(
                        tipodocCod=tipodocreceptor).tipodocId
                    estadoId = EstadoModel.objects.get(estadoCod='01').estadoId

                    dicReceptor = dict()
                    dicReceptor.setdefault('tipodocId', tipodocId)
                    dicReceptor.setdefault('receptorNroDoc', nrodocreceptor)
                    dicReceptor.setdefault(
                        'receptorRazonSocial', razonsocialreceptor)

                    cpeVal = []
                    try:
                        cpeVal = self.get_queryset().filter(
                            serieCpe=seriecpe, numeroCpe=numerocpe, emisorId=emisorId).first()
                    except:
                        print('Se procede al registro del CPE')

                    if not cpeVal:
                        receptor = []
                        try:
                            receptor = ReceptorModel.objects.get(
                                receptorNroDoc=nrodocreceptor, tipodocId=tipodocId, receptorRazonSocial=razonsocialreceptor)
                        except:
                            print('Se procede al registro del Receptor')

                        if not receptor:
                            # Crear Receptor
                            receptorCreado = ReceptorSerializer(
                                data=dicReceptor)
                            if receptorCreado.is_valid(raise_exception=True):
                                receptorCreado.save()
                            receptor = ReceptorModel.objects.get(
                                receptorNroDoc=nrodocreceptor, tipodocId=tipodocId)

                        receptorId = receptor.receptorId

                        # Crear CPE
                        dicCpe = dict()
                        dicCpe.setdefault('serieCpe', seriecpe)
                        dicCpe.setdefault('numeroCpe', numerocpe)
                        dicCpe.setdefault('fechaCpe', fechacpe)
                        dicCpe.setdefault('totalCpe', importecpe)
                        dicCpe.setdefault('importeCpe', importecpe)
                        dicCpe.setdefault('tipocpeId', tipocpeId)
                        dicCpe.setdefault('emisorId', emisorId)
                        dicCpe.setdefault('receptorId', receptorId)
                        dicCpe.setdefault('estadoId', estadoId)

                        if ((tipoDocString == 'CreditNote') or (tipoDocString == 'DebitNote')):
                            dicCpe.setdefault('serierefCpe', serierefCpe)
                            dicCpe.setdefault('numerorefCpe', numerorefCpe)
                            dicCpe.setdefault('tipocperefId', tipocperefId)

                        dicCpe.setdefault(
                            'fechapublicacionCpe', datetime.now())
                        dicCpe.setdefault('monedaCpe', monedacpe)
                        dicCpe.setdefault('fechavencCpe', fechacpe)
                        dicCpe.setdefault('usuId', 1)

                        print(dicCpe)

                        try:
                            # Guardar el XML en S3
                            s3.upload_file('staticfiles/' + nombreXml, bucketaws +
                                           'cpe', nombreXml, ExtraArgs={'ACL': 'public-read'})
                            fs.delete(nombreXml)
                            # Guardar el PDF en S3
                            s3.upload_file('staticfiles/' + nombrePdf, bucketaws +
                                           'pdf',  nombrePdf, ExtraArgs={'ACL': 'public-read'})
                            fs.delete(nombrePdf)

                            dicCpe.setdefault(
                                'XmlCpe', 'https://'+bucketaws+'cpe.s3.us-east-2.amazonaws.com/' + nombreXml)
                            dicCpe.setdefault(
                                'PdfCpe', 'https://'+bucketaws+'pdf.s3.us-east-2.amazonaws.com/' + nombrePdf)

                            respuesta = self.get_serializer(data=dicCpe)
                            if respuesta.is_valid(raise_exception=True):

                                respuesta.save()
                                return Response({
                                    'status': True,
                                    'content': respuesta.data,
                                    'message': 'El CPE fue registrado correctamente'
                                }, status=201)
                            else:
                                return Response({
                                    'status': False,
                                    'content': None,
                                    'message': 'Ocurrió  un error al registrar el CPE'
                                }, status=400)

                        except ClientError as e:
                            return Response({
                                'status': False,
                                'content': None,
                                'message': 'Ocurrió  un error al registrar el XML o PDF del CPE'
                            }, status=400)
                    else:
                        fs.delete(nombreXml)
                        fs.delete(nombrePdf)
                        return Response({
                            'status': False,
                            'content': None,
                            'message': 'El CPE ya se encuentra registrado'
                        }, status=400)
                else:
                    return Response({
                        'status': False,
                        'content': None,
                        'message': 'No se envió el PDF del CPE'
                    }, status=400)
            else:
                return Response({
                    'status': False,
                    'content': None,
                    'message': 'No se envió el XML del CPE'
                }, status=400)
        except expression as error:
            return Response({
                'status': False,
                'content': None,
                'message': 'Ocurrió un error en el registro: {0}'.format(error)
            }, status=400)

# Create your views here.


class RegistroResumenView(CreateAPIView):
    queryset = ResumenModel.objects.all()
    serializer_class = RegistroResumenSerializer

    def post(self, request):
        try:
            #  and ("application/xml" in request.FILES["xml"].content_type)
            if (("xml" in request.FILES) and (request.FILES["xml"])):
                # and ("application/pdf" in request.FILES["pdf"].content_type)
                if (("pdf" in request.FILES) and (request.FILES["pdf"])):
                    fs = FileSystemStorage()
                    s3 = boto3.client('s3')
                    fecha = str(datetime.now().timestamp()).replace('.', '')

                    xml = request.FILES['xml']
                    pdf = request.FILES['pdf']

                    cpe = xmltodict.parse(xml.read())

                    nombreXml = secure_filename(fecha + '-' + xml.name)
                    fs.save('staticfiles/' + nombreXml, xml)

                    nombrePdf = secure_filename(fecha + '-' + pdf.name)
                    fs.save('staticfiles/' + nombrePdf, pdf)

                    tipoDocString = ''
                    for item in cpe:
                        tipoDocString = item

                    # Datos Generales
                    ID = cpe[tipoDocString]['cbc:ID']
                    fechaemisionresumen = cpe[tipoDocString]['cbc:IssueDate']
                    fechageneracionresumen = cpe[tipoDocString]['cbc:ReferenceDate']

                    tipocpe = cpe[tipoDocString]['cbc:ID'].split('-')[0]
                    nrodocemisor = cpe[tipoDocString]['cac:AccountingSupplierParty']['cbc:CustomerAssignedAccountID']

                    emisorId = EmisorModel.objects.get(
                        emisorNroDoc=nrodocemisor).emisorId
                    tipocpeId = TipoCPEModel.objects.get(
                        tipocpeCod=tipocpe).tipocpeId
                    estadoId = EstadoModel.objects.get(estadoCod='01').estadoId

                    cpeVal = []
                    try:
                        cpeVal = self.get_queryset().filter(ID=ID, emisorId=emisorId).first()
                    except:
                        print('No existe el CPE')

                    if not cpeVal:
                        # Crear Resumen
                        dicCpe = dict()
                        dicCpe.setdefault('ID', ID)
                        dicCpe.setdefault(
                            'fechaemisionresumen', fechaemisionresumen)
                        dicCpe.setdefault(
                            'fechageneracionresumen', fechageneracionresumen)
                        dicCpe.setdefault('tipocpeId', tipocpeId)
                        dicCpe.setdefault('emisorId', emisorId)
                        dicCpe.setdefault('estadoId', estadoId)
                        dicCpe.setdefault(
                            'fechapublicacionresumen', datetime.now())
                        dicCpe.setdefault('usuId', 1)

                        try:
                            # Guardar el XML en S3
                            s3.upload_file('staticfiles/' + nombreXml, bucketaws +
                                           'cpe', nombreXml, ExtraArgs={'ACL': 'public-read'})
                            fs.delete(nombreXml)
                            # Guardar el PDF en S3
                            s3.upload_file('staticfiles/' + nombrePdf, bucketaws +
                                           'pdf', nombrePdf, ExtraArgs={'ACL': 'public-read'})
                            fs.delete(nombrePdf)

                            dicCpe.setdefault(
                                'XmlCpe', 'https://'+bucketaws+'cpe.s3.us-east-2.amazonaws.com/' + nombreXml)
                            dicCpe.setdefault(
                                'PdfCpe', 'https://'+bucketaws+'pdf.s3.us-east-2.amazonaws.com/' + nombrePdf)

                            respuesta = self.get_serializer(data=dicCpe)
                            if respuesta.is_valid(raise_exception=True):
                                resumen = respuesta.save()

                                if (tipocpe == 'RC'):
                                    detalle = cpe[tipoDocString]['sac:SummaryDocumentsLine']

                                    if isinstance(detalle, List):
                                        # El CPE tiene más de 1 detalle
                                        for item in detalle:
                                            tipocpeId = TipoCPEModel.objects.get(
                                                tipocpeCod=item['cbc:DocumentTypeCode']).tipocpeId
                                            dicCPE = dict()
                                            dicCPE.setdefault(
                                                'resumenId', resumen.resumenId)
                                            dicCPE.setdefault(
                                                'serierefCpe', item['cbc:ID'].split('-')[0])
                                            dicCPE.setdefault(
                                                'numerorefCpe', item['cbc:ID'].split('-')[1])
                                            dicCPE.setdefault(
                                                'tipocperefId', tipocpeId)
                                            cpeCreado = CPEResumenSerializer(
                                                data=dicCPE)
                                            if cpeCreado.is_valid(raise_exception=True):
                                                cpeCreado.save()
                                    else:
                                        # El CPE solo tiene 1 detalle
                                        tipocpeId = TipoCPEModel.objects.get(
                                            tipocpeCod=detalle['cbc:DocumentTypeCode']).tipocpeId
                                        dicCPE = dict()
                                        dicCPE.setdefault(
                                            'resumenId', resumen.resumenId)
                                        dicCPE.setdefault(
                                            'serierefCpe', detalle['cbc:ID'].split('-')[0])
                                        dicCPE.setdefault(
                                            'numerorefCpe', detalle['cbc:ID'].split('-')[1])
                                        dicCPE.setdefault(
                                            'tipocperefId', tipocpeId)

                                        cpeCreado = CPEResumenSerializer(
                                            data=dicCPE)
                                        if cpeCreado.is_valid(raise_exception=True):
                                            cpeCreado.save()

                                if (tipocpe == 'RA'):
                                    detalle = cpe[tipoDocString]['sac:VoidedDocumentsLine']

                                    if isinstance(detalle, List):
                                        # El CPE tiene más de 1 detalle
                                        for item in detalle:
                                            tipocpeId = TipoCPEModel.objects.get(
                                                tipocpeCod=item['cbc:DocumentTypeCode']).tipocpeId
                                            dicCPE = dict()
                                            dicCPE.setdefault(
                                                'resumenId', resumen.resumenId)
                                            dicCPE.setdefault(
                                                'serierefCpe', item['sac:DocumentSerialID'])
                                            dicCPE.setdefault(
                                                'numerorefCpe', item['sac:DocumentNumberID'])
                                            dicCPE.setdefault(
                                                'tipocperefId', tipocpeId)
                                            cpeCreado = CPEResumenSerializer(
                                                data=dicCPE)
                                            if cpeCreado.is_valid(raise_exception=True):
                                                cpeCreado.save()
                                    else:
                                        # El CPE solo tiene 1 detalle
                                        tipocpeId = TipoCPEModel.objects.get(
                                            tipocpeCod=detalle['cbc:DocumentTypeCode']).tipocpeId
                                        dicCPE = dict()
                                        dicCPE.setdefault(
                                            'resumenId', resumen.resumenId)
                                        dicCPE.setdefault(
                                            'serierefCpe', detalle['sac:DocumentSerialID'])
                                        dicCPE.setdefault(
                                            'numerorefCpe', detalle['sac:DocumentNumberID'])
                                        dicCPE.setdefault(
                                            'tipocperefId', tipocpeId)

                                        cpeCreado = CPEResumenSerializer(
                                            data=dicCPE)
                                        if cpeCreado.is_valid(raise_exception=True):
                                            cpeCreado.save()

                                return Response({
                                    'status': True,
                                    'content': respuesta.data,
                                    'message': 'El Resumen fue registrado correctamente'
                                }, status=201)
                            else:
                                return Response({
                                    'status': False,
                                    'content': None,
                                    'message': 'Ocurrió  un error al registrar el Resumen'
                                }, status=400)

                        except ClientError as e:
                            return Response({
                                'status': False,
                                'content': None,
                                'message': 'Ocurrió  un error al registrar el XML o PDF del Resumen'
                            }, status=400)
                    else:
                        fs.delete(nombreXml)
                        fs.delete(nombrePdf)
                        return Response({
                            'status': False,
                            'content': None,
                            'message': 'El Resumen ya se encuentra registrado'
                        }, status=400)
                else:
                    return Response({
                        'status': False,
                        'content': None,
                        'message': 'No se envió el PDF del Resumen'
                    }, status=400)
            else:
                return Response({
                    'status': False,
                    'content': None,
                    'message': 'No se envió el XML del Resumen'
                }, status=400)
        except expression as error:
            return Response({
                'status': False,
                'content': None,
                'message': 'Ocurrió un error en el registro: {0}'.format(error)
            }, status=400)


class ActualizaTicketView(CreateAPIView):
    queryset = ResumenModel.objects.all()
    serializer_class = ActualizacionTicketSerializer

    def put(self, request):
        try:
            ID = request.data.get('ID')
            emisorNroDoc = request.data.get('emisorNroDoc')
            ticketresumen = request.data.get('ticketresumen')
            infoCpe = ID.split('-')
            tipocpe = infoCpe[0]

            emisorId = EmisorModel.objects.get(
                emisorNroDoc=emisorNroDoc).emisorId
            tipocpeId = TipoCPEModel.objects.get(tipocpeCod=tipocpe).tipocpeId

            cpeVal = []
            try:
                cpeVal = self.get_queryset().filter(
                    ID=ID, emisorId=emisorId, tipocpeId=tipocpeId).first()
            except ValueError:
                return Response({
                    'status': False,
                    'content': None,
                    'message': 'No existe el Resumen'
                }, status=400)

            # Actualizar Resumen
            dicCpe = dict()
            dicCpe.setdefault('ticketresumen', ticketresumen)

            respuesta = self.serializer_class(cpeVal, data=dicCpe)
            if respuesta.is_valid(raise_exception=True):
                resultado = respuesta.update()
                return Response({
                    'status': True,
                    'content': respuesta.data,
                    'message': 'El Resumen fue actualizado correctamente'
                }, status=200)
            else:
                return Response({
                    'status': False,
                    'content': None,
                    'message': 'Ocurrió  un error al actualizar el Resumen'
                }, status=400)

        except expression as error:
            return Response({
                'status': False,
                'content': None,
                'message': 'Ocurrió un error en el registro: {0}'.format(error)
            }, status=400)


class ActualizacionCPEView(CreateAPIView):
    queryset = CPEModel.objects.all()
    serializer_class = ActualizacionCPESerializer

    def put(self, request, idCpe):
        if (("cdr" in request.FILES) and (request.FILES["cdr"])):
            fs = FileSystemStorage()
            s3 = boto3.client('s3')
            xml = request.FILES['cdr']
            cpe = xmltodict.parse(xml.read())
            fecha = str(datetime.now().timestamp()).replace('.', '')
            nombre_seguro = secure_filename(fecha + '-' + xml.name)

            fs.save('staticfiles/' + nombre_seguro, xml)

            infoCpe = idCpe.split('-')
            emisorNroDoc = infoCpe[0]
            tipocpe = infoCpe[1]
            seriecpe = infoCpe[2]
            numerocpe = infoCpe[3]

            tipocpeId = TipoCPEModel.objects.get(tipocpeCod=tipocpe).tipocpeId
            emisorId = EmisorModel.objects.get(
                emisorNroDoc=emisorNroDoc).emisorId

            estadoanulado = '02'
            estadoAnuladoId = EstadoModel.objects.get(
                estadoCod=estadoanulado).estadoId

            cpeVal = []
            try:
                cpeVal = self.get_queryset().filter(serieCpe=seriecpe, numeroCpe=numerocpe,
                                                    tipocpeId=tipocpeId, emisorId=emisorId).first()

                if ((tipocpe == '07') or (tipocpe == '08')):
                    cpeRef = self.get_queryset().filter(serieCpe=cpeVal.serierefCpe, numeroCpe=cpeVal.numerorefCpe,
                                                        tipocpeId=cpeVal.tipocperefId, emisorId=cpeVal.emisorId).first()

            except ValueError:
                return Response({
                    'status': False,
                    'content': None,
                    'message': 'No existe el comprobante'
                }, status=400)

            fechaCdr = cpe['ar:ApplicationResponse']['cbc:ResponseDate']
            mensajeCdr = cpe['ar:ApplicationResponse']['cac:DocumentResponse']['cac:Response']['cbc:Description']

            statusCdr = ''
            try:
                statusCdr = cpe['ar:ApplicationResponse']['cac:DocumentResponse']['cac:Response']['cbc:ResponseCode']
            except ValueError:
                print('No se recuperó el código de respuesta')

            print('statusCdr22222: ' + statusCdr)

            if (statusCdr == ''):
                statusCdr = cpe['ar:ApplicationResponse']['cac:DocumentResponse']['cac:Response']['cbc:ResponseCode']['#text']

            print('fechaCdr: ' + fechaCdr)
            print('statusCdr: ' + statusCdr)
            print('mensajeCdr: ' + mensajeCdr)

            if (statusCdr == '0'):
                idCdr = cpe['ar:ApplicationResponse']['cbc:ID']
                horaCdr = cpe['ar:ApplicationResponse']['cbc:ResponseTime']
            else:
                idCdr = '-'
                horaCdr = '-'

            codEstado = ''
            if (statusCdr == '0'):
                codEstado = statusCdr
            else:
                codEstado = '99'

            estadoId = EstadoModel.objects.get(estadoCod=codEstado).estadoId

            dicCdr = dict()
            dicCdr.setdefault('idCdr', idCdr[0:20])
            dicCdr.setdefault('fechaCdr', fechaCdr[0:10])
            dicCdr.setdefault('horaCdr', horaCdr[0:8])
            dicCdr.setdefault('statusCdr', statusCdr[0:5])
            dicCdr.setdefault('estadoId', estadoId)
            dicCdr.setdefault('mensajeCdr', mensajeCdr)

            try:
                s3.upload_file('staticfiles/' + nombre_seguro, bucketaws +
                               'cdr', nombre_seguro, ExtraArgs={'ACL': 'public-read'})
                fs.delete(nombre_seguro)
                dicCdr.setdefault('CdrCpe', 'https://'+bucketaws +
                                  'cdr.s3.us-east-2.amazonaws.com/' + nombre_seguro)

                respuesta = self.serializer_class(cpeVal, data=dicCdr)

                if respuesta.is_valid(raise_exception=True):

                    resultado = respuesta.update()

                    if ((tipocpe == '07') or (tipocpe == '08')):
                        CPEModel.objects.filter(cpeId=cpeRef.cpeId).update(
                            estadoId=estadoAnuladoId)

                    return Response({
                        'status': True,
                        'content': respuesta.data,
                        'message': 'El CPE fue actualizado correctamente'
                    }, status=200)
                else:
                    return Response({
                        'status': False,
                        'content': None,
                        'message': 'Ocurrió  un error al actualizar el CPE '
                    }, status=400)

            except ClientError as e:
                return Response({
                    'status': False,
                    'content': None,
                    'message': 'Ocurrió  un erro al registrar el CDR del CPE'
                }, status=400)

        else:
            return Response({
                'status': False,
                'content': None,
                'message': 'No se envió el CDR del CPE'
            }, status=400)


class ActualizacionResumenView(CreateAPIView):
    queryset = ResumenModel.objects.all()
    serializer_class = ActualizacionResumenSerializer

    def put(self, request, ID):
        if (("cdr" in request.FILES) and (request.FILES["cdr"])):
            fs = FileSystemStorage()
            s3 = boto3.client('s3')
            xml = request.FILES['cdr']
            cpe = xmltodict.parse(xml.read())
            fecha = str(datetime.now().timestamp()).replace('.', '')
            nombre_seguro = secure_filename(fecha + '-' + xml.name)
            fs.save('staticfiles/' + nombre_seguro, xml)

            infoCpe = ID.split('-')
            emisorNroDoc = infoCpe[0]
            tipocpe = infoCpe[1]
            IDResumen = infoCpe[1] + '-' + infoCpe[2] + '-' + infoCpe[3]

            estadoBaja = '03'
            estadoBajaId = EstadoModel.objects.get(
                estadoCod=estadoBaja).estadoId

            tipocpeId = TipoCPEModel.objects.get(tipocpeCod=tipocpe).tipocpeId
            emisorId = EmisorModel.objects.get(
                emisorNroDoc=emisorNroDoc).emisorId

            cpeVal = []
            try:
                cpeVal = self.get_queryset().filter(
                    ID=IDResumen, tipocpeId=tipocpeId, emisorId=emisorId).first()
            except ValueError:
                return Response({
                    'status': False,
                    'content': None,
                    'message': 'No existe el Resumen'
                }, status=400)

            fechaCdr = cpe['ar:ApplicationResponse']['cbc:ResponseDate']
            statusCdr = cpe['ar:ApplicationResponse']['cac:DocumentResponse']['cac:Response']['cbc:ResponseCode']
            mensajeCdr = cpe['ar:ApplicationResponse']['cac:DocumentResponse']['cac:Response']['cbc:Description']

            if (statusCdr == '0'):
                idCdr = cpe['ar:ApplicationResponse']['cbc:ID']
                horaCdr = cpe['ar:ApplicationResponse']['cbc:ResponseTime']
            else:
                idCdr = '-'
                horaCdr = '-'

            codEstado = ''
            if (statusCdr == '0'):
                codEstado = statusCdr
            else:
                codEstado = '99'

            estadoId = EstadoModel.objects.get(estadoCod=codEstado).estadoId

            dicCdr = dict()
            dicCdr.setdefault('idCdr', idCdr)
            dicCdr.setdefault('fechaCdr', fechaCdr[0:10])
            dicCdr.setdefault('horaCdr', horaCdr)
            dicCdr.setdefault('statusCdr', statusCdr)
            dicCdr.setdefault('estadoId', estadoId)
            dicCdr.setdefault('mensajeCdr', mensajeCdr)

            try:
                s3.upload_file('staticfiles/' + nombre_seguro, bucketaws +
                               'cdr', nombre_seguro, ExtraArgs={'ACL': 'public-read'})
                fs.delete(nombre_seguro)
                dicCdr.setdefault('CdrCpe', 'https://'+bucketaws +
                                  'cdr.s3.us-east-2.amazonaws.com/' + nombre_seguro)

                respuesta = self.serializer_class(cpeVal, data=dicCdr)
                if respuesta.is_valid(raise_exception=True):
                    resultado = respuesta.update()

                    for item in CPEResumenModel.objects.filter(resumenId=cpeVal.resumenId):
                        CPEModel.objects.filter(serieCpe=item.serierefCpe, numeroCpe=item.numerorefCpe,
                                                tipocpeId=item.tipocperefId, emisorId=emisorId).update(estadoId=estadoBajaId)

                    return Response({
                        'status': True,
                        'content': respuesta.data,
                        'message': 'El CPE fue actualizado correctamente'
                    }, status=200)
                else:
                    return Response({
                        'status': False,
                        'content': None,
                        'message': 'Ocurrió  un error al actualizar el CPE'
                    }, status=400)

            except ClientError as e:
                return Response({
                    'status': False,
                    'content': None,
                    'message': 'Ocurrió  un erro al registrar el CDR del CPE'
                }, status=400)

        else:
            return Response({
                'status': False,
                'content': None,
                'message': 'No se envió el CDR del CPE'
            }, status=400)


class TipoCPEView(ListCreateAPIView):
    queryset = TipoCPEModel.objects.all()
    serializer_class = TipoCPESerializer

    def get(self, request):
        respuesta = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'content':  respuesta.data,
            'message': None
        })


class TipoDOCView(ListCreateAPIView):
    queryset = TipoDOCModel.objects.all()
    serializer_class = TipoDOCSerializer

    def get(self, request):
        respuesta = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'content':  respuesta.data,
            'message': None
        })


class CPEView(ListCreateAPIView):
    queryset = CPEModel.objects.all()
    serializer_class = CPESerializer

    def get(self, request, rucEmisor, tipoDocReceptor, rucReceptor, tipoCpe, serieCpe, numeroCpe, fechaCpe, totalCpe):
        rucEmisor = rucEmisor
        tipoDocReceptor = tipoDocReceptor
        rucReceptor = rucReceptor
        tipoCpe = tipoCpe
        serieCpe = serieCpe
        numeroCpe = numeroCpe
        fechaCpe = fechaCpe
        totalCpe = totalCpe

        emisorId = 0
        try:
            emisorId = EmisorModel.objects.get(emisorNroDoc=rucEmisor).emisorId
        except:
            pass

        print(emisorId)

        receptorId = 0
        try:
            receptorId = ReceptorModel.objects.get(
                receptorNroDoc=rucReceptor, tipodocId=tipoDocReceptor).receptorId
        except:
            pass

        respuesta = self.get_queryset().filter(serieCpe=serieCpe, numeroCpe=numeroCpe,
                                               emisorId=emisorId, tipocpeId=tipoCpe, fechaCpe=fechaCpe, totalCpe=totalCpe).first()

        if respuesta:
            content = self.get_serializer(respuesta).data
            if content['idCdr'] != '':
                return Response({
                    'status': True,
                    'content':  content,
                    'message': None
                })
            else:
                return Response({
                    'status': False,
                    'content':  None,
                    'message': 'El Comprobante no existe'
                })
        else:
            return Response({
                'status': False,
                'content':  None,
                'message': 'El Comprobante no existe'
            })


class ValidarEmisorView(ListCreateAPIView):
    queryset = EmisorModel.objects.all()
    serializer_class = EmisorSerializer

    def get(self, request, rucEmisor, claveEmisor):

        rucEmisor = rucEmisor
        claveEmisor = claveEmisor

        emisorId = 0
        try:
            emisorId = EmisorModel.objects.get(
                emisorNroDoc=rucEmisor, emisorClave=claveEmisor, estado=1).emisorId
        except:
            pass

        if emisorId == 0:
            return Response({
                'status': False,
                'content':  None,
                'message': 'Emisor no habilitado'
            })
        else:
            return Response({
                'status': True,
                'content':  emisorId,
                'message': 'Emisor habilitado'
            })


class TipoCPEListView(ListCreateAPIView):
    serializer_class = TipoCPESerializer

    def get(self, request):
        cursor = connection.cursor()

        cursor.callproc('dbclickdata.sp_ObtenerTipoCPE')
        columns = [d[0] for d in cursor.description]

        records = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()

        if records:
            return Response({
                'content':  records
            }, 200)
        else:
            return Response({
                'status': False,
                'content':  None,
                'message': 'No existen datos'
            }, 404)


class EstadoListView(ListCreateAPIView):
    serializer_class = EstadoSerializer

    def get(self, request):
        cursor = connection.cursor()

        cursor.callproc('dbclickdata.sp_ObtenerEstados')
        columns = [d[0] for d in cursor.description]

        records = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()

        if records:
            return Response({
                'content':  records
            }, 200)
        else:
            return Response({
                'status': False,
                'content':  None,
                'message': 'No existen datos'
            }, 404)


class EmisorListView(ListCreateAPIView):
    queryset = EmisorModel.objects.all()
    serializer_class = EmisorSerializer

    def get(self, request):
        respuesta = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'content':  respuesta.data
        })


class CPEListView(ListCreateAPIView):
    serializer_class = CPEListSerializer

    def get(self, request, tipoCpe, estadoCpe, rucReceptor, serieCpe, numeroCpe, fechaDesde, fechaHasta, idEmisor):
        tipoCpe = tipoCpe
        estadoCpe = estadoCpe
        rucReceptor = rucReceptor
        serieCpe = serieCpe
        numeroCpe = numeroCpe
        fechaDesde = fechaDesde
        fechaHasta = fechaHasta
        idEmisor = idEmisor

        cursor = connection.cursor()

        param = (tipoCpe, estadoCpe, rucReceptor, serieCpe,
                 numeroCpe, fechaDesde, fechaHasta, idEmisor,)
        cursor.callproc('dbclickdata.sp_ObtenerCPE', param)
        columns = [d[0] for d in cursor.description]

        records = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()

        if records:
            return Response({
                'content':  records
            }, 200)
        else:
            return Response({
                'status': False,
                'content':  None,
                'message': 'No existen datos'
            }, 404)
