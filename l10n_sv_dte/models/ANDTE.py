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


class InvalidacionDTE(GeneratedsSuper):
    """Elemento Raiz de Invalidacion de Documento Tributario Electronico"""
    subclass = None
    superclass = None

    def __init__(self, identificacion=None, emisor=None, documento=None, motivo=None):
        self.original_tagname_ = None
        self.identificacion = identificacion
        self.emisor = emisor
        self.documento = documento
        self.motivo = motivo

    def get_identificacion(self):
        return self.identificacion

    def set_identificacion(self, identificacion):
        self.identificacion = identificacion

    def get_emisor(self):
        return self.emisor

    def set_emisor(self, emisor):
        self.emisor = emisor

    def get_documento(self):
        return self.documento

    def set_documento(self, documento):
        self.documento = documento

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
        if self.documento is not None:
            self.documento.export(outfile, level, namespace_, name_='documento', pretty_print=pretty_print)
        if self.motivo is not None:
            self.motivo.export(outfile, level, namespace_, name_='motivo', pretty_print=pretty_print)


class Identificacion(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, version, ambiente=None, codigoGeneracion=None, fecAnula=None, horAnula=None):
        self.original_tagname_ = None
        self.version = version
        self.ambiente = ambiente
        self.codigoGeneracion = codigoGeneracion
        self.fecAnula = fecAnula
        self.horAnula = horAnula

    def get_version(self):
        return self.version

    def set_version(self, version):
        self.version = version

    def get_ambiente(self):
        return self.ambiente

    def set_ambiente(self, ambiente):
        self.ambiente = ambiente

    def get_codigoGeneracion(self):
        return self.codigoGeneracion

    def set_codigoGeneracion(self, codigoGeneracion):
        self.codigoGeneracion = codigoGeneracion

    def hasContent_(self):
        if (
                self.version is not None or
                self.ambiente is not None or
                self.codigoGeneracion is not None or
                self.fecAnula is not None or
                self.horAnula is not None
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
        if self.fecAnula is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"fecAnula":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.fecAnula), input_name='Fecha de Generación')),
                eol_)).encode()))
        if self.horAnula is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"horAnula":"%s"%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.horAnula), input_name='Hora de Generación')),
                eol_)).encode()))


class Emisor(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, nit=None, nrc=None, nombre=None,
                 tipoEstablecimiento=None, nomEstablecimiento=None, codEstableMH=None, codEstable=None,
                 codPuntoVentaMH=None, codPuntoVenta=None, telefono=None, correo=None):
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
        if self.tipoEstablecimiento is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tipoEstablecimiento":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.tipoEstablecimiento), input_name='tipoEstablecimiento')),
                eol_)).encode()))
        if self.nomEstablecimiento is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"nomEstablecimiento":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.nomEstablecimiento), input_name='Actividad Económica (Emisor)')),
                eol_)).encode()))
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"nomEstablecimiento":null,%s' % eol_).encode()))
        # if self.codEstableMH is not None:
        #     showIndent(outfile, level, pretty_print)
        #     outfile.write(bytes(('"codEstableMH":"%s",%s' % (
        #         self.gds_encode(self.gds_format_string(quote_xml(self.codEstableMH), input_name='Nombre Comercial (Emisor)')),
        #         eol_)).encode()))
        # else:
        #     showIndent(outfile, level, pretty_print)
        #     outfile.write(bytes(('"codEstableMH":null,%s' % eol_).encode()))
        if self.codEstable is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"codEstable":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.codEstable), input_name='Nombre Comercial (Emisor)')),
                eol_)).encode()))
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"codEstable":null,%s' % eol_).encode()))
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


class Documento(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, tipoDte=None, codigoGeneracion=None, selloRecibido=None, numeroControl=None, fecEmi=None,
                 montoIva=None, codigoGeneracionR=None, codEstablecimiento=None, tipoDocumento=None, numDocumento=None,
                 nombre=None, telefono=None, correo=None):
        self.original_tagname_ = None
        self.tipoDte = tipoDte
        self.codigoGeneracion = codigoGeneracion
        self.selloRecibido = selloRecibido
        self.numeroControl = numeroControl
        self.fecEmi = fecEmi
        self.montoIva = montoIva
        self.codigoGeneracionR = codigoGeneracionR
        self.codEstablecimiento = codEstablecimiento
        self.tipoDocumento = tipoDocumento
        self.numDocumento = numDocumento
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo

    def get_tipoDte(self):
        return self.tipoDte

    def set_tipoDTE(self, tipoDte):
        self.tipoDte = tipoDte

    def hasContent_(self):
        if (
                self.tipoDte is not None or
                self.codigoGeneracion is not None or
                self.codEstablecimiento is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='Resumen', namespacedef_='', pretty_print=True):
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
        if self.tipoDte is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tipoDte":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.tipoDte), input_name='Version')),
                eol_)).encode()))
        if self.codigoGeneracion is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"codigoGeneracion":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.codigoGeneracion), input_name='Version')),
                eol_)).encode()))
        if self.selloRecibido is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"selloRecibido":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.selloRecibido), input_name='Version')),
                eol_)).encode()))
        if self.numeroControl is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"numeroControl":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.numeroControl), input_name='Version')),
                eol_)).encode()))
        if self.fecEmi is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"fecEmi":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.fecEmi), input_name='Version')),
                eol_)).encode()))
        if self.montoIva is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"montoIva":%s,%s' % (
                self.gds_encode(self.gds_format_float(self.montoIva, input_name='PrecioUni')),
                eol_)).encode()))
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"montoIva":null,%s' % eol_).encode()))
        if self.codigoGeneracionR is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"codigoGeneracionR":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.codigoGeneracionR), input_name='Actividad Económica (Emisor)')),
                eol_)).encode()))
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"codigoGeneracionR":null,%s' % eol_).encode()))
        # if self.codEstablecimiento is not None:
        #     showIndent(outfile, level, pretty_print)
        #     outfile.write(bytes(('"codEstablecimiento":"%s"%s' % (
        #         self.gds_encode(self.gds_format_string(quote_xml(self.codEstablecimiento), input_name='Version')),
        #         eol_)).encode()))
        if self.tipoDocumento is not None and self.tipoDocumento is not False:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tipoDocumento":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.tipoDocumento), input_name='Version')),
                eol_)).encode()))
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tipoDocumento":null,%s' % eol_).encode()))
        if self.numDocumento is not None and self.numDocumento is not False:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"numDocumento":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.numDocumento), input_name='Version')),
                eol_)).encode()))
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"numDocumento":null,%s' % eol_).encode()))
        if self.nombre is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"nombre":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.nombre), input_name='Version')),
                eol_)).encode()))
        # else:
        #     showIndent(outfile, level, pretty_print)
        #     outfile.write(bytes(('"nombre":null%s' % eol_).encode()))
        if self.telefono is not None and self.telefono is not False:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"telefono":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.telefono), input_name='Version')),
                eol_)).encode()))
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"telefono":null,%s' % eol_).encode()))
        if self.correo is not None and self.correo is not False:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"correo":"%s"%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.correo), input_name='Version')),
                eol_)).encode()))
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"correo":null%s' % eol_).encode()))


class Motivo(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, tipoAnulacion=None, motivoAnulacion=None, nombreResponsable=None, tipDocResponsable=None,
                 numDocResponsable=None, nombreSolicita=None, tipDocSolicita=None, numDocSolicita=None):
        self.original_tagname_ = None
        self.tipoAnulacion = tipoAnulacion
        self.motivoAnulacion = motivoAnulacion
        self.nombreResponsable = nombreResponsable
        self.tipDocResponsable = tipDocResponsable
        self.numDocResponsable = numDocResponsable
        self.nombreSolicita = nombreSolicita
        self.tipDocSolicita = tipDocSolicita
        self.numDocSolicita = numDocSolicita

    def hasContent_(self):
        if (
                self.tipoAnulacion is not None or
                self.motivoAnulacion is not None or
                self.nombreResponsable is not None or
                self.tipDocResponsable is not None or
                self.numDocResponsable is not None or
                self.nombreSolicita is not None or
                self.tipDocSolicita is not None or
                self.numDocSolicita is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='Resumen', namespacedef_='', pretty_print=True):
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
        # if self.tipoAnulacion is not None:
        #     showIndent(outfile, level, pretty_print)
        #     outfile.write(bytes(('"tipoAnulacion":"%s",%s' % (
        #         self.gds_encode(self.gds_format_string(quote_xml(self.tipoAnulacion), input_name='Version')),
        #         eol_)).encode()))
        if self.tipoAnulacion is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tipoAnulacion":%s,%s' % (
                self.gds_encode(self.gds_format_integer(self.tipoAnulacion, input_name='tipoAnulacion')),
                eol_)).encode()))
        if self.motivoAnulacion is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"motivoAnulacion":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.motivoAnulacion), input_name='Version')),
                eol_)).encode()))
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"motivoAnulacion":null,%s' % eol_).encode()))
        if self.nombreResponsable is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"nombreResponsable":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.nombreResponsable), input_name='Version')),
                eol_)).encode()))
        if self.tipDocResponsable is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tipDocResponsable":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.tipDocResponsable), input_name='Version')),
                eol_)).encode()))
        if self.numDocResponsable is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"numDocResponsable":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.numDocResponsable), input_name='Version')),
                eol_)).encode()))
        if self.nombreSolicita is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"nombreSolicita":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.nombreSolicita), input_name='Version')),
                eol_)).encode()))
        if self.tipDocSolicita is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tipDocSolicita":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.tipDocSolicita), input_name='Version')),
                eol_)).encode()))
        if self.numDocSolicita is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"numDocSolicita":"%s"%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.numDocSolicita), input_name='Version')),
                eol_)).encode()))
