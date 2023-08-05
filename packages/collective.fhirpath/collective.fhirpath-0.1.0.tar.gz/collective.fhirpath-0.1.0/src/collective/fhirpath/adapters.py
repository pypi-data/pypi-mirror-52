# _*_ coding: utf-8 _*_
from .dialect import ElasticSearchDialect
from .engine import ElasticsearchEngine
from collective.elasticsearch.interfaces import IElasticSearchCatalog
from fhirpath.connectors.factory.es import ElasticsearchConnection
from fhirpath.enums import FHIR_VERSION
from fhirpath.interfaces import IElasticsearchEngineFactory
from fhirpath.interfaces import IEngine
from fhirpath.interfaces import IFhirSearch
from fhirpath.interfaces import ISearchContext
from fhirpath.interfaces import ISearchContextFactory
from fhirpath.search import fhir_search
from fhirpath.search import SearchContext
from zope.component import adapter
from zope.interface import implementer


__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"


def create_engine(es_catalog, fhir_version=None):
    """ """
    if fhir_version is None:
        fhir_version = FHIR_VERSION.DEFAULT
    if isinstance(fhir_version, str):
        fhir_version = FHIR_VERSION[fhir_version]

    def es_conn_factory(engine):
        return ElasticsearchConnection.from_prepared(engine.es_catalog.connection)

    def es_dialect_factory(engine):
        """ """
        return ElasticSearchDialect(connection=engine.connection)

    engine_ = ElasticsearchEngine(
        es_catalog, fhir_version, es_conn_factory, es_dialect_factory
    )

    return engine_


@implementer(IElasticsearchEngineFactory)
@adapter(IElasticSearchCatalog)
class ElasticsearchEngineFactory:
    """ """

    def __init__(self, es_catalog):
        """ """
        self.es_catalog = es_catalog

    def __call__(self, fhir_version=None):
        """ """
        return create_engine(self.es_catalog, fhir_version=fhir_version)


@implementer(ISearchContextFactory)
@adapter(IEngine)
class SearchContextFactory:
    """ """

    def __init__(self, engine):
        """ """
        self.engine = engine

    def get(self, resource_type, unrestricted=False):
        """ """
        return SearchContext(
            self.engine, resource_type, unrestricted=unrestricted, async_result=False
        )

    def __call__(self, resource_type, unrestricted=False):
        return self.get(resource_type, unrestricted)


@implementer(IFhirSearch)
@adapter(ISearchContext)
class FhirSearch:
    """ """

    def __init__(self, context):
        """ """
        self.context = context

    def __call__(self, params):
        """ """
        return fhir_search(self.context, params=params)
