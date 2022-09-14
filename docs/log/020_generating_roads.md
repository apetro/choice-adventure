# 020 Generating roads

Okay, it currently generates a world with a village, a road, a village,
and then just forest.

That's kind of boring. We're going to need more villages.

Well. Let's add another pair of villages. More pairs of villages.

And generate roads between them. With occasional wiggles.

And generate roads going north from the villages.

This is pretty good, but it's possible to get adjacent parallel east-west roads.

```
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |RO|RO|RO|RO|RO|RO|RO|RO|  |  |  |  |  |
|  |  |  |  |  |  |VI|RO|  |  |  |  |  |  |RO|RO|RO|RO|VI|  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |RO|  |  |
|  |  |VI|RO|RO|RO|RO|RO|RO|RO|RO|RO|RO|RO|RO|RO|RO|RO|RO|VI|
|  |  |  |  |  |  |  |RO|RO|RO|RO|RO|RO|  |  |  |  |  |  |  |
|  |  |  |VI|RO|RO|RO|RO|  |  |  |  |RO|RO|RO|RO|RO|RO|VI|  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
```

I detect the equivalent situation north-south,
so I'll have to do something similar east-west.

Done. And that's enough for tonight.
