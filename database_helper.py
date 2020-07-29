import json


def add_uid(u_id):
    stats_file = open("stats.json", "r")
    stats = json.load(stats_file)
    if u_id not in stats:
        stats[u_id] = {}

    stats_file.close()
    with open("stats.json", "w") as stats_file:
        json.dump(stats, stats_file)


# Given the user and stat, add 1 to that stat
# (e.g. stat = number of times talked to kuro, this function will increase that counter)
def increase_stat(u_id, stat):
    # add u_id to database if they don't exist yet
    u_id = str(u_id)
    add_uid(u_id)

    stats_file = open("stats.json", "r")
    stats = json.load(stats_file)

    # increase the stat in stats
    if stat in stats[u_id]:
        stats[u_id][stat] += 1
    else:
        stats[u_id][stat] = 1

    stats_file.close()
    with open("stats.json", "w") as stats_file:
        json.dump(stats, stats_file)

