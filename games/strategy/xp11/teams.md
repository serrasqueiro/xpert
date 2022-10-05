# xp11

## League

1. Liga
   + [A liga](http://www.xperteleven.com/standings.aspx?Lid=411258&Sel=T&Lnr=1&dh=2) - 1<sup>a</sup> liga,
     * [here](https://xperteleven.com/standings.aspx?Lid=411258&Sel=T&Lnr=1&dh=2&plang=EN) english version
       + [here](http://www.xperteleven.com/leagueInfo.aspx?Lid=411258&dh=2) - details

   + The Boards
     * [here](http://www.xperteleven.com/standings.aspx?Lid=411258&Sel=T&Lnr=1&dh=2) - 1st League Dashboard
     * [here](http://www.xperteleven.com/standings.aspx?Lid=411258&Sel=T&Lnr=2&dh=2) - 2nd League Dashboard (obsolete)

   + Season Schedule
     * 1st League Schedule [here](http://www.xperteleven.com/fixture.aspx?Lid=411258&Lnr=1&dh=2&plang=EN)
     * 2nd League Schedule [here](http://www.xperteleven.com/fixture.aspx?Lid=411258&Lnr=2&dh=2&plang=EN)

## Teams

- Samples
  1. [TeamID sample](http://www.xperteleven.com/players.aspx?TeamID=1591357&Boost=0&dh=2) - Benfas HM
     * [statsTeam sample](http://www.xperteleven.com/statsTeam.aspx?Sel=M&TeamID=1591357&dh=2)
     * Last matches [here](http://www.xperteleven.com/games.aspx?Sel=O&TeamID=1591357&dh=2)
  1. [TeamID sample](http://www.xperteleven.com/players.aspx?TeamID=1591464&Boost=0&dh=2) - Estrela Alapraia
     * [statsTeam sample](http://www.xperteleven.com/statsTeam.aspx?Sel=M&TeamID=1591464&dh=2)
     * Last matches [here](http://www.xperteleven.com/games.aspx?Sel=O&TeamID=1591464&dh=2)

## Game samples

- Here a few game samples
  1.  [here](http://www.xperteleven.com/gameDetails.aspx?GameID=319069347&dh=2)
      - (only one same shown, see fixture.aspx)

## Championship
1. [here](https://xperteleven.com/showroom.aspx?Lid=411258&Lnr=1&dh=2&Omg=10&Cup=0)
   - round 10 (default language)
1. [here](https://xperteleven.com/showroom.aspx?Lid=411258&Lnr=1&dh=2&Omg=10&Cup=0&plang=EN)
   - round 10 (english language)

# fixture.py
Use `bpython` to explore the HTML tree (using BeautifulSoup4).
1. `importlib.reload(fixture)`
1. `data = open(".xpert.data", "rb").read()`
1. `adict = fixture.processor(data)`
1. `tbls = [(key, adict["fixture"]["t-index"][key]) for key in adict["fixture"]["t-index"]]`
1. `atables = [(elem["index"], elem["table-id"]) for elem in adict["fixture"]["tables"]]`
