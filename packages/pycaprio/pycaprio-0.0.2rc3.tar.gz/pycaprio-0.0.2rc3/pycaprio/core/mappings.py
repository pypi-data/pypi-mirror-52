DATE_FORMAT_ISO8601 = "%Y-%m-%dT%H:%M:%S%z"
NO_PROJECT = -1
NO_DOCUMENT = -1


class DocumentFormats:
    DEFAULT = 'webanno'
    WEBANNO = 'webanno'
    NIF = 'nif'
    LIF = 'lif'
    TEI = 'dkpro-core-tei'
    PERSEUS = 'perseus_2.1'
    CONLLU = 'conllu'
    TEXT = 'text'
    JSON = 'json'
    XMI = 'xmi'


class DocumentStatus:
    DEFAULT = 'NEW'
    NEW = 'NEW'
    LOCKED = 'LOCKED'
    IN_PROGRESS = 'IN-PROGRESS'
    COMPLETE = 'COMPLETE'


class AnnotationStatus:
    DEFAULT = 'ANNOTATION-IN-PROGRESS'
    ANNOTATION_IN_PROGRESS = 'ANNOTATION-IN-PROGRESS'
    ANNOTATION_COMPLETE = 'ANNOTATION-COMPLETE'
    CURATION_IN_PROGRESS = 'CURATION-IN-PROGRESS'
    CURATION_COMPLETE = 'CURATION-COMPLETE'
