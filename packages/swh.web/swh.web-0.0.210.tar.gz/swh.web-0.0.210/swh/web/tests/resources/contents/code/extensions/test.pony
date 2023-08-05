use "collections"

class StopWatch
  """
  A simple stopwatch class for performance micro-benchmarking
  """
  var _s: U64 = 0

  fun delta(): U64 =>
    Time.nanos() - _s

actor LonelyPony
  """
  A simple manifestation of the lonely pony problem
  """
  var env: Env
  let sw: StopWatch = StopWatch

  new create(env': Env) =>
    env = env