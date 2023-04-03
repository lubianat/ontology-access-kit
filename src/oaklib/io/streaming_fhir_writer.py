import logging
from dataclasses import dataclass
from typing import Iterable

from linkml_runtime.dumpers import json_dumper

from oaklib.converters.obo_graph_to_fhir_converter import OboGraphToFhirJsonConverter
from oaklib.datamodels.obograph import GraphDocument
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.io.streaming_writer import StreamingWriter
from oaklib.types import CURIE


@dataclass
class StreamingFhirJsonWriter(StreamingWriter):
    """
    A writer that emits FHIR CodeSystem objects or Concept objects
    """

    def emit_multiple(self, entities: Iterable[CURIE], **kwargs):
        oi = self.ontology_interface
        if isinstance(oi, OboGraphInterface):
            logging.info("Extracting graph")
            g = oi.extract_graph(list(entities), include_metadata=True)
            gd = GraphDocument(graphs=[g])
            logging.info(f"Converting {len(g.nodes)} nodes to OBO")
            converter = OboGraphToFhirJsonConverter()
            converter.curie_converter = oi.converter
            code_system = converter.convert(gd)
            logging.info(f"Writing {len(code_system.concept)} Concepts")
            # TODO: Should not this call OboGraphToFhirJsonConverter.dump()?
            self.file.write(json_dumper.dumps(code_system))
        else:
            super().emit_multiple(entities, **kwargs)


# TODO:
@dataclass
class StreamingFhirNpmWriter(StreamingWriter):
    """
    A writer that emits FHIR CodeSystem objects or Concept objects
    """

    def emit_multiple(self, entities: Iterable[CURIE], **kwargs):
        oi = self.ontology_interface
        if isinstance(oi, OboGraphInterface):
            logging.info("Extracting graph")
            g = oi.extract_graph(list(entities), include_metadata=True)
            gd = GraphDocument(graphs=[g])
            logging.info(f"Converting {len(g.nodes)} nodes to OBO")
            converter = None
            print(gd, converter)
        else:
            super().emit_multiple(entities, **kwargs)
