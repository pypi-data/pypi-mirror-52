========================
Django Rest Framework HQ
========================

Filter Extensions and support for ElasticSearch

Change Log
----------

- 0.1.17  Sort range and terms aggregations fields representations on bucket name
- 0.1.16  Add metric_name as instance variable to range and terms aggregations fields
- 0.1.15  Add optional metric name for sub aggregation in terms and range aggregations
- 0.1.14  Pass TopHitsAggregationField' context to its child serializers
- 0.1.13  Tweak FunctionScore params so `origin` is scoped
- 0.1.12  Tweak FunctionScore geo params to allow decimal
- 0.1.11  Make GeoPointField writable
- 0.1.10  Updated ElasticsearchPagination.get_paginated_response to include get_related if exists
- 0.1.7   Added Aggregation Classes
- 0.1.6   Remove Exception Classes, Project specific
- 0.1.5   Add tests + removed MixedFilterBackend, MixedSerializerMixin. Project specific
- 0.1.4   Add max offset in ElasticsearchPagination
- 0.1.3   Raise parse error on invalid dates
- 0.1.2   Removed permission classes, Project specific
- 0.1.1   Removed _index from more_like_this (causing issue with ES2)
- 0.1.0   Imported
