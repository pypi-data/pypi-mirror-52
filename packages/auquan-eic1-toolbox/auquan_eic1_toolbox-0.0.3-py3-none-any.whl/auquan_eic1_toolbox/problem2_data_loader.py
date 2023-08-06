import numpy as np
from backtester.dataSource.data_source import DataSource
from backtester.instrumentUpdates import *
import os
from datetime import datetime
import csv
from backtester.logger import *
try:
    from urllib2 import urlopen, URLError
except ImportError:
    from urllib.request import urlopen, URLError
from functools import wraps
import time
import requests, zipfile, io

def retry(exceptions, tries=4, delay=3, backoff=2, logger=None):
    """
    Retry calling the decorated function using an exponential backoff.

    Args:
        exceptions: The exception to check. may be a tuple of
            exceptions to check.
        tries: Number of times to try (not retry) before giving up.
        delay: Initial delay between retries in seconds.
        backoff: Backoff multiplier (e.g. value of 2 will double the delay
            each retry).
        logger: Logger to use. If None, print.
    """
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    msg = '{}, Retrying in {} seconds...'.format(e, mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry

@retry(URLError, tries=4, delay=3, backoff=2)
def urlopen_with_retry(url):
    return urlopen(url)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class CsvDataSource(DataSource):
    def __init__(self, cachedFolderName, dataSetId, instrumentIds, downloadUrl = None, timeKey = None, timeStringFormat = None, startDateStr=None, endDateStr=None, liveUpdates=True, pad=True):
        self._cachedFolderName = cachedFolderName
        self._dataSetId = dataSetId
        self._downloadUrl = downloadUrl
        self._timeKey = timeKey
        self._timeStringFormat = timeStringFormat
        self.ensureDirectoryExists(self._cachedFolderName, self._dataSetId)
        self.ensureAllInstrumentsFile(dataSetId)
        super(CsvDataSource, self).__init__(cachedFolderName, dataSetId, instrumentIds, startDateStr, endDateStr)
        if liveUpdates:
            self._allTimes, self._groupedInstrumentUpdates = self.getGroupedInstrumentUpdates()
        else:
            self._allTimes, self._bookDataByInstrument = self.getAllInstrumentUpdates()
            self._bookDataFeatureKeys = list(self._bookDataByInstrument[self._instrumentIds[0]].columns)
            if pad:
                self.padInstrumentUpdates()
            if (startDateStr is not None) and (endDateStr is not None):
                self.filterUpdatesByDates([(startDateStr, endDateStr)])

    def getFileName(self, instrumentId):
        return self._cachedFolderName + self._dataSetId + '/' + instrumentId + '.csv'

    def ensureAllInstrumentsFile(self, dataSetId):
        stockListFileName = self._cachedFolderName + self._dataSetId + '/' + 'stock_list.txt'
        if os.path.isfile(stockListFileName):
            return True
        
        url = '%s/%s.zip' % (self._downloadUrl, self._dataSetId)
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(path = self._cachedFolderName)
        
        return True
        # url = ''
        # if self._dataSetId != '':
        #     url = '%s/%s/stock_list.txt' % (self._downloadUrl, self._dataSetId)
        # else:
        #     url = '%s/stock_list.txt' % (self._downloadUrl)
        # print(url)
        # response = urlopen_with_retry(url)
        # status = response.getcode()
        # if status == 200:
        #     print('Downloading list of stocks to file: %s' % (stockListFileName))
        #     with open(stockListFileName, 'w') as f:
        #         f.write(response.read().decode('utf8').replace('\r\n', '\n'))
        #     return True
        # else:
        #     logError('File not found. Please check internet')
        #     return False

    def getAllInstrumentIds(self):
        stockListFileName = self._cachedFolderName + self._dataSetId + '/' + 'stock_list.txt'
        if not os.path.isfile(stockListFileName):
            logError('Stock list file not present. Please try running again.')
            return []

        with open(stockListFileName) as f:
            content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content]
        return content

    def downloadFile(self, instrumentId, downloadLocation):
        url = ''
        if self._dataSetId != '':
            print(url)
            url = '%s/%s/%s.csv' % (self._downloadUrl, self._dataSetId, instrumentId)
        else:
            url = '%s/%s.csv' % (self._downloadUrl, instrumentId)

        response = urlopen_with_retry(url)
        status = response.getcode()
        if status == 200:
            print('Downloading %s data to file: %s' % (instrumentId, downloadLocation))
            with open(downloadLocation, 'w') as f:
                f.write(response.read().decode('utf8').replace('\r\n', '\n'))
            return True
        else:
            logError('Got Response code: %s'%str(status))
            return False

    def downloadAndAdjustData(self, instrumentId, fileName):
        if not os.path.isfile(fileName):
            if not self.downloadFile(instrumentId, fileName):
                logError('Skipping %s:' % (instrumentId))
                return False
        return True

    def getInstrumentUpdateFromRow(self, instrumentId, row):
        bookData = row
        for key in bookData:
            if is_number(bookData[key]):
                bookData[key] = float(bookData[key])
            elif bookData[key] == '':
                bookData[key] = np.nan
            # print(key, bookData[key])
        timeKey = self._timeKey
        timeOfUpdate = datetime.strptime(row[timeKey], self._timeStringFormat)
        bookData.pop(timeKey, None)
        inst = StockInstrumentUpdate(stockInstrumentId=instrumentId,
                                     tradeSymbol=instrumentId,
                                     timeOfUpdate=timeOfUpdate,
                                     bookData=bookData)
        # print(inst.getBookData())
        if self._bookDataFeatureKeys is None:
            self._bookDataFeatureKeys = bookData.keys()  # just setting to the first one we encounter
        return inst

if __name__ == "__main__":
    ds = CsvDataSource(cachedFolderName='historicalData/',
                             dataSetId='train',
                             instrumentIds=[],
                             downloadUrl = 'https://qq14-data.s3.us-east-2.amazonaws.com',
                             timeKey = 'datetime',
                             timeStringFormat = '%Y-%m-%d',
                             startDateStr='2008/03/31',
                             endDateStr='2008/03/31',
                             liveUpdates=True,
                             pad=True)
