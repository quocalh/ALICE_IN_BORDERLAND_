for the sake of time, i was able to deploy the most dogshit code i ever written, no enums, no separated file for graphic, no optimization, only supports multiple threads, with some really questionable classes, i knew i had not done it right but continue to push it further anyways, i mean 2 months for this is crazy i cant lie. Anyways, fuck my skillset.



In my next project, i will try to recreate the once function but won't try to use the current method (it works but too stupid, and pose a low level in reliability (not sure whether i have reactive em every state or not situation))
The old method:
  def once_func(...)-> float:
    once_func = None # not sure if the same thing can be done in C++ :D (using static variables i suppose?)
  reserved_once_func = once_func
  // revive the function
  once_func = reserved_once_func
  // it works great but looks stupid as fuck (it also created a mumbo jumbo in the game's codebase :sob:)

In my head, maybe it will reintroduce as a "@once" function:
e.g.
  @once
  def my_func(self, ...) -> float:
    ...
the @once function will ensure the thing only run once in the list


and i will have a revive function, but not really sure how to implement
maybe like this?
  @revive
  def RevivingOnceFunction(func, ...) -> None:
    ...
or
  def RevivingOnceFunction(func, ...) -> None:
    ...
idk, but we will see
