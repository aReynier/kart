from django.test import TestCase

import graphene

from kart.schema import Query

from production.tests.factories import (
    EventFactory,
    PerformanceFactory,
    ArtworkFactory,
    KeywordFactory,
    FilmFactory,
    InstallationFactory
)

from people.tests.factories import ArtistFactory


class TestGQLPages(TestCase):
    """
    TODO: do tests
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_query_artworkx_panox(self):
        # create
        self.event = EventFactory()
        self.artist = ArtistFactory()
        self.performance = PerformanceFactory(authors=[self.artist])
        self.event.performances.add(self.performance)
        self.event.save()

        query = "query ArtworkXPanoX($expo: Int, $oeuvre: ID) {\
                    exhibition(id: $expo) {\
                        title\
                        artworkExhib(id: $oeuvre) {\
                            artwork {\
                                id\
                                title\
                                picture\
                                type\
                                descriptionFr\
                                descriptionEn\
                                thanksFr\
                                thanksEn\
                                productionDate\
                                inSituGalleries {\
                                    media {\
                                        picture }\
                                }\
                                authors {\
                                    id\
                                    displayName\
                                    firstName\
                                    lastName\
                                    bioFr\
                                    bioEn }\
                                partners {\
                                    name}\
                            }\
                            prevAlpha {\
                                id }\
                            nextAlpha {\
                                id}\
                        }\
                    }\
                }"
        schema = graphene.Schema(query=Query)
        result = schema.execute(query, variables={'expo': self.event.id, 'oeuvre': self.performance.id})
        self.assertIsNone(result.errors)

    def test_query_exhibx(self):
        event = EventFactory()
        artist = ArtistFactory()
        performance = PerformanceFactory(authors=[artist])
        event.performances.add(performance)
        event.save()

        query = 'query exhib($idExhib: Int) {\
                    exhibition(id: $idExhib) {\
                        artworks {\
                            id\
                            authors {\
                            id\
                            displayName\
                            }\
                        }\
                    }\
                }'
        schema = graphene.Schema(query=Query)
        result = schema.execute(query, variables={'idExhib': event.id, })
        self.assertIsNone(result.errors)

    def test_query_all_artworks_keywords(self):
        query = 'query ArtworksKeywords {\
                    artworks {\
                        keywords {\
                        name\
                        }\
                    }\
                }'
        schema = graphene.Schema(query=Query)
        result = schema.execute(query)
        self.assertIsNone(result.errors)

    def test_query_all_productions_artworks_keywords(self):
        query = 'query AllProductionsArtworksKeywords {\
                    productions {\
                        ... on ArtworkType {\
                            keywords {\
                                name\
                            }\
                        }\
                    }\
                }'
        schema = graphene.Schema(query=Query)
        result = schema.execute(query)
        self.assertIsNone(result.errors)

    def test_query_specific_artwork_keywords(self):
        artwork = ArtworkFactory()
        keyword = KeywordFactory()
        artwork.keywords.add(keyword)
        artwork.save()

        query = 'query ArtworkKeywords($artworkId: Int) {\
                    artwork(id: $artworkId) {\
                        keywords {\
                        name\
                        }\
                    }\
                }'
        schema = graphene.Schema(query=Query)
        result = schema.execute(query, variables={'artworkId': artwork.id})
        self.assertIsNone(result.errors)

    def test_query_specific_artwork_keywords_with_two_keywords(self):
        artwork = ArtworkFactory()
        firstKeyword = KeywordFactory(name='mythe')
        secondKeyword = KeywordFactory(name='société')
        artwork.keywords.add(firstKeyword, secondKeyword)
        artwork.save()

        query = 'query ArtworkKeywords($artworkId: Int) {\
                    artwork(id: $artworkId) {\
                        keywords {\
                        name\
                        }\
                    }\
                }'
        schema = graphene.Schema(query=Query)
        result = schema.execute(query, variables={'artworkId': artwork.id})
        assert result.data['artwork']['keywords'][0]['name'] == "mythe"
        assert result.data['artwork']['keywords'][1]['name'] == "société"
        self.assertIsNone(result.errors)

    # Following test about artworks query's production date
    def test_artworks_query_production_date(self):
        ArtworkFactory()

        query = 'query ArtworksProductionDate {\
                    artworks {\
                        productionDate\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artworks'][0]['productionDate'] is not None

    # following test about artworks filters
    def test_query_with_artworks_production_year_filter(self):
        artwork = ArtworkFactory(production_date="2019-01-01")
        artwork.save()

        query = 'query ArtworksFilters {\
                    artworksWithFilter(\
                        belongProductionYear: "2019"\
                    ) {\
                        keywords {\
                            name\
                        }\
                        productionDate\
                        type\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artworksWithFilter'][0]['productionDate'] == "2019-01-01"

    def test_query_with_artworks_keyword_filters(self):
        artwork = ArtworkFactory()
        firstKeyword = KeywordFactory(name='mythe')
        secondKeyword = KeywordFactory(name='société')
        artwork.keywords.add(firstKeyword, secondKeyword)
        artwork.save()

        query = 'query ArtworksFilters {\
                    artworksWithFilter(\
                        hasKeywordName: "mythe"\
                    ) {\
                        keywords {\
                            name\
                        }\
                        productionDate\
                        type\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artworksWithFilter'][0]['keywords'][0]['name'] == "mythe"

    def test_query_with_two_artworks_filters(self):
        artwork = ArtworkFactory(production_date="2019-01-01")
        firstKeyword = KeywordFactory(name='mythe')
        secondKeyword = KeywordFactory(name='société')
        artwork.keywords.add(firstKeyword, secondKeyword)
        artwork.save()

        query = 'query ArtworksFilters {\
                    artworksWithFilter(\
                        hasKeywordName: "mythe"\
                        belongProductionYear: "2019"\
                    ) {\
                        keywords {\
                            name\
                        }\
                        productionDate\
                        type\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artworksWithFilter'][0]['productionDate'] == "2019-01-01"

    def test_query_with_artworks_type_film_filters(self):
        FilmFactory()

        query = 'query ArtworksFilters {\
                    artworksWithFilter(\
                        hasType: "Film"\
                    ) {\
                        keywords {\
                            name\
                        }\
                        productionDate\
                        type\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artworksWithFilter'][0]['type'] == "Film"

    def test_query_with_artworks_type_installation_filters(self):
        InstallationFactory()

        query = 'query ArtworksFilters {\
                    artworksWithFilter(\
                        hasType: "Installation"\
                    ) {\
                        keywords {\
                            name\
                        }\
                        productionDate\
                        type\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artworksWithFilter'][0]['type'] == "Installation"

    def test_query_with_artworks_type_performance_filters(self):
        PerformanceFactory()

        query = 'query ArtworksFilters {\
                    artworksWithFilter(\
                        hasType: "Performance"\
                    ) {\
                        keywords {\
                            name\
                        }\
                        productionDate\
                        type\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artworksWithFilter'][0]['type'] == "Performance"

    def test_query_with_artworks_wrong_type_filters(self):
        FilmFactory()

        query = 'query ArtworksFilters {\
                    artworksWithFilter(\
                        hasType: "coucou"\
                    ) {\
                        keywords {\
                            name\
                        }\
                        productionDate\
                        type\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artworksWithFilter'] == []

    # Find out why this test doesn't work
    def test_query_with_all_artworks_filters(self):
        film = FilmFactory(production_date="2019-01-01")
        firstKeyword = KeywordFactory(name='mythe')
        secondKeyword = KeywordFactory(name='société')
        film.keywords.add(firstKeyword, secondKeyword)
        film.save()

        query = 'query ArtworksFilters {\
                    artworksWithFilter(\
                        belongProductionYear: "2019"\
                        hasKeywordName: "mythe"\
                        hasType: "Film"\
                    ) {\
                        keywords {\
                            name\
                        }\
                        productionDate\
                        type\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artworksWithFilter'][0]['productionDate'] == "2019-01-01"
        assert result.data['artworksWithFilter'][0]['keywords'][0]['name'] == "mythe"
        assert result.data['artworksWithFilter'][0]['type'] == "Film"
