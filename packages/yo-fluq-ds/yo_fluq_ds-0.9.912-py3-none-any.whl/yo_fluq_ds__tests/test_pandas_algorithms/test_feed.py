from yo_fluq_ds__tests.common import *

class FeedTests(TestCase):
    def test_feed_fluent(self):
        plt = pd.Series([1,2,3,4]).feed_to_fluent_callable(FluentPlot()).call_obj(lambda z: z.plot).args().exec.result()