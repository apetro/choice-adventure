# 013 Sourcing actions from the Tile and the Player

Right about here is where I lost patience with the lack of separation of concerns between the modules and I started trying to organize this code.

So, rather than an all-knowing game loop that knows about all the different tiles and all the different states the player might be in, I switched this around to source actions from the active tile and from the player.

Invented `Action`, `Actions`, and a method on the player and on the tile to get their available `Actions`.

That feels better.

It's still spaghetti code, with tiles and player and world needing references to one another, but still, this feels more structured in a way to support adding more actions in the future.
