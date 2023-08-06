from backtester.trading_system_parameters import TradingSystemParameters
from backtester.features.feature import Feature
from datetime import timedelta
from backtester.timeRule.nse_time_rule import CustomTimeRule
from backtester.orderPlacer.backtesting_order_placer import BacktestingOrderPlacer
from backtester.trading_system import TradingSystem
from backtester.version import updateCheck
from backtester.constants import *
from backtester.features.feature import Feature
from backtester.logger import *
import pandas as pd
import numpy as np
import sys
from sklearn import linear_model
from sklearn import metrics as sm
from auquan_eic1_toolbox.problem2_data_loader import CsvDataSource
from auquan_eic1_toolbox.problem2_execution_system import Problem2ExecutionSystem
from auquan_eic1_toolbox.problem2_time_rule import DayTimeRule
# from problem2_data_loader import CsvDataSource
# from problem2_execution_system import Problem2ExecutionSystem
# from problem2_time_rule import DayTimeRule
import copy

## Make your changes to the functions below.
## SPECIFY the symbols you are modeling for in getSymbolsToTrade() below
## You need to specify features you want to use in getInstrumentFeatureConfigDicts() and getMarketFeatureConfigDicts()
## and create your predictions using these features in getPrediction()

## Don't change any other function
## The toolbox does the rest for you, from downloading and loading data to running backtest


class MyTradingParams(TradingSystemParameters):
    '''
    initialize class
    place any global variables here
    '''
    def __init__(self, tradingFunctions):
        self.__tradingFunctions = tradingFunctions
        self.targetVariable = 'Y'
        self.__dataSetId = 'train'
        self.__instrumentIds = self.__tradingFunctions.getSymbolsToTrade()
        self.__priceKey = 'Share Price'
        self.__additionalInstrumentFeatureConfigDicts = []
        self.__additionalMarketFeatureConfigDicts = []
        self.__fees = {'brokerage': 0.0001,'spread': 0.05}
        self.__startDate = '2008/03/31'
        self.__endDate = '2019/03/31'
        self.features_list = list(pd.read_csv('features_list.txt', index_col=None, header=None)[0])
        super(MyTradingParams, self).__init__()


    '''
    Returns an instance of class DataParser. Source of data for instruments
    '''

    def getDataParser(self):
        instrumentIds = self.__tradingFunctions.getSymbolsToTrade()
        return CsvDataSource(cachedFolderName='historicalData/',
                             dataSetId=self.__dataSetId,
                             instrumentIds=instrumentIds,
                            #  downloadUrl = 'https://qq3-data.s3.ap-south-1.amazonaws.com',
                             downloadUrl = 'https://qq14-data.s3.us-east-2.amazonaws.com',
                             timeKey = 'datetime',
                             timeStringFormat = '%Y-%m-%d',
                             startDateStr=self.__startDate,
                             endDateStr=self.__endDate,
                             liveUpdates=True,
                             pad=True)

    '''
    Returns an instance of class TimeRule, which describes the times at which
    we should update all the features and try to execute any trades based on
    execution logic.
    For eg, for intra day data, you might have a system, where you get data
    from exchange at a very fast rate (ie multiple times every second). However,
    you might want to run your logic of computing features or running your execution
    system, only at some fixed intervals (like once every 5 seconds). This depends on your
    strategy whether its a high, medium, low frequency trading strategy. Also, performance
    is another concern. if your execution system and features computation are taking
    a lot of time, you realistically wont be able to keep upto pace.
    '''
    def getTimeRuleForUpdates(self):
        return DayTimeRule(startDate=self.__startDate, endDate=self.__endDate, frequency='Mo', sample='3',
                           startTime='00:00', endTime='17:00')


    '''
    Returns a timedetla object to indicate frequency of updates to features
    Any updates within this frequncy to instruments do not trigger feature updates.
    Consequently any trading decisions that need to take place happen with the same
    frequency
    '''

    def getFrequencyOfFeatureUpdates(self):
        return timedelta(weeks=100000)  # minutes, seconds

    def getStartingCapital(self):
        return 10000*len(self.__instrumentIds)

    '''
    This is a way to use any custom features you might have made.
    Returns a dictionary where
    key: featureId to access this feature (Make sure this doesnt conflict with any of the pre defined feature Ids)
    value: Your custom Class which computes this feature. The class should be an instance of Feature
    Eg. if your custom class is MyCustomFeature, and you want to access this via featureId='my_custom_feature',
    you will import that class, and return this function as {'my_custom_feature': MyCustomFeature}
    '''

    def getCustomFeatures(self):
        customFeatures = {'prediction': TrainingPredictionFeature,
                'AUC_ROC_Calculator' : AUC_ROC_Calculator,
                'LogLossCalculator' : LogLossCalculator,
                'fees_and_spread': FeesCalculator,
                'pnl': PNL,
                'capital': Capital,
                'total_profit': TotalProfit,
                'total_loss': TotalLoss,
                'count_profit': CountProfit,
                'count_loss': CountLoss,
                'ScoreCalculator': ScoreCalculator}
        # customFeatures.update(self.__tradingFunctions.getCustomFeatures())
        return customFeatures


    def getInstrumentFeatureConfigDicts(self):
        # ADD RELEVANT FEATURES HERE
        feesConfigDict = {'featureKey': 'fees',
                          'featureId': 'fees_and_spread',
                          'params': {'feeDict': self.__fees,
                                    'price': self.getPriceFeatureKey(),
                                    'position' : 'position'}}
        profitlossConfigDict = {'featureKey': 'pnl',
                            'featureId': 'pnl',
                            'params': {'price': self.getPriceFeatureKey(),
                                       'fees': 'fees'}}
        capitalConfigDict = {'featureKey': 'capital',
                            'featureId': 'capital',
                            'params': {'price': self.getPriceFeatureKey(), 'fees': 'fees'}}
        totalProfitConfigDict = {'featureKey': 'total_profit',
                                'featureId': 'total_profit',
                                'params': {'pnlKey': 'pnl'}}
        totalLossConfigDict = {'featureKey': 'total_loss',
                            'featureId': 'total_loss',
                            'params': {'pnlKey': 'pnl'}}
        countProfitConfigDict = {'featureKey': 'count_profit',
                                'featureId': 'count_profit',
                                'params': {'pnlKey': 'pnl'}}
        countLossConfigDict = {'featureKey': 'count_loss',
                            'featureId': 'count_loss',
                            'params': {'pnlKey': 'pnl'}}

        predictionDict = {'featureKey': 'prediction',
                            'featureId': 'prediction',
                            'params': {'function': self.__tradingFunctions,
                                        'targetVariable': self.targetVariable,
                                        'features_list': self.features_list}}
        aucRocDict = {'featureKey': 'auc_roc_score',
                     'featureId': 'AUC_ROC_Calculator',
                     'params': {'predictionKey': 'prediction',
                                'targetVariable' : self.targetVariable}}
        logLossDict = {'featureKey': 'log_loss',
                     'featureId': 'LogLossCalculator',
                     'params': {'predictionKey': 'prediction',
                                'targetVariable' : self.targetVariable}}
        scoreDict = {'featureKey': 'score',
                     'featureId': 'ScoreCalculator',
                     'params': {'predictionKey': 'prediction',
                                'targetVariable' : self.targetVariable}}

        

        # stockFeatureConfigs = self.__tradingFunctions.getInstrumentFeatureConfigDicts()
        # return {INSTRUMENT_TYPE_STOCK: stockFeatureConfigs + [feesConfigDict, profitlossConfigDict, capitalConfigDict, totalProfitConfigDict, totalLossConfigDict, countProfitConfigDict, countLossConfigDict, predictionDict, aucRocDict, logLossDict, scoreDict]
        #         + self.__additionalInstrumentFeatureConfigDicts}
        return {INSTRUMENT_TYPE_STOCK: [feesConfigDict, profitlossConfigDict, capitalConfigDict, totalProfitConfigDict, totalLossConfigDict, countProfitConfigDict, countLossConfigDict, predictionDict, aucRocDict, logLossDict, scoreDict]
                + self.__additionalInstrumentFeatureConfigDicts}


    '''
    Returns an array of market feature config dictionaries
        market feature config Dictionary has the following keys:
        featureId: a string representing the type of feature you want to use
        featureKey: a string representing the key you will use to access the value of this feature.this
        params: A dictionary with which contains other optional params if needed by the feature
    '''

    def getMarketFeatureConfigDicts(self):
    # ADD RELEVANT FEATURES HERE
        aucRocDict = {'featureKey': 'auc_roc_score',
                     'featureId': 'AUC_ROC_Calculator',
                     'params': {'predictionKey': 'prediction',
                                'targetVariable' : self.targetVariable}}
        logLossDict = {'featureKey': 'log_loss',
                     'featureId': 'LogLossCalculator',
                     'params': {'predictionKey': 'prediction',
                                'targetVariable' : self.targetVariable}}

        scoreDict = {'featureKey': 'score',
                     'featureId': 'ScoreCalculator',
                     'params': {'predictionKey': 'prediction',
                                'targetVariable' : self.targetVariable}}

        # marketFeatureConfigs = self.__tradingFunctions.getMarketFeatureConfigDicts()
        # return marketFeatureConfigs + [aucRocDict, logLossDict, scoreDict] +self.__additionalMarketFeatureConfigDicts
        return [aucRocDict, logLossDict, scoreDict] +self.__additionalMarketFeatureConfigDicts


    '''
    Returns the type of execution system we want to use. Its an implementation of the class ExecutionSystem
    It converts prediction to intended positions for different instruments.
    '''

    def getExecutionSystem(self):
        return Problem2ExecutionSystem(enter_threshold=0.99,
                                    exit_threshold=0.55,
                                    longLimit=10000,
                                    shortLimit=10000,
                                    capitalUsageLimit=0.10 * self.getStartingCapital(),
                                    enterlotSize=1, exitlotSize = 1,
                                    limitType='L', price=self.getPriceFeatureKey())

    '''
    Returns the type of order placer we want to use. its an implementation of the class OrderPlacer.
    It helps place an order, and also read confirmations of orders being placed.
    For Backtesting, you can just use the BacktestingOrderPlacer, which places the order which you want, and automatically confirms it too.
    '''

    def getOrderPlacer(self):
        return BacktestingOrderPlacer()

    '''
    Returns the amount of lookback data you want for your calculations. The historical market features and instrument features are only
    stored upto this amount.
    This number is the number of times we have updated our features.
    '''

    def getLookbackSize(self):
        return max(720, self.__tradingFunctions.lookback)

    def getPriceFeatureKey(self):
        return self.__priceKey

    def setPriceFeatureKey(self, priceKey='Adj_Close'):
        self.__priceKey = priceKey

    def getTargetVariableKey(self):
        return self.targetVariable

    def setTargetVariableKey(self, targetVariable):
        self.targetVariable = targetVariable


    def getDataSetId(self):
        return self.__dataSetId

    def setDataSetId(self, dataSetId):
        self.__dataSetId = dataSetId

    def getInstrumentsIds(self):
        return self.__instrumentIds

    def setInstrumentsIds(self, instrumentIds):
        self.__instrumentIds = instrumentIds

    def getDates(self):
        return {'startDate':self.__startDate,
                'endDate':self.__endDate}

    def setDates(self, dateDict):
        self.__startDate = dateDict['startDate']
        self.__endDate = dateDict['endDate']

    def setFees(self, feeDict={'brokerage': 0.0001,'spread': 0.05}):
        self.__fees = feeDict

    def setAdditionalInstrumentFeatureConfigDicts(self, dicts = []):
        self.__additionalInstrumentFeatureConfigDicts = dicts

    def setAdditionalMarketFeatureConfigDicts(self, dicts = []):
        self.__additionalMarketFeatureConfigDicts = dicts

class FeesCalculator(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        fees = pd.Series(0,index = instrumentManager.getAllInstrumentsByInstrumentId())
        return fees
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        return 0

class PNL(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        fees = pd.Series(0,index = instrumentManager.getAllInstrumentsByInstrumentId())
        return fees
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        return 0

class Capital(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        fees = pd.Series(0,index = instrumentManager.getAllInstrumentsByInstrumentId())
        return fees
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        return 0

class TotalProfit(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        fees = pd.Series(0,index = instrumentManager.getAllInstrumentsByInstrumentId())
        return fees
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        return 0

class TotalLoss(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        fees = pd.Series(0,index = instrumentManager.getAllInstrumentsByInstrumentId())
        return fees
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        return 0

class CountProfit(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        fees = pd.Series(0,index = instrumentManager.getAllInstrumentsByInstrumentId())
        return fees
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        return 0

class CountLoss(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        fees = pd.Series(0,index = instrumentManager.getAllInstrumentsByInstrumentId())
        return fees
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        return 0


class TrainingPredictionFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        tf = featureParams['function']
        # predictions = pd.Series(np.nan, index = instrumentManager.getAllInstrumentsByInstrumentId())
        # holder for all the instrument features for all instruments
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()
        X_train_dict = {}
        y_train_dict = {}
        X_test_dict = {}
        
        features_list = featureParams['features_list']
        targetVariable = featureParams['targetVariable']
        
        instrumentIds = instrumentManager.getAllInstrumentsByInstrumentId()
        datetime = lookbackInstrumentFeatures.getFeatureDf(features_list[0]).index

        for instrumentId in instrumentIds:
            df = pd.DataFrame(columns=features_list, index=datetime)
            for feature in features_list:
                df[feature] = lookbackInstrumentFeatures.getFeatureDf(feature)
            y = lookbackInstrumentFeatures.getFeatureDf(targetVariable)[instrumentId]
            X_train_dict[instrumentId] = df.iloc[:-1,:]
            X_test_dict[instrumentId] = df.iloc[-1,:]
            y_train_dict[instrumentId] = y.iloc[:-1]
        
        predictions = tf.getPrediction(time, updateNum, X_train_dict, y_train_dict, X_test_dict)
        return predictions

class ScoreCalculator(Feature):
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        ids = list(instrumentManager.getAllInstrumentsByInstrumentId())
        if updateNum <2 :
            return pd.Series(0, index=ids)
            
        predictionData = instrumentLookbackData.getFeatureDf(featureParams['predictionKey'])
        trueValue = instrumentLookbackData.getFeatureDf(featureParams['targetVariable'])
        
        def get_roc_auc_score(y_true, y_score):
            combined = np.concatenate([ np.expand_dims(y_true, axis=1), np.expand_dims(y_score, axis=1)], axis=1)
            combined = combined[~np.isnan(combined).any(axis=1)]
            if combined.shape[0] == 0:
                return np.nan
            else:
                try:
                    return sm.roc_auc_score(y_true=combined[:,0], y_score=combined[:,1])
                except Exception as e:
                    print(e)
                    return np.nan

        score = dict()
        for col in predictionData.columns:
            score[col] = get_roc_auc_score( trueValue[col].values, predictionData[col].values )
        return score

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()
        auc_roc_scores = lookbackInstrumentFeatures.getFeatureDf('score').iloc[-1,:]
        mean_scores = np.nanmean(auc_roc_scores)
        return mean_scores

class AUC_ROC_Calculator(Feature):
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        ids = list(instrumentManager.getAllInstrumentsByInstrumentId())
        if updateNum <2 :
            return pd.Series(0, index=ids)
            
        predictionData = instrumentLookbackData.getFeatureDf(featureParams['predictionKey'])
        trueValue = instrumentLookbackData.getFeatureDf(featureParams['targetVariable'])
        
        # temp = instrumentLookbackData.getFeatureDf('Accounts Payable')
        
        def get_roc_auc_score(y_true, y_score):
            combined = np.concatenate([ np.expand_dims(y_true, axis=1), np.expand_dims(y_score, axis=1)], axis=1)
            # Consider only last 15 quarters if more present
            if(len(combined) > 15):
                combined = combined[-15:,:]
            combined = combined[~np.isnan(combined).any(axis=1)]
            if combined.shape[0] == 0:
                return np.nan
            else:
                try:
                    return sm.roc_auc_score(y_true=combined[:,0], y_score=combined[:,1])
                except Exception as e:
                    print(e)
                    return np.nan

        score = dict()#pd.DataFrame(columns=predictionData.columns)
        for col in predictionData.columns:
            score[col] = get_roc_auc_score( trueValue[col].values, predictionData[col].values )

        # print('ROC = %s'%score)
        return score

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()
        auc_roc_scores = lookbackInstrumentFeatures.getFeatureDf('auc_roc_score').iloc[-1,:]
        mean_scores = np.nanmean(auc_roc_scores)
        print('Mean AUC ROC score: %s'%mean_scores)
        return mean_scores


class LogLossCalculator(Feature):
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        ids = list(instrumentManager.getAllInstrumentsByInstrumentId())
        if updateNum <2 :
            return pd.Series(0, index=ids)
            
        predictionData = instrumentLookbackData.getFeatureDf(featureParams['predictionKey'])
        trueValue = instrumentLookbackData.getFeatureDf(featureParams['targetVariable'])
        
        def get_log_loss_score(y_true, y_score):
            combined = np.concatenate([ np.expand_dims(y_true, axis=1), np.expand_dims(y_score, axis=1)], axis=1)
            # Consider only last 15 quarters if more present
            if(len(combined) > 15):
                combined = combined[-15:,:]
            combined = combined[~np.isnan(combined).any(axis=1)]
            if combined.shape[0] == 0:
                return np.nan
            else:
                try:
                    return sm.log_loss(y_true=combined[:,0], y_pred=combined[:,1])
                except Exception as e:
                    print(e)
                    return np.nan

        score = dict()
        for col in predictionData.columns:
            score[col] = get_log_loss_score( trueValue[col].values, predictionData[col].values )

        # print('Log Loss = %s'%score)
        return score

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()
        log_loss_scores = lookbackInstrumentFeatures.getFeatureDf('log_loss').iloc[-1,:]
        mean_scores = np.nanmean(log_loss_scores)
        print('Mean Log Loss: %s'%mean_scores)
        return mean_scores

