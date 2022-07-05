import random

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Strategy:

  def __init__(self):
    super()
    
  def get_name(self):
    return self.__class__.__name__

  def pick_keepers(self, rolls, remaining, score, target, num_future_players):
    pass

  def keep_nums_or_lowest(self, rolls, nums, score, target, num_future_players):
    '''Keep only threes and numbers specified or if they don't exist, the lowest available.'''
    lowest = 7
    keepers = []
    for roll in rolls:
      if roll == 3:
        keepers.append(0)
        lowest = 0
      elif roll in nums and (score + roll) <= target :
        keepers.append(roll)
      elif roll < lowest:
        lowest = roll
    if not keepers:
      keepers.append(lowest)
    return keepers

class Only3OrLowest(Strategy):

  def __init__(self):
    super()
    
  def pick_keepers(self, rolls, remaining, score, target, num_future_players):
    return self.keep_nums_or_lowest(rolls, [], score, target, num_future_players)

class Only31OrLowest(Strategy):

  def __init__(self):
    super()
    
  def pick_keepers(self, rolls, remaining, score, target, num_future_players):
    return self.keep_nums_or_lowest(rolls, [1], score, target, num_future_players)

class Only312OrLowest(Strategy):

  def __init__(self):
    super()
    
  def pick_keepers(self, rolls, remaining, score, target, num_future_players):
    return self.keep_nums_or_lowest(rolls, [1,2], score, target, num_future_players)

class TakeHigherDiceLater1(Strategy):

  def __init__(self):
    super()
    
  def pick_keepers(self, rolls, remaining, score, target, num_future_players):
    # remaining - dice kept
    # 5 - [3]
    # 4 - [1,3]
    # 3 - [1,2,3]
    # 2 - [1,2,3]
    # 1 - (any bc no choice)
    nums = []
    if remaining == 4:
      nums = [1]
    elif remaining == 2 or remaining == 3:
      nums = [1,2]
    return self.keep_nums_or_lowest(rolls, nums, score, target, num_future_players)

class TakeHigherDiceLater2(Strategy):

  def __init__(self):
    super()
    
  def pick_keepers(self, rolls, remaining, score, target, num_future_players):
    # remaining - dice kept
    # 5 - [3]
    # 4 - [1,3]
    # 3 - [1,3]
    # 2 - [1,2,3]
    # 1 - (any bc no choice)
    nums = []
    if remaining == 4 or remaining == 3:
      nums = [1]
    elif remaining == 2:
      nums = [1,2]
    return self.keep_nums_or_lowest(rolls, nums, score, target, num_future_players)

class TakeHigherDiceLater3(Strategy):

  def __init__(self):
    super()

  def pick_keepers(self, rolls, remaining, score, target, num_future_players):
    # remaining - dice kept
    # 5 - [3]
    # 4 - [3]
    # 3 - [1,3]
    # 2 - [1,2,3]
    # 1 - (any bc no choice)
    nums = []
    if remaining == 3:
      nums = [1]
    elif remaining == 2:
      nums = [1,2]
    return self.keep_nums_or_lowest(rolls, nums, score, target, num_future_players)

class TakeHigherDiceLater4(Strategy):

  def __init__(self):
    super()

  def pick_keepers(self, rolls, remaining, score, target, num_future_players):
    # remaining - dice kept
    # 5 - [3]
    # 4 - [3]
    # 3 - [1,3]
    # 2 - [1,3]
    # 1 - (any bc no choice)
    nums = []
    if remaining == 3 or remaining == 2:
      nums = [1]
    return self.keep_nums_or_lowest(rolls, nums, score, target, num_future_players)

# Same as TakeHigherDiceLater3 however this strategy aims for a score less than
# premeditated target to anticipate future players scoring lower. If the current
# minimum is less, still target under it.
class PremeditatedTarget(Strategy):

  def __init__(self, premeditated_target):
    self.premeditated_target = premeditated_target
    self.take_higher = TakeHigherDiceLater3()
    super()

  def get_name(self):
    return self.__class__.__name__ + str(self.premeditated_target)

  def pick_keepers(self, rolls, remaining, score, target, num_future_players):
    # If there are more players, use premeditated target
    if num_future_players > 5 and self.premeditated_target < target:
      target = self.premeditated_target
    return self.take_higher.pick_keepers(rolls=rolls,
                                         remaining=remaining,
                                         score=score,
                                         target=target,
                                         num_future_players=num_future_players)

def get_rolls(x):
  rolls = []
  for _ in range(0,x):
    rolls.append(random.randrange(1,7))
  return rolls

# complete one player turn using a specific strategy
def do_turn(strategy, target, num_future_players):
  score = 0
  remaining = 5
  while remaining > 0:
    rolls = get_rolls(remaining)
    keepers = strategy.pick_keepers(rolls,
                                    remaining,
                                    score,
                                    target,
                                    num_future_players)
    score += sum(keepers)
    remaining -= len(keepers)
  return score

# complete a game with players each using a different strategy
def do_game(strategies):
  winning_strat = ''
  winning_score = 31
  num_players = len(strategies)
  for index, strategy in enumerate(strategies):
    score = do_turn(strategy, winning_score - 1, num_players - (index + 1))
    if score < winning_score:
      winning_strat = strategy.get_name()
      winning_score = score
  # print(f'Winner: {winning_strat}')
  # print(f'Score: {winning_score}')
  return (winning_score, winning_strat)

def test_single_strat(strategy, num_players=1, num_games=10000):
  scores = []
  players = [strategy] * num_players
  for _ in range(num_games):
    result = do_game(players)
    scores.append(result[0])
  return scores

# doesn't account for the order of the strategies employed. For example, if the
# player to your right plays conservatively, you could target a higher score.

def combat_strats(strategies, num_games=10000):
  scores = []
  num_wins = {strategy.get_name(): 0 for strategy in strategies}
  for _ in range(num_games):
    random.shuffle(strategies)
    result = do_game(strategies)
    scores.append(result[0])
    num_wins[result[1]] += 1
  return (scores, num_wins)

def plot_distribution(scores, title):
  scores_df = pd.DataFrame(scores)
  sns.set(rc = {'figure.figsize':(20,10)})
  ax = sns.displot(scores_df)
  ax.set_axis_labels('Winning Score', 'Frequency')
  plt.title(title)

def ordered_bar_plot(d, title):
  # order results
  # print(list(results.keys()))
  # df = pd.DataFrame({'lab':list(results.keys()), 'val':list(results.values())})
  arr = list(d.items())
  sorted_by_wins = sorted(arr, key=lambda tup: tup[1])
  sns.set(rc = {'figure.figsize':(30,10)})
  df = pd.DataFrame({k:[v] for k,v in sorted_by_wins})
  ax = sns.barplot(data=df)
  ax.set_xlabel('Strategy')
  ax.set_ylabel('Total Wins')
  ax.set_title(title)

# 13 player game with all strats
results = combat_strats([Only3OrLowest(),
                         Only31OrLowest(),
                         Only312OrLowest(),
                         TakeHigherDiceLater1(),
                         TakeHigherDiceLater2(),
                         TakeHigherDiceLater3(),
                         TakeHigherDiceLater4(),
                         PremeditatedTarget(1),
                         PremeditatedTarget(2),
                         PremeditatedTarget(3),
                         PremeditatedTarget(4),
                         PremeditatedTarget(5),
                         PremeditatedTarget(6)],
                        num_games=40000)
ordered_bar_plot(results[1], 'All Strats - 40k Times')

# 4 player game with middle risk strats
# results = combat_strats([TakeHigherDiceLater2,
#                          Only312OrLowest],
#                         num_games=50000)
# ordered_bar_plot(results[1], 'Higher vs basic2 - 50k Times')


# plot_distribution(test_single_strat(TakeHigherDiceLater2, 3), 'Winning Score of HigherLater2 - 10k Three Player Games')
