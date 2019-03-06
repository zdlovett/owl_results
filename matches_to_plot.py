"""
Convert the data from the matches api endpoint to Vega compatible json files

The information that we are most interested in is:
    -Team wins (who beat who)
    -Player #matches played and Team #matches played
"""

import json
from datetime import datetime as dt
from IPython import embed


def get_team_wins(content):
    "Build vega compatible json outputs given the match content"
    links = []
    teams = []
    results = [] # team -> team ordering

    for match in content:
        competitors = [team['name'] for team in match['competitors']]
        teams.extend(competitors)

        try:
            winner = match['winner']['name']
        except KeyError:
            start = match['startDate'] / 1000
            start = dt.fromtimestamp(start)
            print(f"No winner for match on {start}")
            continue

        competitors.remove(winner)
        results.append((winner, competitors[0]))

    teams = list(set(teams))
    teams = [{'id':i+1, 'name':name} for i, name in enumerate(teams)]
    teams.append({'id':0, 'name':'root'})

    for team in teams[1:]:
        team['parent'] = 0
    team_to_id = {t['name']:t['id'] for t in teams}

    for winner, loser in results:
        link = {
            "source" : team_to_id[winner],
            "target" : team_to_id[loser]
        }
        links.append(link)

    return teams, links


def dump(obj, filename):
    with open(filename, 'w') as fp:
        json.dump(obj, fp, indent=4)

def main():
    # load the data
    with open("./dumps/matches.json", 'rb') as fp:
        matches = json.load(fp)

    teams, links = get_team_wins(matches['content'])

    dump(teams, 'teams.json')
    dump(links, 'links.json')

    embed()


if __name__ == '__main__':
    main()




"""
matches keys:
    'content', -> list of all of the matches
    'totalPages',
    'totalElements',
    'last',
    'numberOfElements',
    'size',
    'number',
    'sort',
    'first'

match == content[0].keys (keys for a match)
    'id',
    'competitors', # list of 'teams'
    'scores',
    'conclusionValue',
    'conclusionStrategy',
    'winner', # 'team'
    'home',
    'state',
    'status',
    'statusReason',
    'attributes',
    'games', -> [{'id', 'number', 'points', 'attributes', 'attributesVersion', 'players', 'state', 'status', 'statusReason', 'stats', 'handle', 'match'},]
    'clientHints',
    'bracket',
    'dateCreated',
    'flags',
    'handle',
    'competitorStatuses',
    'timeZone',
    'actualStartDate',
    'actualEndDate',
    'startDate',
    'endDate',
    'showStartTime',
    'showEndTime'

team {
    'id',
    'availableLanguages',
    'handle',
    'name',
    'homeLocation',
    'primaryColor',
    'secondaryColor',
    'game',
    'attributes',
    'attributesVersion',
    'abbreviatedName',
    'addressCountry',
    'logo',
    'icon',
    'players',
    'secondaryPhoto',
    'type'}

games -> players -> {team, player, matchGame, sortIndex}
                             \_> {'id',
                                    'availableLanguages',
                                    'handle',
                                    'name',
                                    'homeLocation',
                                    'game',
                                    'attributes',
                                    'attributesVersion',
                                    'familyName',
                                    'givenName',
                                    'nationality',
                                    'headshot',
                                    'type'}
"""