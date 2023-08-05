reduced_binary_coding
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy| |code_climate_maintainability| |pip| |downloads|

Python package implementing reduced binary coding.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install reduced_binary_coding

Tests Coverage
----------------------------------------------
Since some software handling coverages sometime get slightly different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|

Usage example
----------------------------------------------

.. code:: python

    from reduced_binary_coding import reduced_binary_coding

    reduced_binary_coding(3) # 00
    reduced_binary_coding(11) # 100

.. |travis| image:: https://travis-ci.org/LucaCappelletti94/reduced_binary_coding.png
   :target: https://travis-ci.org/LucaCappelletti94/reduced_binary_coding
   :alt: Travis CI build

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_reduced_binary_coding&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_reduced_binary_coding
    :alt: SonarCloud Quality

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_reduced_binary_coding&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_reduced_binary_coding
    :alt: SonarCloud Maintainability

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_reduced_binary_coding&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_reduced_binary_coding
    :alt: SonarCloud Coverage

.. |coveralls| image:: https://coveralls.io/repos/github/LucaCappelletti94/reduced_binary_coding/badge.svg?branch=master
    :target: https://coveralls.io/github/LucaCappelletti94/reduced_binary_coding?branch=master
    :alt: Coveralls Coverage

.. |pip| image:: https://badge.fury.io/py/reduced-binary-coding.svg
    :target: https://badge.fury.io/py/reduced-binary-coding
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/reduced-binary-coding
    :target: https://pepy.tech/badge/reduced-binary-coding
    :alt: Pypi total project downloads 

.. |codacy|  image:: https://api.codacy.com/project/badge/Grade/d9d93f8e0ee44844837a9126e0b8be38
    :target: https://www.codacy.com/manual/LucaCappelletti94/reduced_binary_coding?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LucaCappelletti94/reduced_binary_coding&amp;utm_campaign=Badge_Grade
    :alt: Codacy Maintainability

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/cfb705a5b387a0636ad8/maintainability
    :target: https://codeclimate.com/github/LucaCappelletti94/reduced_binary_coding/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/cfb705a5b387a0636ad8/test_coverage
    :target: https://codeclimate.com/github/LucaCappelletti94/reduced_binary_coding/test_coverage
    :alt: Code Climate Coverate