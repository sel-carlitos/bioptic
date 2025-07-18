import re as re_

from .MixedClass import GeneratedsSuper, quote_xml, showIndent

try:
    from lxml import etree as etree_
except ImportError:
    pass

Validate_simpletypes_ = True
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
String_cleanup_pat_ = re_.compile(r'[\n\r\s]+')
Namespace_extract_pat_ = re_.compile(r'{(.*)}(.*)')
CDATA_pattern_ = re_.compile(r'<!\[CDATA\[.*?\]\]>', re_.DOTALL)

# Change this to redirect the generated superclass module to use a
# specific subclass module.
CurrentSubclassModule_ = None

#
# Data representation classes.
#


class NotaDebitoElectronica(GeneratedsSuper):
    """Elemento Raiz de la Nota de Débito"""

    subclass = None
    superclass = None

    def __init__(
        self,
        identificacion=None,
        documentoRelacionado=None,
        emisor=None,
        receptor=None,
        ventaTercero=None,
        cuerpoDocumento=None,
        resumen=None,
        extension=None,
        apendice=None,
    ):
        self.original_tagname_ = None
        self.identificacion = identificacion
        self.documentoRelacionado = documentoRelacionado
        self.emisor = emisor
        self.receptor = receptor
        self.ventaTercero = ventaTercero
        self.cuerpoDocumento = cuerpoDocumento
        self.resumen = resumen
        self.extension = extension
        self.apendice = apendice

    def get_identificacion(self):
        return self.identificacion

    def set_identificacion(self, identificacion):
        self.identificacion = identificacion

    def get_documentoRelacionado(self):
        return self.documentoRelacionado

    def set_documentoRelacionado(self, documentoRelacionado):
        self.documentoRelacionado = documentoRelacionado

    def get_emisor(self):
        return self.emisor

    def set_emisor(self, emisor):
        self.emisor = emisor

    def get_receptor(self):
        return self.receptor

    def set_receptor(self, receptor):
        self.receptor = receptor

    def get_cuerpoDocumento(self):
        return self.cuerpoDocumento

    def set_cuerpoDocumento(self, cuerpoDocumento):
        self.cuerpoDocumento = cuerpoDocumento

    def get_resumen(self):
        return self.resumen

    def set_resumen(self, resumen):
        self.resumen = resumen

    def hasContent_(self):
        if (
            self.identificacion is not None
            or self.documentoRelacionado is not None
            or self.emisor is not None
            or self.receptor is not None
            or self.cuerpoDocumento is not None
            or self.resumen is not None
            or self.extension is not None
            or self.apendice is not None
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

    def exportChildren(self, outfile, level, namespace_='', name_='ECF', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''

        if self.identificacion is not None:
            self.identificacion.export(outfile, level, namespace_, name_='identificacion', pretty_print=pretty_print)
        if self.documentoRelacionado is not None:
            self.documentoRelacionado.export(
                outfile, level, namespace_, name_='documentoRelacionado', pretty_print=pretty_print
            )
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"documentoRelacionado":null,%s' % eol_).encode()))
        if self.emisor is not None:
            self.emisor.export(outfile, level, namespace_, name_='emisor', pretty_print=pretty_print)
        if self.receptor is not None:
            self.receptor.export(outfile, level, namespace_, name_='receptor', pretty_print=pretty_print)
        if self.ventaTercero is not None:
            self.ventaTercero.export(outfile, level, namespace_, name_='ventaTercero', pretty_print=pretty_print)
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"ventaTercero":null,%s' % eol_).encode()))

        if self.cuerpoDocumento is not None:
            self.cuerpoDocumento.export(outfile, level, namespace_, name_='cuerpoDocumento', pretty_print=pretty_print)
        if self.resumen is not None:
            self.resumen.export(outfile, level, namespace_, name_='resumen', pretty_print=pretty_print)

        if self.extension is not None:
            self.extension.export(outfile, level, namespace_, name_='extension', pretty_print=pretty_print)
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"extension":null,%s' % eol_).encode()))
        if self.apendice is not None:
            self.apendice.export(outfile, level, namespace_, name_='apendice', pretty_print=pretty_print)
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"apendice":null%s' % eol_).encode()))


class DocumentosRelacionado(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, documentoRelacionado=None):
        self.original_tagname_ = None
        if documentoRelacionado is None:
            self.documentoRelacionado = []
        else:
            self.documentoRelacionado = documentoRelacionado

    def get_documentoRelacionado(self):
        return self.documentoRelacionado

    def set_documentoRelacionado(self, documentoRelacionado):
        self.documentoRelacionado = documentoRelacionado

    def add_documentoRelacionado(self, value):
        self.documentoRelacionado.append(value)

    def insert_documentoRelacionado_at(self, index, value):
        self.documentoRelacionado.insert(index, value)

    def replace_documentoRelacionado_at(self, index, value):
        self.documentoRelacionado[index] = value

    def hasContent_(self):
        if self.documentoRelacionado:
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='CuerpoDocumento', namespacedef_='', pretty_print=True):
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
            bytes(
                (
                    '%s"%s":%s'
                    % (
                        namespace_,
                        name_,
                        namespacedef_ and ' ' + namespacedef_ or '',
                    )
                ).encode()
            )
        )
        if self.hasContent_():
            outfile.write(bytes(('[%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Identificacion', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
            outfile.write(bytes(('%s],%s' % (namespace_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportChildren(
        self, outfile, level, namespace_='', name_='DetalleServicioType', fromsubclass_=False, pretty_print=True
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for documentoRelacionado_ in self.documentoRelacionado:
            documentoRelacionado_.export(outfile, level, namespace_, name_='Item', pretty_print=pretty_print)


class DocumentoRelacionado(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, tipoDocumento=None, tipoGeneracion=None, numeroDocumento=None, fechaEmision=None):
        self.original_tagname_ = None
        self.tipoDocumento = tipoDocumento
        self.tipoGeneracion = tipoGeneracion
        self.numeroDocumento = numeroDocumento
        self.fechaEmision = fechaEmision

    def get_tipoDocumento(self):
        return self.tipoDocumento

    def set_tipoDocumento(self, tipoDocumento):
        self.tipoDocumento = tipoDocumento

    def get_tipoGeneracion(self):
        return self.tipoGeneracion

    def set_tipoGeneracion(self, tipoGeneracion):
        self.tipoGeneracion = tipoGeneracion

    def get_numeroDocumento(self):
        return self.numeroDocumento

    def set_numeroDocumento(self, numeroDocumento):
        self.numeroDocumento = numeroDocumento

    def get_fechaEmision(self):
        return self.fechaEmision

    def set_fechaEmision(self, fechaEmision):
        self.fechaEmision = fechaEmision

    def hasContent_(self):
        if (
            self.tipoDocumento is not None
            or self.tipoGeneracion is not None
            or self.numeroDocumento is not None
            or self.fechaEmision is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='Item', namespacedef_='', pretty_print=True):
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
            bytes(
                (
                    '%s%s'
                    % (
                        namespace_,
                        namespacedef_ and ' ' + namespacedef_ or '',
                    )
                ).encode()
            )
        )
        if self.hasContent_():
            outfile.write(bytes(('{%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Identificacion', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
            outfile.write(bytes(('%s}%s' % (namespace_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportChildren(self, outfile, level, namespace_='', name_='EmisorType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.tipoDocumento is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"tipoDocumento":"%s",%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(
                                    quote_xml(self.tipoDocumento), input_name='Tipo de Documento Tributario Relacionado'
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.tipoGeneracion is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"tipoGeneracion":%s,%s'
                        % (
                            self.gds_format_integer(
                                self.tipoGeneracion,
                                input_name='Tipo de Generación del Documento Tributario relacionado',
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.numeroDocumento is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"numeroDocumento":"%s",%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(
                                    quote_xml(self.numeroDocumento), input_name='Número de documento relacionado'
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.fechaEmision is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"fechaEmision":"%s"%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(
                                    quote_xml(self.fechaEmision),
                                    input_name='Fecha de Generación del Documento Relacionado',
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )


class Identificacion(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(
        self,
        version,
        ambiente=None,
        tipoDTE=None,
        numeroControl=None,
        codigoGeneracion=None,
        tipoModelo=None,
        tipoOperacion=None,
        fecEmi=None,
        horEmi=None,
        tipoMoneda=None,
        tipoContingencia=None,
        motivoContin=None,
    ):
        self.original_tagname_ = None
        self.version = version
        self.ambiente = ambiente
        self.tipoDTE = tipoDTE
        self.numeroControl = numeroControl
        self.codigoGeneracion = codigoGeneracion
        self.tipoModelo = tipoModelo
        self.tipoOperacion = tipoOperacion
        self.fecEmi = fecEmi
        self.horEmi = horEmi
        self.tipoMoneda = tipoMoneda
        self.tipoContingencia = tipoContingencia
        self.motivoContin = motivoContin

    def get_version(self):
        return self.version

    def set_version(self, version):
        self.version = version

    def get_ambiente(self):
        return self.ambiente

    def set_ambiente(self, ambiente):
        self.ambiente = ambiente

    def get_tipoDTE(self):
        return self.tipoDTE

    def set_tipoDTE(self, tipoDTE):
        self.tipoDTE = tipoDTE

    def get_numeroControl(self):
        return self.numeroControl

    def set_numeroControl(self, numeroControl):
        self.numeroControl = numeroControl

    def get_codigoGeneracion(self):
        return self.codigoGeneracion

    def set_codigoGeneracion(self, codigoGeneracion):
        self.codigoGeneracion = codigoGeneracion

    def hasContent_(self):
        if (
            self.version is not None
            or self.ambiente is not None
            or self.tipoDTE is not None
            or self.numeroControl is not None
            or self.codigoGeneracion is not None
            or self.tipoModelo is not None
            or self.tipoOperacion is not None
            or self.fecEmi is not None
            or self.horEmi is not None
            or self.tipoMoneda is not None
            or self.tipoContingencia is not None
            or self.motivoContin is not None
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
            bytes(
                (
                    '%s"%s":%s'
                    % (
                        namespace_,
                        name_,
                        namespacedef_ and ' ' + namespacedef_ or '',
                    )
                ).encode()
            )
        )
        if self.hasContent_():
            outfile.write(bytes(('{%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Identificacion', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
            outfile.write(bytes(('%s},%s' % (namespace_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportChildren(self, outfile, level, namespace_='', name_='EmisorType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.version is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"version":%s,%s'
                        % (self.gds_encode(self.gds_format_integer(self.version, input_name='Version')), eol_)
                    ).encode()
                )
            )
        if self.ambiente is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"ambiente":"%s",%s'
                        % (
                            self.gds_encode(self.gds_format_string(quote_xml(self.ambiente), input_name='Ambiente')),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.tipoDTE is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"tipoDte":"%s",%s'
                        % (self.gds_encode(self.gds_format_string(quote_xml(self.tipoDTE), input_name='TipoDTE')), eol_)
                    ).encode()
                )
            )
        if self.numeroControl is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"numeroControl":"%s",%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(quote_xml(self.numeroControl), input_name='NumeroControl')
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.tipoModelo is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"tipoModelo":%s,%s'
                        % (self.gds_format_integer(self.tipoModelo, input_name='Modelo de Facturación'), eol_)
                    ).encode()
                )
            )
        if self.tipoOperacion is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"tipoOperacion":%s,%s'
                        % (self.gds_format_integer(self.tipoOperacion, input_name='Tipo de Transmisión'), eol_)
                    ).encode()
                )
            )
        if self.tipoContingencia is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"tipoContingencia":%s,%s'
                        % (self.gds_format_integer(self.tipoContingencia, input_name='Tipo de Contingencia'), eol_)
                    ).encode()
                )
            )
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tipoContingencia":null,%s' % eol_).encode()))
        if self.motivoContin is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"motivoContin":%s,%s'
                        % (self.gds_format_integer(self.motivoContin, input_name='Motivo de Contingencia'), eol_)
                    ).encode()
                )
            )
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"motivoContin":null,%s' % eol_).encode()))
        if self.codigoGeneracion is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"codigoGeneracion":"%s",%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(
                                    quote_xml(self.codigoGeneracion), input_name='Código de Generación'
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.fecEmi is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"fecEmi":"%s",%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(quote_xml(self.fecEmi), input_name='Fecha de Generación')
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.horEmi is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"horEmi":"%s",%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(quote_xml(self.horEmi), input_name='Hora de Generación')
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.tipoMoneda is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"tipoMoneda":"%s"%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(quote_xml(self.tipoMoneda), input_name='Tipo de Moneda')
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )


class Emisor(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(
        self,
        nit=None,
        nrc=None,
        nombre=None,
        codActividad=None,
        descActividad=None,
        telefono=None,
        correo=None,
        nombreComercial=None,
        tipoEstablecimiento=None,
        direccion=None,
    ):
        self.original_tagname_ = None
        self.nit = nit
        self.nrc = nrc
        self.nombre = nombre
        self.codActividad = codActividad
        self.descActividad = descActividad
        self.telefono = telefono
        self.correo = correo
        self.nombreComercial = nombreComercial
        self.tipoEstablecimiento = tipoEstablecimiento
        self.direccion = direccion

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

    def get_nombreComercial(self):
        return self.nombreComercial

    def set_nombreComercial(self, nombreComercial):
        self.nombreComercial = nombreComercial

    def get_tipoEstablecimiento(self):
        return self.tipoEstablecimiento

    def set_tipoEstablecimiento(self, tipoEstablecimiento):
        self.tipoEstablecimiento = tipoEstablecimiento

    def hasContent_(self):
        if (
            self.nit is not None
            or self.nombre is not None
            or self.codActividad is not None
            or self.telefono is not None
            or self.correo is not None
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
            bytes(
                (
                    '%s"%s":%s'
                    % (
                        namespace_,
                        name_,
                        namespacedef_ and ' ' + namespacedef_ or '',
                    )
                ).encode()
            )
        )
        if self.hasContent_():
            outfile.write(bytes(('{%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Identificacion', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
            outfile.write(bytes(('%s},%s' % (namespace_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportChildren(self, outfile, level, namespace_='', name_='EmisorType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.nit is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"nit":"%s",%s'
                        % (
                            self.gds_encode(self.gds_format_string(quote_xml(self.nit), input_name='NIT (Emisor)')),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.nrc is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"nrc":"%s",%s'
                        % (
                            self.gds_encode(self.gds_format_string(quote_xml(self.nrc), input_name='NRC (Emisor)')),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.nombre is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"nombre":"%s",%s'
                        % (self.gds_encode(self.gds_format_string(quote_xml(self.nombre), input_name='Nombre')), eol_)
                    ).encode()
                )
            )
        if self.codActividad is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"codActividad":"%s",%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(quote_xml(self.codActividad), input_name='CodActividad')
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.descActividad is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"descActividad":"%s",%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(
                                    quote_xml(self.descActividad), input_name='Actividad Económica (Emisor)'
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.nombreComercial is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"nombreComercial":"%s",%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(
                                    quote_xml(self.nombreComercial), input_name='Nombre Comercial (Emisor)'
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.tipoEstablecimiento is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"tipoEstablecimiento":"%s",%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(
                                    quote_xml(self.tipoEstablecimiento), input_name='Tipo de establecimiento (Emisor)'
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.direccion is not None:
            self.direccion.export(outfile, level, namespace_, name_='direccion', pretty_print=pretty_print)
        if self.telefono is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"telefono":"%s",%s'
                        % (
                            self.gds_encode(self.gds_format_string(quote_xml(self.telefono), input_name='Telefono')),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.correo is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"correo":"%s"%s'
                        % (self.gds_encode(self.gds_format_string(quote_xml(self.correo), input_name='Correo')), eol_)
                    ).encode()
                )
            )


class Direccion(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(
        self,
        departamento=None,
        municipio=None,
        complemento=None,
    ):
        self.original_tagname_ = None
        self.departamento = departamento
        self.municipio = municipio
        self.complemento = complemento

    def get_departamento(self):
        return self.departamento

    def set_nit(self, departamento):
        self.departamento = departamento

    def get_municipio(self):
        return self.municipio

    def set_municipio(self, municipio):
        self.municipio = municipio

    def get_complemento(self):
        return self.complemento

    def set_complemento(self, complemento):
        self.complemento = complemento

    def hasContent_(self):
        if self.departamento is not None or self.municipio is not None or self.complemento is not None:
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
            bytes(
                (
                    '%s"%s":%s'
                    % (
                        namespace_,
                        name_,
                        namespacedef_ and ' ' + namespacedef_ or '',
                    )
                ).encode()
            )
        )
        if self.hasContent_():
            outfile.write(bytes(('{%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Identificacion', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
            outfile.write(bytes(('%s},%s' % (namespace_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportChildren(self, outfile, level, namespace_='', name_='EmisorType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.departamento is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"departamento":"%s",%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(
                                    quote_xml(self.departamento), input_name='Dirección: Departamento'
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.municipio is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"municipio":"%s",%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(quote_xml(self.municipio), input_name='Dirección: Municipio')
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.complemento is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"complemento":"%s"%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(quote_xml(self.complemento), input_name='Dirección: complemento')
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )


class Receptor(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(
        self,
        nit=None,
        nombre=None,
        tipoDocumento=None,
        numDocumento=None,
        nrc=None,
        codActividad=None,
        descActividad=None,
        direccion=None,
        telefono=None,
        correo=None,
        nombreComercial=None,
    ):
        self.original_tagname_ = None
        self.nit = nit
        self.nombre = nombre
        self.tipoDocumento = tipoDocumento
        self.numDocumento = numDocumento
        self.nrc = nrc
        self.codActividad = codActividad
        self.descActividad = descActividad
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.nombreComercial = nombreComercial

    def get_nit(self):
        return self.nit

    def set_nit(self, nit):
        self.nit = nit

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre):
        self.nombre = nombre

    def hasContent_(self):
        if (
            self.nit is not None
            or self.nombre is not None
            or self.tipoDocumento is not None
            or self.numDocumento is not None
            or self.nrc is not None
            or self.codActividad is not None
            or self.descActividad is not None
            or self.direccion is not None
            or self.telefono is not None
            or self.correo is not None
            or self.nombreComercial is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='Receptor', namespacedef_='', pretty_print=True):
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
            bytes(
                (
                    '%s"%s":%s'
                    % (
                        namespace_,
                        name_,
                        namespacedef_ and ' ' + namespacedef_ or '',
                    )
                ).encode()
            )
        )
        if self.hasContent_():
            outfile.write(bytes(('{%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Identificacion', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
            outfile.write(bytes(('%s},%s' % (namespace_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportChildren(self, outfile, level, namespace_='', name_='EmisorType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.nit is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"nit":"%s",%s'
                        % (self.gds_encode(self.gds_format_string(quote_xml(self.nit), input_name='NIT')), eol_)
                    ).encode()
                )
            )
        if self.tipoDocumento is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"tipoDocumento":"%s",%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(
                                    quote_xml(self.tipoDocumento),
                                    input_name='Tipo de documento de identificación (Receptor)',
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.numDocumento is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"numDocumento":"%s",%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(
                                    quote_xml(self.numDocumento),
                                    input_name='Número de documento de Identificación (Receptor)',
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.nrc is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"nrc":"%s",%s'
                        % (
                            self.gds_encode(self.gds_format_string(quote_xml(self.nrc), input_name='NRC (Receptor)')),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.nombre is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"nombre":"%s",%s'
                        % (self.gds_encode(self.gds_format_string(quote_xml(self.nombre), input_name='Nombre')), eol_)
                    ).encode()
                )
            )
        if self.codActividad is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"codActividad":"%s",%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(
                                    quote_xml(self.codActividad), input_name='Código de Actividad Económica (Receptor)'
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.descActividad is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"descActividad":"%s",%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(
                                    quote_xml(self.descActividad), input_name='Actividad Económica (Receptor)'
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.nombreComercial is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"nombreComercial":"%s",%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(
                                    quote_xml(self.nombreComercial), input_name='Nombre Comercial (Receptor)'
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"nombreComercial":null,%s' % eol_).encode()))
        if self.direccion is not None:
            self.direccion.export(outfile, level, namespace_, name_='direccion', pretty_print=pretty_print)
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"direccion":null,%s' % eol_).encode()))
        if self.telefono is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"telefono":"%s",%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(
                                    quote_xml(self.telefono), input_name='Actividad Económica (Receptor)'
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.correo is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"correo":"%s"%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(
                                    quote_xml(self.correo), input_name='Correo electrónico (Receptor)'
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )


class CuerpoDocumento(GeneratedsSuper):
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
        if self.Item:
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='CuerpoDocumento', namespacedef_='', pretty_print=True):
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
            bytes(
                (
                    '%s"%s":%s'
                    % (
                        namespace_,
                        name_,
                        namespacedef_ and ' ' + namespacedef_ or '',
                    )
                ).encode()
            )
        )
        if self.hasContent_():
            outfile.write(bytes(('[%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Identificacion', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
            outfile.write(bytes(('%s],%s' % (namespace_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportChildren(
        self, outfile, level, namespace_='', name_='DetalleServicioType', fromsubclass_=False, pretty_print=True
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for i, LineaItem_ in enumerate(self.Item, 1):
            LineaItem_.export(
                outfile, level, namespace_, name_='Item', pretty_print=pretty_print, enu=i, tam=len(self.Item)
            )


class Item(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(
        self,
        numItem,
        tipoItem=None,
        descripcion=None,
        cantidad=None,
        uniMedida=None,
        precioUni=None,
        numeroDocumento=None,
        codigo=None,
        codTributo=None,
        montoDescu=0.00,
        ventaNoSuj=0.00,
        ventaExenta=0.00,
        ventaGravada=0.00,
        tributos=None,
    ):
        self.original_tagname_ = None
        self.numItem = numItem
        self.tipoItem = tipoItem
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.uniMedida = uniMedida
        self.precioUni = precioUni
        self.numeroDocumento = numeroDocumento
        self.codigo = codigo
        self.codTributo = codTributo
        self.montoDescu = montoDescu
        self.ventaNoSuj = ventaNoSuj
        self.ventaExenta = ventaExenta
        self.ventaGravada = ventaGravada
        if tributos is None:
            self.tributos = []
        else:
            self.tributos = tributos

    def get_numItem(self):
        return self.numItem

    def set_numItem(self, numItem):
        self.numItem = numItem

    def get_tipoItem(self):
        return self.tipoItem

    def set_tipoItem(self, tipoItem):
        self.tipoItem = tipoItem

    def get_descripcion(self):
        return self.descripcion

    def set_descripcion(self, descripcion):
        self.descripcion = descripcion

    def get_cantidad(self):
        return self.cantidad

    def set_cantidad(self, cantidad):
        self.cantidad = cantidad

    def get_uniMedida(self):
        return self.uniMedida

    def set_uniMedida(self, uniMedida):
        self.uniMedida = uniMedida

    def get_precioUni(self):
        return self.precioUni

    def set_precioUni(self, precioUni):
        self.precioUni = precioUni

    def get_codigo(self):
        return self.codigo

    def set_codigo(self, codigo):
        self.codigo = codigo

    def get_numeroDocumento(self):
        return self.numeroDocumento

    def set_numeroDocumento(self, numeroDocumento):
        self.numeroDocumento = numeroDocumento

    def get_ventaGravada(self):
        return self.ventaGravada

    def set_ventaGravada(self, ventaGravada):
        self.ventaGravada = ventaGravada

    def get_montoDescu(self):
        return self.montoDescu

    def set_montoDescu(self, montoDescu):
        self.montoDescu = montoDescu

    def get_ventaExenta(self):
        return self.ventaExenta

    def set_ventaExenta(self, ventaExenta):
        self.ventaExenta = ventaExenta

    def get_tributos(self):
        return self.tributos

    def set_tributos(self, tributos):
        self.tributos = tributos

    def add_tributos(self, value):
        self.tributos.append(value)

    def insert_tributos_at(self, index, value):
        self.tributos.insert(index, value)

    def replace_tributos_at(self, index, value):
        self.tributos[index] = value

    def hasContent_(self):
        if (
            self.numItem is not None
            or self.tipoItem is not None
            or self.descripcion is not None
            or self.cantidad is not None
            or self.uniMedida is not None
            or self.precioUni is not None
            or self.numeroDocumento is not None
            or self.codigo is not None
            or self.codTributo is not None
            or self.montoDescu is not None
            or self.ventaNoSuj is not None
            or self.ventaExenta is not None
            or self.ventaGravada is not None
            or self.tributos is not None
        ):
            return True
        else:
            return False

    def export(
        self, outfile, level, namespace_='', name_='Item', namespacedef_='', pretty_print=True, enu=None, tam=None
    ):
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
            bytes(
                (
                    '%s%s'
                    % (
                        namespace_,
                        namespacedef_ and ' ' + namespacedef_ or '',
                    )
                ).encode()
            )
        )
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

    def exportChildren(self, outfile, level, namespace_='', name_='EmisorType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.numItem is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"numItem":%s,%s'
                        % (self.gds_encode(self.gds_format_string(quote_xml(self.numItem), input_name='NumItem')), eol_)
                    ).encode()
                )
            )
        if self.tipoItem is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"tipoItem":%s,%s'
                        % (
                            self.gds_encode(self.gds_format_string(quote_xml(self.tipoItem), input_name='TipoItem')),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.numeroDocumento is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"numeroDocumento":"%s",%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(
                                    quote_xml(self.numeroDocumento), input_name='Número de documento relacionado'
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"numeroDocumento":null,%s' % eol_).encode()))
        if self.descripcion is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"descripcion":"%s",%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(quote_xml(self.descripcion), input_name='Descripcion')
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.cantidad is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"cantidad":%s,%s'
                        % (
                            self.gds_encode(self.gds_format_string(quote_xml(self.cantidad), input_name='Cantidad')),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.codigo is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"codigo":"%s",%s'
                        % (self.gds_encode(self.gds_format_string(quote_xml(self.codigo), input_name='Código')), eol_)
                    ).encode()
                )
            )
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"codigo":null,%s' % eol_).encode()))
        if self.codTributo is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"codTributo":"%s",%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(
                                    quote_xml(self.codTributo), input_name='Tributo sujeto a cálculo de IVA'
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"codTributo":null,%s' % eol_).encode()))
        if self.uniMedida is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"uniMedida":%s,%s'
                        % (self.gds_encode(self.gds_format_integer(self.uniMedida, input_name='UniMedida')), eol_)
                    ).encode()
                )
            )
        if self.precioUni is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"precioUni":%s,%s'
                        % (self.gds_encode(self.gds_format_float(self.precioUni, input_name='PrecioUni')), eol_)
                    ).encode()
                )
            )
        if self.montoDescu is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"montoDescu":%s,%s'
                        % (
                            self.gds_encode(
                                self.gds_format_float(
                                    self.montoDescu, input_name='Descuento, Bonificación, Rebajas por ítem'
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.ventaNoSuj is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"ventaNoSuj":%s,%s'
                        % (
                            self.gds_encode(self.gds_format_float(self.ventaNoSuj, input_name='Ventas no Sujetas')),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.ventaExenta is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"ventaExenta":%s,%s'
                        % (
                            self.gds_encode(self.gds_format_float(self.ventaExenta, input_name='Ventas no Sujetas')),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.ventaGravada is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"ventaGravada":%s,%s'
                        % (
                            self.gds_encode(self.gds_format_float(self.ventaGravada, input_name='Ventas Gravadas')),
                            eol_,
                        )
                    ).encode()
                )
            )
        if len(self.tributos):
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '%s"%s":%s'
                        % (
                            namespace_,
                            'tributos',
                            ' ' + '',
                        )
                    ).encode()
                )
            )

            outfile.write(bytes(('[%s' % (eol_,)).encode()))
            showIndent(outfile, level, pretty_print)
            for tributo_ in self.tributos:
                showIndent(outfile, level, pretty_print)
                outfile.write(
                    bytes(
                        (
                            '"%s"%s'
                            % (
                                self.gds_encode(
                                    self.gds_format_string(
                                        quote_xml(tributo_), input_name='Número de documento relacionado'
                                    )
                                ),
                                eol_,
                            )
                        ).encode()
                    )
                )
                showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('%s]%s' % (namespace_, eol_)).encode()))
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tributos":null%s' % eol_).encode()))


class Resumen(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(
        self,
        totalNoSuj=0.00,
        totalLetras=None,
        ivaRete1=0.00,
        subTotalVentas=0.00,
        subTotal=0.00,
        reteRenta=0.00,
        descuExenta=0.00,
        totalDescu=0.00,
        tributos=None,
        descuGravada=0.00,
        totalGravada=0.00,
        montoTotalOperacion=0.00,
        ivaPerci1=0.00,
        totalExenta=0.00,
        descuNoSuj=0.00,
        condicionOperacion=None,
        numPagoElectronico=None,
    ):
        self.original_tagname_ = None
        self.totalNoSuj = totalNoSuj
        self.ivaPerci1 = ivaPerci1
        self.totalLetras = totalLetras
        self.ivaRete1 = ivaRete1
        self.subTotalVentas = subTotalVentas
        self.subTotal = subTotal
        self.reteRenta = reteRenta
        self.tributos = tributos
        self.descuExenta = descuExenta
        self.totalDescu = totalDescu
        self.descuGravada = descuGravada
        self.totalGravada = totalGravada
        self.montoTotalOperacion = montoTotalOperacion
        self.totalExenta = totalExenta
        self.descuNoSuj = descuNoSuj
        self.condicionOperacion = condicionOperacion
        self.numPagoElectronico = numPagoElectronico

    def set_totalLetras(self, totalLetras):
        self.totalLetras = totalLetras

    def get_totalLetras(self):
        return self.totalLetras

    def get_totalGravada(self):
        return self.totalGravada

    def set_totalGravada(self, totalGravada):
        self.totalGravada = totalGravada

    def get_subTotalVentas(self):
        return self.subTotalVentas

    def set_subTotalVentas(self, subTotalVentas):
        self.subTotalVentas = subTotalVentas

    def get_subTotal(self):
        return self.subTotal

    def set_subTotal(self, subTotal):
        self.subTotal = subTotal

    def get_tributos(self):
        return self.tributos

    def set_tributos(self, tributos):
        self.tributos = tributos

    def get_montoTotalOperacion(self):
        return self.montoTotalOperacion

    def set_montoTotalOperacion(self, montoTotalOperacion):
        self.montoTotalOperacion = montoTotalOperacion

    def set_totalExenta(self, totalExenta):
        self.totalExenta = totalExenta

    def get_totalExenta(self):
        return self.totalExenta

    def set_ivaRete1(self, ivaRete1):
        self.ivaRete1 = ivaRete1

    def get_ivaRete1(self):
        return self.ivaRete1

    def set_totalDescu(self, totalDescu):
        self.totalDescu = totalDescu

    def get_totalDescu(self):
        return self.totalDescu

    def set_condicionOperacion(self, condicionOperacion):
        self.condicionOperacion = condicionOperacion

    def get_condicionOperacion(self):
        return self.condicionOperacion

    def hasContent_(self):
        if (
            self.totalNoSuj is not None
            or self.ivaPerci1 is not None
            or self.totalLetras is not None
            or self.ivaRete1 is not None
            or self.subTotalVentas is not None
            or self.subTotal is not None
            or self.reteRenta is not None
            or self.tributos is not None
            or self.descuExenta is not None
            or self.descuGravada is not None
            or self.totalDescu is not None
            or self.totalGravada is not None
            or self.montoTotalOperacion is not None
            or self.totalExenta is not None
            or self.descuNoSuj is not None
            or self.condicionOperacion is not None
            or self.numPagoElectronico is not None
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
            bytes(
                (
                    '%s"%s":%s'
                    % (
                        namespace_,
                        name_,
                        namespacedef_ and ' ' + namespacedef_ or '',
                    )
                ).encode()
            )
        )
        if self.hasContent_():
            outfile.write(bytes(('{%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Identificacion', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
            outfile.write(bytes(('%s},%s' % (namespace_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportChildren(self, outfile, level, namespace_='', name_='EmisorType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.totalNoSuj is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"totalNoSuj":%s,%s'
                        % (
                            self.gds_encode(
                                self.gds_format_float(self.totalNoSuj, input_name='Total de Operaciones no sujetas')
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.totalExenta is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"totalExenta":%s,%s'
                        % (
                            self.gds_encode(
                                self.gds_format_float(self.totalExenta, input_name='Total de Operaciones exentas')
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.descuNoSuj is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"descuNoSuj":%s,%s'
                        % (
                            self.gds_encode(
                                self.gds_format_float(
                                    self.descuNoSuj,
                                    input_name='Monto global de Descuento, Bonificación, Rebajas y otros a ventas no sujetas',
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.descuExenta is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"descuExenta":%s,%s'
                        % (
                            self.gds_encode(
                                self.gds_format_float(
                                    self.descuExenta,
                                    input_name='Monto global de Descuento, Bonificación, Rebajas y otros a ventas exentas',
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.descuGravada is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"descuGravada":%s,%s'
                        % (
                            self.gds_encode(
                                self.gds_format_float(
                                    self.descuExenta,
                                    input_name='Monto global de Descuento, Bonificación, Rebajas y otros a ventas gravadas',
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.totalDescu is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"totalDescu":%s,%s'
                        % (
                            self.gds_encode(
                                self.gds_format_float(
                                    self.totalDescu, input_name='Total del monto de Descuento, Bonificación, Rebajas'
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.tributos is not None:
            self.tributos.export(outfile, level, namespace_, name_='tributos', pretty_print=pretty_print)
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tributos":null%s' % eol_).encode()))
        if self.totalLetras is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"totalLetras":"%s",%s'
                        % (
                            self.gds_encode(self.gds_format_string(quote_xml(self.totalLetras), input_name='Version')),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.subTotalVentas is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"subTotalVentas":%s,%s'
                        % (
                            self.gds_encode(
                                self.gds_format_float(
                                    self.subTotalVentas, input_name='Suma de operaciones sin impuestos'
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.subTotal is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"subTotal":%s,%s'
                        % (self.gds_encode(self.gds_format_float(self.subTotal, input_name='Sub-Total')), eol_)
                    ).encode()
                )
            )
        if self.ivaPerci1 is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"ivaPerci1":%s,%s'
                        % (self.gds_encode(self.gds_format_float(self.ivaPerci1, input_name='Sub-Total')), eol_)
                    ).encode()
                )
            )
        if self.ivaRete1 is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"ivaRete1":%s,%s'
                        % (self.gds_encode(self.gds_format_float(self.ivaRete1, input_name='IVA Retenido')), eol_)
                    ).encode()
                )
            )
        if self.reteRenta is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"reteRenta":%s,%s'
                        % (self.gds_encode(self.gds_format_float(self.reteRenta, input_name='Retención Renta')), eol_)
                    ).encode()
                )
            )
        if self.montoTotalOperacion is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"montoTotalOperacion":%s,%s'
                        % (
                            self.gds_encode(
                                self.gds_format_float(
                                    self.montoTotalOperacion, input_name='Monto Total de la Operación'
                                )
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.totalGravada is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"totalGravada":%s,%s'
                        % (
                            self.gds_encode(
                                self.gds_format_float(self.totalGravada, input_name='Total de Operaciones Gravadas')
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.condicionOperacion is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"condicionOperacion":%s,%s'
                        % (
                            self.gds_encode(
                                self.gds_format_integer(self.condicionOperacion, input_name='Condición de la Operación')
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.numPagoElectronico is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"numPagoElectronico":%s%s'
                        % (
                            self.gds_encode(
                                self.gds_format_integer(self.condicionOperacion, input_name='Condición de la Operación')
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"numPagoElectronico":null%s' % eol_).encode()))


class Tributos(GeneratedsSuper):
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
        if self.Item:
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
            bytes(
                (
                    '%s"%s":%s'
                    % (
                        namespace_,
                        name_,
                        namespacedef_ and ' ' + namespacedef_ or '',
                    )
                ).encode()
            )
        )
        if self.hasContent_():
            outfile.write(bytes(('[%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Identificacion', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
            outfile.write(bytes(('%s],%s' % (namespace_, eol_)).encode()))
        else:
            # outfile.write(bytes(('/>%s' % (eol_,)).encode()))
            outfile.write(bytes(('null,%s' % eol_).encode()))

    def exportChildren(
        self, outfile, level, namespace_='', name_='DetalleServicioType', fromsubclass_=False, pretty_print=True
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for i, LineaItem_ in enumerate(self.Item, 1):
            LineaItem_.export(
                outfile, level, namespace_, name_='Item', pretty_print=pretty_print, enu=i, tam=len(self.Item)
            )


class Tributo(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, codigo=None, descripcion=None, valor=None):
        self.original_tagname_ = None
        self.codigo = codigo
        self.descripcion = descripcion
        self.valor = valor

    def get_codigo(self):
        return self.codigo

    def set_codigo(self, codigo):
        self.codigo = codigo

    def get_descripcion(self):
        return self.descripcion

    def set_descripcion(self, descripcion):
        self.descripcion = descripcion

    def get_valor(self):
        return self.valor

    def set_valor(self, valor):
        self.valor = valor

    def hasContent_(self):
        if self.codigo is not None or self.descripcion is not None or self.valor is not None:
            return True
        else:
            return False

    def export(
        self, outfile, level, namespace_='', name_='Item', namespacedef_='', pretty_print=True, enu=None, tam=None
    ):
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
            bytes(
                (
                    '%s%s'
                    % (
                        namespace_,
                        namespacedef_ and ' ' + namespacedef_ or '',
                    )
                ).encode()
            )
        )
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

    def exportChildren(self, outfile, level, namespace_='', name_='EmisorType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.codigo is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"codigo":"%s",%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(quote_xml(self.codigo), input_name='Resumen Código de Tributo')
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.descripcion is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"descripcion":"%s",%s'
                        % (
                            self.gds_encode(
                                self.gds_format_string(quote_xml(self.descripcion), input_name='Nombre del Tributo')
                            ),
                            eol_,
                        )
                    ).encode()
                )
            )
        if self.valor is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(
                    (
                        '"valor":%s%s'
                        % (self.gds_encode(self.gds_format_float(self.valor, input_name='Valor del Tributo')), eol_)
                    ).encode()
                )
            )
