golomb_coding
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy| |code_climate_maintainability| |pip| |downloads|

Python package implementing Golomb coding.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install golomb_coding

Tests Coverage
----------------------------------------------
Since some software handling coverages sometime get slightly different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|


Usage examples
----------------------------------------------
The coding available from this package are `golomb_coding`, `bernoulli_golomb_coding` and `optimal_golomb_coding`.
The following examples are usages of Golomb coding.

.. code:: python

    from golomb_coding import golomb_coding

    golomb_coding(0, 3) # 10
    golomb_coding(1, 3) # 110
    golomb_coding(2, 3) # 111
    golomb_coding(3, 3) # 010
    golomb_coding(4, 3) # 0110
    golomb_coding(5, 3) # 0111
    golomb_coding(6, 3) # 0010
    golomb_coding(7, 3) # 00110
    golomb_coding(8, 3) # 00111
    golomb_coding(9, 3) # 00010
    golomb_coding(10, 3) # 000110
    golomb_coding(11, 3) # 000111
    golomb_coding(12, 3) # 000010
    golomb_coding(13, 3) # 0000110
    golomb_coding(14, 3) # 0000111
    golomb_coding(15, 3) # 0000010


.. |travis| image:: https://travis-ci.org/LucaCappelletti94/golomb_coding.png
   :target: https://travis-ci.org/LucaCappelletti94/golomb_coding
   :alt: Travis CI build

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_golomb_coding&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_golomb_coding
    :alt: SonarCloud Quality

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_golomb_coding&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_golomb_coding
    :alt: SonarCloud Maintainability

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_golomb_coding&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_golomb_coding
    :alt: SonarCloud Coverage

.. |coveralls| image:: https://coveralls.io/repos/github/LucaCappelletti94/golomb_coding/badge.svg?branch=master
    :target: https://coveralls.io/github/LucaCappelletti94/golomb_coding?branch=master
    :alt: Coveralls Coverage

.. |pip| image:: https://badge.fury.io/py/golomb-coding.svg
    :target: https://badge.fury.io/py/golomb-coding
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/golomb-coding
    :target: https://pepy.tech/badge/golomb-coding
    :alt: Pypi total project downloads 

.. |codacy|  image:: https://api.codacy.com/project/badge/Grade/cb6aa47c254948e388b05a5dd8404c84
    :target: https://www.codacy.com/manual/LucaCappelletti94/golomb_coding?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LucaCappelletti94/golomb_coding&amp;utm_campaign=Badge_Grade
    :alt: Codacy Maintainability

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/67cf2724ca33dbcd33c4/maintainability
    :target: https://codeclimate.com/github/LucaCappelletti94/golomb_coding/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/67cf2724ca33dbcd33c4/test_coverage
    :target: https://codeclimate.com/github/LucaCappelletti94/golomb_coding/test_coverage
    :alt: Code Climate Coverate