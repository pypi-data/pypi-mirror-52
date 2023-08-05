unary_coding
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy| |code_climate_maintainability| |pip| |downloads|

Python package implementing unary coding.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install unary_coding

Tests Coverage
----------------------------------------------
Since some software handling coverages sometime get slightly different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|

Usage example
----------------------------------------------

.. code:: python

    from unary_coding import unary, inverted_unary

    unary(3) # 1110
    inverted_unary(3) # 0001


.. |travis| image:: https://travis-ci.org/LucaCappelletti94/unary_coding.png
   :target: https://travis-ci.org/LucaCappelletti94/unary_coding
   :alt: Travis CI build

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_unary_coding&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_unary_coding
    :alt: SonarCloud Quality

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_unary_coding&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_unary_coding
    :alt: SonarCloud Maintainability

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_unary_coding&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_unary_coding
    :alt: SonarCloud Coverage

.. |coveralls| image:: https://coveralls.io/repos/github/LucaCappelletti94/unary_coding/badge.svg?branch=master
    :target: https://coveralls.io/github/LucaCappelletti94/unary_coding?branch=master
    :alt: Coveralls Coverage

.. |pip| image:: https://badge.fury.io/py/unary-coding.svg
    :target: https://badge.fury.io/py/unary-coding
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/unary-coding
    :target: https://pepy.tech/badge/unary-coding
    :alt: Pypi total project downloads 

.. |codacy|  image:: https://api.codacy.com/project/badge/Grade/17059b2f32624dafbabd4cd7f06bd110
    :target: https://www.codacy.com/manual/LucaCappelletti94/unary_coding?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LucaCappelletti94/unary_coding&amp;utm_campaign=Badge_Grade
    :alt: Codacy Maintainability

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/0f26605f29cdd7fd3f77/maintainability
    :target: https://codeclimate.com/github/LucaCappelletti94/unary_coding/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/0f26605f29cdd7fd3f77/test_coverage
    :target: https://codeclimate.com/github/LucaCappelletti94/unary_coding/test_coverage
    :alt: Code Climate Coverate