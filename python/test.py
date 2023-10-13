import cs2leaderboard as cs2

# w/o instantiation
all = cs2.fetch_all()
print(all)

# w/ instantiation
class_all = cs2.cs2leaderboard()
print(class_all.fetch_all())