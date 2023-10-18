# from locale import ABDAY_1
import asyncio
import unittest
import logging, sys, os
from singletonpattern import Singleton
from statepattern import Context
from ib import IBManager
from ib_insync import util

'''
    Testing suite for the IBManager, a class wrappered around the ib_insync library
    To show stdout message, run in debug mode
'''
class init_test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_init(self):
        mgr = IBManager()
        self.assertIsNotNone(mgr)
        self.assertIsInstance(mgr, Singleton)
        self.assertIsInstance(mgr, Context)
    
    def test_singleton_init(self):
        mgr = IBManager.getInstance()
        mgr2 = IBManager.getInstance()
        self.assertIsNotNone(mgr)
        self.assertIsInstance(mgr, Singleton)
        self.assertIsInstance(mgr, Context)
        self.assertIs(mgr, mgr2)

    def test_diff_ib_inst(self):
        class A(Singleton):
            def __init__(self):
                pass
        mgr = IBManager()
        mgr2 = IBManager.getInstance()
        mgr3 = IBManager.getInstance()
        self.assertIs(mgr2, mgr3)
        self.assertIs(mgr, mgr2)

class subscribe_data_test(unittest.TestCase):
    threadIdLog = True
    logger = logging.getLogger(__qualname__)
    logger.setLevel(logging.DEBUG)
    log_stream_hdr = logging.StreamHandler(stream=sys.stdout)
    log_formatter = logging.Formatter(fmt=("%(threadName)s:" if threadIdLog else "") + "%(levelname)s:%(asctime)s.%(msecs)03d: %(message)s",
                    datefmt='%Y/%d/%m %H:%M:%S')
    log_stream_hdr.setFormatter(log_formatter)
    logger.addHandler(log_stream_hdr)

    @classmethod
    def setUpClass(cls):
        util.startLoop()
        cls.ib_mgr = IBManager.getInstance()
        cls.ib_mgr.connectIB()


    @classmethod
    def tearDownClass(cls):
        cls.ib_mgr.close()

    @unittest.skip("This should only be run manually in debug mode to see the flow of the program")
    def test_subscribe_5sec_data(self):
        self.logger.debug("Test subscription started")
        loop = asyncio.get_event_loop()
        # await self.ib_mgr.subscribeContract('EURUSD')
        loop.create_task(self.ib_mgr.sub_5sec_data('EURUSD'))
        self.ib_mgr._ib.sleep(60)
        self.ib_mgr.unsubscribeAll()
        self.logger.debug("Test subscription ended")

    def test_subscribe_1min_data(self):
        self.logger.debug("Test subscription started")
        loop = asyncio.get_event_loop()
        # await self.ib_mgr.subscribeContract('EURUSD')
        loop.create_task(self.ib_mgr.sub_1min_data('EURUSD'))
        self.ib_mgr._ib.sleep(30)
        self.ib_mgr.unsubscribeAll()
        self.logger.debug("Test subscription ended")

    def test_subscribe_1h_data(self):
        self.logger.debug("Test subscription started")
        loop = asyncio.get_event_loop()
        # await self.ib_mgr.subscribeContract('EURUSD')
        loop.create_task(self.ib_mgr.sub_1hour_data('EURUSD'))
        self.ib_mgr._ib.sleep(30)
        self.ib_mgr.unsubscribeAll()
        self.logger.debug("Test subscription ended")
    
    def test_subscribe_4h_data(self):
        self.logger.debug("Test subscription started")
        loop = asyncio.get_event_loop()
        # await self.ib_mgr.subscribeContract('EURUSD')
        loop.create_task(self.ib_mgr.sub_4hour_data('EURUSD'))
        self.ib_mgr._ib.sleep(30)
        self.ib_mgr.unsubscribeAll()
        self.logger.debug("Test subscription ended")
    
    def test_subscribe_1d_data(self):
        self.logger.debug("Test subscription started")
        loop = asyncio.get_event_loop()
        # await self.ib_mgr.subscribeContract('EURUSD')
        loop.create_task(self.ib_mgr.sub_1day_data('EURUSD'))
        self.ib_mgr._ib.sleep(30)
        self.ib_mgr.unsubscribeAll()
        self.logger.debug("Test subscription ended")

    def test_subscribe_orderbook(self):
        self.logger.debug("Test subscribe orderbook started")
        loop = asyncio.get_event_loop()
        loop.create_task(self.ib_mgr.subscribeOrderBook(symbol='EURUSD'))
        self.ib_mgr._ib.sleep(10)
        loop.create_task(self.ib_mgr.unsubscribe_orderbook())
        self.ib_mgr._ib.sleep(2)
        self.logger.debug("Test subscribe orderbook ended")

    def test_lmt_order(self):
        pass


if __name__ == '__main__':
    init_test.main()
    subscribe_data_test.main()