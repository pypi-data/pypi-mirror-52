#!/usr/bin/env python
# coding: utf-8

# In[1]:


with __import__("importnb").Notebook():
    try:
        from . import rdflib_patch
    except:
        import rdflib_patch
import rdflib, pandas, pydantic, jsonschema, json, abc, networkx, itertools, dataclasses, requests, typing, collections, requests_cache, inspect, IPython, pyld.jsonld as jsonld, abc
from toolz.curried import *
from rdflib.namespace import OWL, RDF, RDFS, SKOS, DC, DCTERMS

requests_cache.install_cache("rdf")
__all__ = tuple("Graph CC RDFS HYDRA OWL XHTML RDF XS XSD SW".split())


# In[2]:


if "field_class_to_schema_enum_enabled" not in globals():
    field_class_to_schema_enum_enabled = (
        pydantic.schema.field_class_to_schema_enum_enabled
    )


# Meta classes hold linked data types in their annotations.
#
# The class of the meta class stores the python type annotations.

# In[3]:


def split(object):
    ns, sep, pointer = object.rpartition("/#"["#" in object])
    return ns + sep, pointer


# Load in a bunch of namespaces.

# In[4]:


Graph = rdflib.ConjunctiveGraph()

for cls in (
    rdflib.namespace.RDF,
    rdflib.namespace.RDFS,
    rdflib.namespace.OWL,
    "https://www.w3.org/ns/prov.ttl",
    "http://schema.org/version/latest/schema.ttl",
    "https://raw.githubusercontent.com/AKSW/RDB2RDF-Seminar/master/sparqlmap/eclipse/workspace/xturtle.core/xsd.ttl",
):
    Graph.parse(data=requests.get(str(cls)).text, format="ttl")
Graph.parse(
    data=json.dumps(
        jsonld.expand(requests.get("https://www.w3.org/ns/hydra/core").json())
    ),
    format="json-ld",
)
Graph.parse(
    data=requests.get("http://www.w3.org/2003/06/sw-vocab-status/ns#").text,
    format="xml",
)
Graph.parse(
    data=requests.get("https://creativecommons.org/schema.rdf").text, format="xml"
)


# Create namespaces in python to provide improved interaction and predictin.

# In[5]:


namespaces = pipe(
    Graph,
    concat,
    filter(flip(isinstance)(rdflib.URIRef)),
    filter(flip(str.startswith)("http")),
    set,
    groupby(compose(first, split)),
    valmap(compose(list, map(compose(second, split)))),
    itemmap(lambda x: (rdflib.URIRef(x[0]), rdflib.namespace.ClosedNamespace(*x))),
)
CC = namespaces[rdflib.term.URIRef("http://creativecommons.org/ns#")]
RDFS = namespaces[rdflib.term.URIRef("http://www.w3.org/2000/01/rdf-schema#")]
HYDRA = namespaces[rdflib.term.URIRef("http://www.w3.org/ns/hydra/core#")]
OWL = namespaces[rdflib.term.URIRef("http://www.w3.org/2002/07/owl#")]
XHTML = namespaces[rdflib.term.URIRef("http://www.w3.org/1999/xhtml/vocab#")]
RDF = namespaces[rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#")]
XSD = namespaces[rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema#")]
XS = namespaces[rdflib.term.URIRef("http://www.w3.org/2001/XMLSchema-datatypes#")]
SW = namespaces[rdflib.term.URIRef("http://www.w3.org/2003/06/sw-vocab-status/ns#")]
SCHEMA = namespaces[rdflib.term.URIRef("http://schema.org/")]
PROV = namespaces[rdflib.term.URIRef("http://www.w3.org/ns/prov#")]


# In[6]:


class WebType:
    """Base class for creating pythonic semantic types with pydantic."""

    @classmethod
    def schema(cls):
        return cls.__pydantic_model__.schema(cls)

    def __get_validators__():
        return []

    def dict(self, **ctx):
        object = {
            "@context": ctx,
            **{
                k: v.dict(**(ctx and v.__context__ or {}))
                if isinstance(v, WebType)
                else v
                for k, v in [
                    (x, getattr(self, x))
                    for x in self.__context__
                    if getattr(self, x, None) is not None
                ]
            },
        }
        for k, v in object.items():
            try:
                jsonschema.validate(
                    v,
                    {
                        "anyOf": [
                            {"type": "string", "format": "uri"},
                            {"type": "string", "format": "json-pointer"},
                        ]
                    },
                    format_checker=jsonschema.draft7_format_checker,
                )
                object["@context"][k] = {"@type": "@id", "@id": object["@context"][k]}
            except jsonschema.ValidationError:
                ...
        return object

    def metadata(self):
        return jsonld.expand(self.dict(**self.__context__))


# Create some basic semantic classes to illustrate the process.

# In[7]:


types = {}

types[RDFS.Resource] = type(
    second(split(RDFS.Resource)),
    (WebType,),
    {
        "__doc__": "".join(Graph[RDFS.Resource, RDFS.comment]),
        "__context__": pipe(
            Graph[:, RDFS.domain, RDFS.Resource]
            + Graph[:, SCHEMA.domainIncludes, RDFS.Resource],
            map(juxt(compose(second, split), identity)),
            dict,
        ),
        "type": RDFS.Resource,
        "subject": Graph[RDFS.Resource],
        "object": Graph[:, :, RDFS.Resource],
    },
)
types[RDFS.Class] = type(
    second(split(RDFS.Class)),
    (types[RDFS.Resource],),
    {
        "__doc__": "".join(Graph[RDFS.Class, RDFS.comment]),
        "__context__": pipe(
            Graph[:, RDFS.domain, RDFS.Class]
            + Graph[:, SCHEMA.domainIncludes, RDFS.Class],
            map(juxt(compose(second, split), identity)),
            dict,
        ),
        "type": RDFS.Class,
        "subject": Graph[RDFS.Class],
        "object": Graph[:, :, RDFS.Class],
    },
)


def get(type):
    if type not in types:
        subject = Graph[type]
        object = Graph[:, :, type]
        __annotations__ = {}
        bases = pipe(
            subject,
            filter(
                compose(
                    {RDFS.subPropertyOf, RDFS.subClassOf, RDF.type}.__contains__, first
                )
            ),
            map(last),
            map(get),
            set,
            tuple,
        ) or (get(RDFS.Resource),)
        __context__ = pipe(
            Graph[:, RDFS.domain, type] + Graph[:, SCHEMA.domainIncludes, type],
            map(juxt(compose(second, split), identity)),
            dict,
        )
        types[type] = __import__("builtins").type(
            second(split(type)),
            tuple(sorted(bases, key=lambda x: list(types).index(x.type), reverse=True)),
            {"__doc__": "".join(Graph[type, RDFS.comment]), **locals()},
        )
        types[type].__context__ = pipe(
            types[type],
            inspect.getmro,
            map(lambda x: getattr(x, "__context__", {})),
            lambda x: collections.ChainMap(*x),
            dict,
        )
    return types[type]


def generate(type):
    object = get(type)
    pipe({**types}, valmap(annotate))
    return object


# Pydantic reads from annotations, `annotate` composes them below.

# In[8]:


def annotate(cls):
    """Add type annotations from the context."""
    if not hasattr(cls, "__annotations__"):
        cls.__annotations__ = {}
    if cls.__annotations__:
        return cls
    pipe(
        cls.__context__,
        valmap(lambda x: Graph[x, RDFS.range] + Graph[x, SCHEMA.rangeIncludes]),
        cls.__annotations__.update,
    )
    pipe(cls.__annotations__, dict.values, concat, set, map(get), list)
    pipe(
        cls.__annotations__,
        valmap(
            lambda x: pipe(
                x, map(types.get), tuple, (str,).__add__, typing.Union.__getitem__
            )
        ),
        cls.__annotations__.update,
    )
    cls.__annotations__ = {
        "value": cls.__annotations__.pop("value"),
        **cls.__annotations__,
        "type": cls.__annotations__.pop("type"),
    }
    [setattr(cls, x, getattr(cls, x, None)) for x in cls.__context__]
    pydantic.dataclasses.dataclass(cls)
    return cls


# We'll need a `pydantic.schema` for our types.

# In[9]:


if "field_class_to_schema_enum_enabled" not in globals():
    field_class_to_schema_enum_enabled = (
        pydantic.schema.field_class_to_schema_enum_enabled
    )
pydantic.schema.field_class_to_schema_enum_enabled = (
    (get(RDFS.Resource), {}),
) + field_class_to_schema_enum_enabled


# # Describe the iris data in a dataframe

# In[11]:


dataset, thing = map(generate, (SCHEMA.Dataset, SCHEMA.Thing))
print(dataset, dataset.type)


# Load the iris dataset from sklearn in pandas using functional programming syntax.

# In[12]:


import sklearn.datasets, pandas

df = pipe(
    sklearn.datasets.load_iris(),
    juxt(*map(operator.itemgetter, "data target feature_names".split())),
    lambda x: pandas.DataFrame(*x),
)


# Enrich the dataframe with semantic information.

# In[13]:


df.T.pipe(
    display,
    metadata={
        "@graph": dataset(
            identifier="/iris.csv",
            comment="""Fisher's iris data""",
            sameAs="https://www.wikidata.org/wiki/Q4203254",
            subjectOf=[
                thing(
                    identifier="""
https://nbviewer.jupyter.org/github/justmarkham/scikit-learn-videos/blob/283ef07cc5f0e88f6fbf4dcb071a611158eeea21/03_getting_started_with_iris.ipynb
https://en.wikipedia.org/wiki/Iris_flower_data_set
    """.strip().splitlines()
                )
            ],
        ).metadata()
    },
)


# Now the metadata is encoded directly into the notebook output.  The expansion describes what we can recover with an unnesting syntax.

# In[14]:


jsonld.expand(
    pandas.read_json("namespaces.ipynb", typ=pandas.Series).to_dict(),
    options={
        "expandContext": {x: "@nest" for x in "cells outputs metadata data".split()}
    },
)


# #### Alternatively, the semantic data can be encoded in a dataframe.

# In[15]:


df = (
    pandas.DataFrame(
        jsonld.flatten(
            pandas.read_json("namespaces.ipynb", typ=pandas.Series).to_dict(),
            options={
                "expandContext": {
                    x: "@nest" for x in "cells outputs metadata data".split()
                }
            },
        )
    )
    .set_index("@id")
    .stack()
    .apply(pandas.Series)
    .stack()
    .apply(pandas.Series)
)
df.T
