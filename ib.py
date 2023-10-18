import nest_asyncio
nest_asyncio.apply()
from ib_insync import *
from fastapi_socketio import SocketManager
from statepattern import Context
from singletonpattern import Singleton
from typing import Dict, List
import dataclasses
import logging
import asyncio
import json
import sys
from data_obj.objects import Asset


class IBManager(Singleton, Context):
    threadIdLog = True
    logger = logging.getLogger(__qualname__)
    logger.setLevel(logging.DEBUG)
    log_stream_hdr = logging.StreamHandler(stream=sys.stdout)
    log_formatter = logging.Formatter(fmt=("%(threadName)s:" if threadIdLog else "") + "%(levelname)s:%(asctime)s.%(msecs)03d: %(message)s",
                    datefmt='%Y/%d/%m %H:%M:%S')
    log_stream_hdr.setFormatter(log_formatter)
    logger.addHandler(log_stream_hdr)

    def __init__(self):
        Context.__init__(self)
        self._ib = IB()
        # result = self._ib.connect('192.168.0.201', 8000, clientId=704)
        # print(result)
        self.sm = None
        self.main_asset: Asset = Asset()
        self._asset_dict: Dict[str, Asset] = {}
        self.contract = None
        self.logger.debug(f"ib instance: {self._ib}")

    def setSM(self, sm: SocketManager) -> None:
        self.sm = sm

    def connectIB(self, ip_address: str = '192.168.0.201', port=8000, clientId=704):
        result = self._ib.connect(ip_address, port, clientId)
        self.logger.debug(f"connectIB result: {result}")

    def setContract(self, symbol:str):
        contract = Forex(symbol)
        self.contract = contract
        self._ib.qualifyContracts(contract)

    def get_pos_list(self):
        pos_list = self._ib.positions()
        self.logger.debug(f"Position list in account: {pos_list}")

    async def batchsubscribe(self, symbol:str):
        print("batchsubscribe function called")
        if self._ib.isConnected():
            print("IB is connected")
            await self.subscribeContract(symbol)
            # self.subscribeOrderBook(self.contract)
        else:
            self.logger.error("IB is not connected")
        

    async def sub_5sec_data(self, symbol: str):
        self.logger.debug("Subscribe 1s data started")
        self._add_asset(symbol)
        contract = Forex(symbol)
        self.logger.debug(f"contract: {contract}")
        self.main_asset.bars_5s = self._ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='60 S',
        barSizeSetting='5 secs',
        whatToShow='MIDPOINT',
        useRTH=True,
        formatDate=1,
        keepUpToDate=True)
        self.logger.debug(f"5s bars on subscribe: {self.main_asset.bars_5s}")
        ls = [util.tree(bar.__dict__) for bar in self.main_asset.bars_5s]
        if self.sm is not None:
            await self.sm.emit('bars on subscribe', json.dumps(ls))
        self.main_asset.bars_1s.updateEvent += self.on1sBarUpdate    
        self.logger.debug("Subscribe 1s data ended")
    
    async def sub_1min_data(self, symbol: str):
        self.logger.debug("Subscribe 1m data started")
        contract = Forex(symbol)
        self.logger.debug(f"contract: {contract}")
        self.bars_1m = self._ib.reqHistoricalData(
            contract,
            endDateTime='',
            durationStr='3600 S',
            # barSizeSetting='1 secs',
            barSizeSetting='1 min',
            whatToShow='MIDPOINT',
            useRTH=True,
            formatDate=1,
            keepUpToDate=True)

        ls = [util.tree(bar.__dict__) for bar in self.bars_1m]
        if self.sm is not None:
            await self.sm.emit('init 1m bar', json.dumps(ls))
        self.bars_1m.updateEvent += self.on1mBarUpdate
        self.logger.debug("Subscribe Contract function ended")
    
    async def sub_orderbook(self, symbol:str =None):
        self.orderbook_contract = Forex(symbol)
        self.ticker = self._ib.reqMktDepth(contract=self.orderbook_contract, numRows=10)
        self.ticker.updateEvent += self.onOrderBookUpdate

    async def unsubscribe_orderbook(self):
        self._ib.cancelMktDepth(self.orderbook_contract)

    def limitOrder(self):
        contract = Forex('AUDUSD')
        self._ib.qualifyContracts(contract)

    def close(self):
        self._ib.disconnect()

    async def on1mBarUpdate(self, bars, hasNewBar):
        if hasNewBar:
            #send('Bar Updated')
            ls = [util.tree(i.__dict__) for i in bars]
            # ls = util.tree(bars)
            if self.sm is not None:
                await self.sm.emit('new 1m bar', json.dumps(ls))
            print('1 min passed')
            print(bars[-1])
            # print(self.bars_1m)
        else:
            ls = [util.tree(i.__dict__) for i in bars]
            # ls = util.tree(bars)
            df = util.df(bars[-61:-1])
            if self.sm is not None:
                await self.sm.emit('1m bar changed', json.dumps(ls))
            self.logger.debug(f"latest 1m bar updated: {bars[-1]}")
            # print(bars[-1])
            # print(df)

    async def on5sBarUpdate(self, bars, hasNewBar):
        if hasNewBar:
            # self.action()
            # send('Bar Updated')
            ls = util.tree(bars)
            if self.sm is not None:
                await self.sm.emit('new 5s bar', json.dumps(ls))
            self.logger.debug(f"new 5s bar updated: {bars[-1]}")
        else:
            self.logger.debug(f"latest 5s bar updated: {bars[-1]}")

        

    async def onOrderBookUpdate(self, ticker):
        """
            domBids/domAsks is a list

            Important fields that could be useful in ticker
            - ticker.contract
        """
        self.logger.debug(f"Bid: {[bid._asdict() for bid in ticker.domBids]}")
        self.logger.debug(f"Ask: {[ask._asdict() for ask in ticker.domAsks]}")
        if self.sm is not None:
            pass

    def unsubscribeAll(self):
        for asset in self._asset_dict.values():
            print(f"5s bars: {asset.bars_5s}")
            print(f"1m bars: {asset.bars_1m}")
        if self.main_asset.bars_1s:
            self._ib.cancelHistoricalData(self.main_asset.bars_1s)
        # if self.bars_1m:
        #     self._ib.cancelHistoricalData(self.bars_1m)
        # self._ib.cancelMktDepth(self.contract)

    def _add_asset(self, symbol: str):
        '''
            add Asset data class to the asset
        '''
        if symbol not in self._asset_dict:
            self.asset_list[symbol] = Asset()


 
if __name__ == '__main__':
    import os
    print (os.path.dirname(os.path.abspath(__file__)))
    ib_mgr = IBManager.getInstance()
    ib_mgr.connectIB()
    # ib_mgr.setContract('AUDUSD')
    loop = asyncio.get_event_loop()
    ib_mgr.get_pos_list()
    loop.create_task(ib_mgr.batchsubscribe('EURUSD'))
    # loop.run_until_complete(ib_mgr.batchsubscribe('EURUSD'))
    ib_mgr._ib.sleep(10)
    ib_mgr.unsubscribeAll()
    ib_mgr.close()
    print("Closing")