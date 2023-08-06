from mapi.metadata.metadata_movie import MetadataMovie
from mapi.metadata.metadata_television import MetadataTelevision
from mapi.providers import API_ALL, API_MOVIE, API_TELEVISION, provider_factory

provider = input("provider? [%s]" % ",".join(API_ALL))

query = {}


def get_fields(options):
    for field in options:
        query[field] = input("%s? " % field).strip() or None


if provider in API_MOVIE:
    get_fields(MetadataMovie.fields_accepted - MetadataTelevision.fields_extra)
elif provider in API_TELEVISION:
    get_fields(
        MetadataTelevision.fields_accepted - MetadataTelevision.fields_extra
    )

provider = provider_factory(provider)
for result in provider.search(**query):
    print(result)
