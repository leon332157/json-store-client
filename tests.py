import unittest
import json_store_client
import random

TOKEN = "4aca8a426a3d8f3b0230f8dd83806b10d25237e22393bdcddb710f548c373d7e"
KEY = 'testKey'
DATA = {'testDataKey': 'testDataValue'}


class TestSyncClient(unittest.TestCase):
    def setUp(self):
        self.client = json_store_client.Client(TOKEN)

    def testInit(self):
        self.assertIsInstance(self.client, json_store_client.Client)

    def testEmptyKey(self):
        with self.assertWarns(json_store_client.EmptyResponseWarning):
            self.client.get(str(random.randint(0, 10)))

    def testSave(self):
        self.assertEqual(self.client.store(KEY, DATA), '"{\\"testDataKey\\": \\"testDataValue\\"}"')
        self.assertEqual(self.client.get(KEY), DATA)

    def testSaveMultiple(self):
        self.assertIsNone(self.client.store_multiple(DATA))
        self.assertEqual(self.client.get('testDataKey'), 'testDataValue')

    def testDelete(self):
        self.assertEqual(self.client.delete(KEY), KEY)

    def doCleanups(self):
        self.client.session.close()


class TestAsyncClient(unittest.TestCase):
    def setUp(self):
        self.client = json_store_client.AsyncClient(TOKEN)

    def testInit(self):
        self.assertIsInstance(self.client, json_store_client.AsyncClient)

    async def testEmptyKey(self):
        with self.assertWarns(json_store_client.EmptyResponseWarning):
            await self.client.get(str(random.randint(0, 10)))

    async def testSave(self):
        self.assertEqual(await self.client.store(KEY, DATA), '"{\\"testDataKey\\": \\"testDataValue\\"}"')
        self.assertEqual(await self.client.get(KEY), DATA)

    async def testSaveMultiple(self):
        self.assertIsNone(await self.client.store_multiple(DATA))
        self.assertEqual(await self.client.get('testDataKey'), 'testDataValue')

    async def testDelete(self):
        self.assertEqual(await self.client.delete(KEY), KEY)

    async def doCleanups(self):
        await self.client.session.close()


if __name__ == '__main__':
    unittest.main()
