from yo_fluq import *
from unittest import TestCase

class TestFeed(TestCase):
    def test_feed_execute(self):
        q = (Query
             .args(1,2,3,4)
             .feed_to_fluent_callable(Query.push())
             .split_by_group(lambda z: z%2)
             .sum()
             .exec.result()
             )
        self.assertDictEqual({0:6,1:4}, q)

    def test_feed_feed(self):
        q = (Query
             .args(1,2,3,4)
             .feed_to_fluent_callable(Query.push())
             .split_by_group(lambda z: z%2)
             .sum()
             .exec.feed(set)
        )
        self.assertSetEqual(
            {0,1},
            q
        )

    def test_feed_feed_fluent(self):
        q = (Query
             .args(1,2,3,4)
             .feed_to_fluent_callable(Query.push())
             .split_by_group(lambda z: z % 2)
             .sum()
             .exec.feed(Query.dict)
             .order_by(lambda z: z.key)
             .select(lambda z: z.value)
             .to_list()
        )
        self.assertListEqual(
            [6,4],
            q
        )

    def test_feed_feed_fluent_callable(self):
        q = (
            Query
            .args(1,2,3, 4)
            .feed_to_fluent_callable(Query.push())
            .split_by_group(lambda z: z%2)
            .sum()
            .exec.feed_to_fluent_callable(Query.push())
            .count()
            .exec.result()
        )
        self.assertEqual(2,q)

