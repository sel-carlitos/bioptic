# -*- coding: utf-8 -*-

from .MixedClass import GeneratedsSuper
from .MixedClass import showIndent
from .MixedClass import quote_xml
import re as re_
import sys

try:
    from lxml import etree as etree_
except ImportError:
    from xml.etree import ElementTree as etree_

Validate_simpletypes_ = True
if sys.version_info.major == 2:
    BaseStrType_ = basestring
else:
    BaseStrType_ = str

try:
    from generatedsnamespaces import GenerateDSNamespaceDefs as GenerateDSNamespaceDefs_
except ImportError:
    GenerateDSNamespaceDefs_ = {}

#
# Globals
#

ExternalEncoding = 'utf-8'
Tag_pattern_ = re_.compile(r'({.*})?(.*)')
String_cleanup_pat_ = re_.compile(r"[\n\r\s]+")
Namespace_extract_pat_ = re_.compile(r'{(.*)}(.*)')
CDATA_pattern_ = re_.compile(r"<!\[CDATA\[.*?\]\]>", re_.DOTALL)

# Change this to redirect the generated superclass module to use a
# specific subclass module.
CurrentSubclassModule_ = None

#
# Data representation classes.
#


class ContingenciaDTE(GeneratedsSuper):
    """Elemento Raiz de Contigngencia de Documento Tributario Electronico"""
    subclass = None
    superclass = None

    def __init__(self, motivo=None, selloRecibido=None, identificacion=None, firmaElectronica=None,
                 emisor=None, detalleDTE=None):
        self.original_tagname_ = None
        self.motivo = motivo
        self.selloRecibido = selloRecibido
        self.identificacion = identificacion
        self.firmaElectronica = firmaElectronica
        self.emisor = emisor
        self.detalleDTE = detalleDTE

    def get_identificacion(self):
        return self.identificacion

    def set_identificacion(self, identificacion):
        self.identificacion = identificacion

    def get_emisor(self):
        return self.emisor

    def set_emisor(self, emisor):
        self.emisor = emisor

    # def get_documento(self):
    #     return self.documento
    #
    # def set_documento(self, documento):
    #     self.documento = documento

    def get_motivo(self):
        return self.motivo

    def set_motivo(self, motivo):
        self.motivo = motivo

    def hasContent_(self):
        if (
                self.identificacion is not None or
                self.emisor is not None or
                self.documento is not None or
                self.motivo is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='ECF', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ECF')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        # outfile.write(bytes(('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        if self.hasContent_():
            # outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='ECF', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('%s}%s' % (namespace_, eol_)).encode()))
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportChildren(self, outfile, level, namespace_='', name_='ECF', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''

        if self.identificacion is not None:
            self.identificacion.export(outfile, level, namespace_, name_='identificacion', pretty_print=pretty_print)
        if self.emisor is not None:
            self.emisor.export(outfile, level, namespace_, name_='emisor', pretty_print=pretty_print)
        if self.detalleDTE is not None:
            self.detalleDTE.export(outfile, level, namespace_, name_='detalleDTE', pretty_print=pretty_print)
        if self.motivo is not None:
            self.motivo.export(outfile, level, namespace_, name_='motivo', pretty_print=pretty_print)


class Identificacion(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, codigoGeneracion=None, hTransmision=None, fTransmision=None, ambiente=None, version=None):
        self.original_tagname_ = None
        self.version = version
        self.ambiente = ambiente
        self.codigoGeneracion = codigoGeneracion
        self.hTransmision = hTransmision
        self.fTransmision = fTransmision

    # def get_version(self):
    #     return self.version
    #
    # def set_version(self, version):
    #     self.version = version
    #
    # def get_ambiente(self):
    #     return self.ambiente
    #
    # def set_ambiente(self, ambiente):
    #     self.ambiente = ambiente
    #
    # def get_codigoGeneracion(self):
    #     return self.codigoGeneracion
    #
    # def set_codigoGeneracion(self, codigoGeneracion):
    #     self.codigoGeneracion = codigoGeneracion

    def hasContent_(self):
        if (
                self.version is not None or
                self.ambiente is not None or
                self.codigoGeneracion is not None or
                self.hTransmision is not None or
                self.fTransmision is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='identificacion', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('identificacion')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(
            bytes(('%s"%s":%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        if self.hasContent_():
            outfile.write(bytes(('{%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Identificacion', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
            outfile.write(bytes(('%s},%s' % (namespace_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportChildren(self, outfile, level, namespace_='', name_='EmisorType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.version is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"version":%s,%s' % (
                self.gds_encode(self.gds_format_integer(self.version, input_name='Version')),
                eol_)).encode()))
        if self.ambiente is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"ambiente":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.ambiente), input_name='Ambiente')),
                eol_)).encode()))
        if self.codigoGeneracion is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"codigoGeneracion":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.codigoGeneracion), input_name='codigoGeneracion')),
                eol_)).encode()))
        if self.hTransmision is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"hTransmision":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.hTransmision), input_name='Fecha de Generación')),
                eol_)).encode()))
        if self.fTransmision is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"fTransmision":"%s"%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.fTransmision), input_name='Hora de Generación')),
                eol_)).encode()))


class Emisor(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, nit=None, nrc=None, nombre=None,
                 tipoEstablecimiento=None, nomEstablecimiento=None, codEstableMH=None, codEstable=None,
                 codPuntoVentaMH=None, codPuntoVenta=None, telefono=None, correo=None, nombreResponsable=None,
                 tipoDocResponsable=None, numeroDocResponsable=None):
        self.original_tagname_ = None
        self.nit = nit
        self.nrc = nrc
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.tipoEstablecimiento = tipoEstablecimiento
        self.nomEstablecimiento = nomEstablecimiento
        self.codEstableMH = codEstableMH
        self.codEstable = codEstable
        self.codPuntoVentaMH = codPuntoVentaMH
        self.codPuntoVenta = codPuntoVenta
        self.nombreResponsable = nombreResponsable
        self.tipoDocResponsable = tipoDocResponsable
        self.numeroDocResponsable = numeroDocResponsable

    def get_nit(self):
        return self.nit

    def set_nit(self, nit):
        self.nit = nit

    def get_telefono(self):
        return self.telefono

    def set_telefono(self, telefono):
        self.telefono = telefono

    def get_correo(self):
        return self.correo

    def set_correo(self, correo):
        self.correo = correo

    def hasContent_(self):
        if (
                self.nit is not None or
                self.nombre is not None or
                self.tipoEstablecimiento is not None or
                self.nomEstablecimiento is not None or
                self.nombreResponsable is not None or
                self.tipoDocResponsable is not None or
                self.numeroDocResponsable is not None or
                self.codEstableMH is not None or
                self.codEstable is not None or
                self.codPuntoVentaMH is not None or
                self.codPuntoVenta is not None or
                self.telefono is not None or
                self.correo is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='Emisor', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('identificacion')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(
            bytes(('%s"%s":%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        if self.hasContent_():
            outfile.write(bytes(('{%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Identificacion', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
            outfile.write(bytes(('%s},%s' % (namespace_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportChildren(self, outfile, level, namespace_='', name_='EmisorType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.nit is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"nit":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.nit), input_name='NIT')),
                eol_)).encode()))
        if self.nombre is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"nombre":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.nombre), input_name='Nombre')),
                eol_)).encode()))
        if self.nombreResponsable is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"nombreResponsable":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.nombreResponsable), input_name='Nombre')),
                eol_)).encode()))
        if self.tipoDocResponsable is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tipoDocResponsable":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.tipoDocResponsable), input_name='Nombre')),
                eol_)).encode()))
        if self.numeroDocResponsable is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"numeroDocResponsable":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.numeroDocResponsable), input_name='Nombre')),
                eol_)).encode()))
        if self.tipoEstablecimiento is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tipoEstablecimiento":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.tipoEstablecimiento), input_name='tipoEstablecimiento')),
                eol_)).encode()))
        if self.codEstableMH is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"codEstableMH":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.codEstableMH), input_name='Nombre Comercial (Emisor)')),
                eol_)).encode()))
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"codEstableMH":null,%s' % eol_).encode()))
        # if self.codPuntoVentaMH is not None:
        #     showIndent(outfile, level, pretty_print)
        #     outfile.write(bytes(('"codPuntoVentaMH":"%s",%s' % (
        #         self.gds_encode(self.gds_format_string(quote_xml(self.codPuntoVentaMH), input_name='Nombre Comercial (Emisor)')),
        #         eol_)).encode()))
        # else:
        #     showIndent(outfile, level, pretty_print)
        #     outfile.write(bytes(('"codPuntoVentaMH":null,%s' % eol_).encode()))
        if self.codPuntoVenta is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"codPuntoVenta":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.codPuntoVenta), input_name='Nombre Comercial (Emisor)')),
                eol_)).encode()))
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"codPuntoVenta":null,%s' % eol_).encode()))
        if self.telefono is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"telefono":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.telefono), input_name='Telefono')),
                eol_)).encode()))
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"telefono":null,%s' % eol_).encode()))
        if self.correo is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"correo":"%s"%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.correo), input_name='Correo')),
                eol_)).encode()))


class DetalleDTE(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, Item=None):
        self.original_tagname_ = None
        if Item is None:
            self.Item = []
        else:
            self.Item = Item

    def get_Item(self):
        return self.Item

    def set_Item(self, Item):
        self.Item = Item

    def add_Item(self, value):
        self.Item.append(value)

    def insertItem_at(self, index, value):
        self.Item.insert(index, value)

    def replace_Item_at(self, index, value):
        self.Item[index] = value

    def hasContent_(self):
        if (
                self.Item
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='identificacion', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('identificacion')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(
            bytes(('%s"%s":%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        if self.hasContent_():
            outfile.write(bytes(('[%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Identificacion', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
            outfile.write(bytes(('%s],%s' % (namespace_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportChildren(self, outfile, level, namespace_='', name_='DetalleServicioType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for i, LineaItem_ in enumerate(self.Item, 1):
            LineaItem_.export(outfile, level, namespace_, name_='Item', pretty_print=pretty_print, enu=i, tam=len(self.Item))


class Item(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, noItem, codigoGeneracion=None, tipoDoc=None):
        self.original_tagname_ = None
        self.noItem = noItem
        self.codigoGeneracion = codigoGeneracion
        self.tipoDoc = tipoDoc

    # def get_numItem(self):
    #     return self.numItem
    #
    # def set_numItem(self, numItem):
    #     self.numItem = numItem
    #
    # def get_tipoItem(self):
    #     return self.tipoItem
    #
    # def set_tipoItem(self, tipoItem):
    #     self.tipoItem = tipoItem
    #
    # def get_descripcion(self):
    #     return self.descripcion
    #
    # def set_descripcion(self, descripcion):
    #     self.descripcion = descripcion
    #
    # def get_cantidad(self):
    #     return self.cantidad
    #
    # def set_cantidad(self, cantidad):
    #     self.cantidad = cantidad
    #
    # def get_uniMedida(self):
    #     return self.uniMedida
    #
    # def set_uniMedida(self, uniMedida):
    #     self.uniMedida = uniMedida
    #
    # def get_precioUni(self):
    #     return self.precioUni
    #
    # def set_precioUni(self, precioUni):
    #     self.precioUni = precioUni
    #
    # def get_codigo(self):
    #     return self.codigo
    #
    # def set_codigo(self, codigo):
    #     self.codigo = codigo
    #
    # def get_ventaGravada(self):
    #     return self.ventaGravada
    #
    # def set_ventaGravada(self, ventaGravada):
    #     self.ventaGravada = ventaGravada
    #
    # def get_montoDescu(self):
    #     return self.montoDescu
    #
    # def set_montoDescu(self, montoDescu):
    #     self.montoDescu = montoDescu
    #
    # def get_ventaExenta(self):
    #     return self.ventaExenta
    #
    # def set_ventaExenta(self, ventaExenta):
    #     self.ventaExenta = ventaExenta
    #
    # def get_tributos(self):
    #     return self.tributos
    #
    # def set_tributos(self, tributos):
    #     self.tributos = tributos
    #
    # def add_tributos(self, value):
    #     self.tributos.append(value)
    #
    # def insert_tributos_at(self, index, value):
    #     self.tributos.insert(index, value)
    #
    # def replace_tributos_at(self, index, value):
    #     self.tributos[index] = value

    def hasContent_(self):
        if (
                self.noItem is not None or
                self.codigoGeneracion is not None or
                self.tipoDoc is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='Item', namespacedef_='', pretty_print=True, enu=None, tam=None):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('identificacion')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(
            # bytes(('%s"%s":%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
            bytes(('%s%s' % (namespace_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        if self.hasContent_():
            outfile.write(bytes(('{%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Identificacion', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
            if enu == 1 and tam == 1:
                outfile.write(bytes(('%s}%s' % (namespace_, eol_)).encode()))
            elif enu != tam:
                outfile.write(bytes(('%s},%s' % (namespace_, eol_)).encode()))
            else:
                outfile.write(bytes(('%s}%s' % (namespace_, eol_)).encode()))
        #     outfile.write(bytes(('%s}%s' % (namespace_, eol_)).encode()))
        # else:
        #     outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportChildren(self, outfile, level, namespace_='', name_='EmisorType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.noItem is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"noItem":%s,%s' % (
                self.gds_encode(self.gds_format_integer(self.noItem, input_name='Version')),
                eol_)).encode()))
        if self.codigoGeneracion is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"codigoGeneracion":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.codigoGeneracion), input_name='TipoItem')),
                eol_)).encode()))
        if self.tipoDoc is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tipoDoc":"%s"%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.tipoDoc),
                                                       input_name='Número de documento relacionado')),
                eol_)).encode()))


class Motivo(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, tipoContingencia=None, hFin=None, hInicio=None, fInicio=None, fFin=None, motivoContingencia=None):
        self.original_tagname_ = None
        self.tipoContingencia = tipoContingencia
        self.hFin = hFin
        self.hInicio = hInicio
        self.fInicio = fInicio
        self.fFin = fFin
        self.motivoContingencia = motivoContingencia

    # def get_version(self):
    #     return self.version
    #
    # def set_version(self, version):
    #     self.version = version
    #
    # def get_ambiente(self):
    #     return self.ambiente
    #
    # def set_ambiente(self, ambiente):
    #     self.ambiente = ambiente
    #
    # def get_codigoGeneracion(self):
    #     return self.codigoGeneracion
    #
    # def set_codigoGeneracion(self, codigoGeneracion):
    #     self.codigoGeneracion = codigoGeneracion

    def hasContent_(self):
        if (
                self.tipoContingencia is not None or
                self.hFin is not None or
                self.hInicio is not None or
                self.fInicio is not None or
                self.fFin is not None or
                self.motivoContingencia is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='identificacion', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('identificacion')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(
            bytes(('%s"%s":%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        if self.hasContent_():
            outfile.write(bytes(('{%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Identificacion', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
            outfile.write(bytes(('%s}%s' % (namespace_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportChildren(self, outfile, level, namespace_='', name_='EmisorType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''

        if self.fInicio is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"fInicio":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.fInicio), input_name='Fecha de Generación')),
                eol_)).encode()))
        if self.fFin is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"fFin":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.fFin), input_name='Hora de Generación')),
                eol_)).encode()))
        if self.hInicio is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"hInicio":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.hInicio), input_name='codigoGeneracion')),
                eol_)).encode()))
        if self.hFin is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"hFin":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.hFin), input_name='Ambiente')),
                eol_)).encode()))
        if self.tipoContingencia is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tipoContingencia":%s,%s' % (
                self.gds_encode(self.gds_format_integer(self.tipoContingencia, input_name='Version')),
                eol_)).encode()))
        if self.motivoContingencia is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"motivoContingencia":"%s"%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.motivoContingencia), input_name='Hora de Generación')),
                eol_)).encode()))
