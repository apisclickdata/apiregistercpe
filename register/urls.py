from django.urls import path
from .views import RegistroCPEView, ActualizacionCPEView, TipoCPEView, TipoDOCView, CPEView, ValidarEmisorView, RegistroResumenView, ActualizaTicketView, ActualizacionResumenView, EmisorListView, EstadoListView, TipoCPEListView, CPEListView

urlpatterns = [
    path('registrarcpe', RegistroCPEView.as_view(), name='Registrar'),
    path('registraresumen', RegistroResumenView.as_view(), name='Registraresumen'),
    path('actualizarticket', ActualizaTicketView.as_view(), name='ActualizarTicket'),
    path('actualizarcpe/<str:idCpe>', ActualizacionCPEView.as_view(), name='Actualizar'),
    path('actualizarresumen/<str:ID>', ActualizacionResumenView.as_view(), name='ActualizarResumen'),
    path('tipocpe', TipoCPEView.as_view(), name='TipoCPE'),
    path('tipodoc', TipoDOCView.as_view(), name='TipoDOC'),
    path('emisorlist', EmisorListView.as_view(), name='EmisorList'),
    path('tipocpelist', TipoCPEListView.as_view(), name='TipoCPEList'),
    path('estadolist', EstadoListView.as_view(), name='EstadoList'),
    path('validaremisor/<str:rucEmisor>/<str:claveEmisor>/', ValidarEmisorView.as_view(), name='ValidarEmisor'),
    path('consultarcpe/<str:rucEmisor>/<int:tipoDocReceptor>/<str:rucReceptor>/<int:tipoCpe>/<str:serieCpe>/<str:numeroCpe>/<str:fechaCpe>/<str:totalCpe>', CPEView.as_view(), name='CPE'),
    path('consultarcpelist/<int:tipoCpe>/<int:estadoCpe>/<str:rucReceptor>/<str:serieCpe>/<str:numeroCpe>/<str:fechaDesde>/<str:fechaHasta>/<int:idEmisor>', CPEListView.as_view(), name='CPEList'),
]
 