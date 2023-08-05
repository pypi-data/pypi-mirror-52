#!/usr/local/bin/python
# encoding: utf-8
"""
*import the ZTF stream into the marshall*

:Author:
    David Young

:Date Created:
    August 19, 2019
"""
################# GLOBAL IMPORTS ####################
import sys
import os
os.environ['TERM'] = 'vt100'
from fundamentals import tools
from ..data import data as basedata
from astrocalc.times import now


class data(basedata):
    """
    *Import the ZTF transient data into the marshall database*

    **Key Arguments:**
        - ``log`` -- logger
        - ``dbConn`` -- the marshall database connection
        - ``settings`` -- the settings dictionary

    **Usage:**

        To setup your logger, settings and database connections, please use the ``fundamentals`` package (`see tutorial here <http://fundamentals.readthedocs.io/en/latest/#tutorial>`_). 

        To initiate a data object, use the following:

        .. code-block:: python 

            from marshallEngine.feeders.ztf.data import data
            ingester = data(
                log=log,
                settings=settings,
                dbConn=dbConn
            ).ingest(withinLastDays=withInLastDay)   
    """
    # Initialisation

    def __init__(
            self,
            log,
            dbConn,
            settings=False,
    ):
        self.log = log
        log.debug("instansiating a new 'data' object")
        self.settings = settings
        self.dbConn = dbConn

        self.fsTableName = "fs_ztf"
        self.survey = "ZTF"

        # xt-self-arg-tmpx

        return None

    def ingest(
            self,
            withinLastDays):
        """*Ingest the data into the marshall feeder survey table*

        **Key Arguments:**
            - ``withinLastDays`` -- within the last number of days. *Default: 50*
        """
        self.log.debug('starting the ``ingest`` method')

        allLists = []

        # MIGHT NEED SOMETHING LIKE THIS ... OTHERWISE DELETE AND ADD ANOTHER IMPORT METHOD
        # csvDicts = self.get_csv_data(
        #     url=self.settings["panstarrs urls"]["ps13pi"]["summary csv"],
        #     user=self.settings["credentials"]["ps13pi"]["username"],
        #     pwd=self.settings["credentials"]["ps13pi"]["password"]
        # )
        # allLists.extend(self._clean_data_pre_ingest(
        #     surveyName="ps13pi", withinLastDays=withinLastDays))

        self.dictList = allLists
        self._import_to_feeder_survey_table()

        self.insert_into_transientBucket()

        self.log.debug('completed the ``ingest`` method')
        return None

    def _clean_data_pre_ingest(
            self,
            surveyName,
            withinLastDays=False):
        """*clean up the list of dictionaries containing the ZTF data, pre-ingest*

        **Key Arguments:**
            - ``surveyName`` -- the ZTF survey name
            -  ``withinLastDays`` -- the lower limit of observations to include (within the last N days from now). Default *False*, i.e. no limit

        **Return:**
            - ``dictList`` -- the cleaned list of dictionaries ready for ingest

        **Usage:**

            To clean the data from the ZTF survey:

            .. code-block:: python 

                dictList = ingesters._clean_data_pre_ingest(surveyName="ZTF")

            Note you will also be able to access the data via ``ingester.dictList``
        """
        self.log.debug('starting the ``_clean_data_pre_ingest`` method')

        self.dictList = []

        # CALC MJD LIMIT
        if withinLastDays:
            mjdLimit = now(
                log=self.log
            ).get_mjd() - float(withinLastDays)

        for row in self.csvDicts:
            # IF NOW IN THE LAST N DAYS - SKIP
            if withinLastDays and float(row["mjd_obs"]) < mjdLimit:
                continue

            # MASSAGE THE DATA IN THE INPT FORMAT TO WHAT IS NEEDED IN THE
            # FEEDER SURVEY TABLE IN THE DATABASE
            thisDictionary = {}
            # thisDictionary["candidateID"] = row["ps1_designation"]
            # ...

            self.dictList.append(thisDictionary)

        self.log.debug('completed the ``_clean_data_pre_ingest`` method')
        return self.dictList

    # use the tab-trigger below for new method
    # xt-class-method
