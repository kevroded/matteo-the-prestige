import os, json, re, jsonpickle
import sqlite3 as sql

data_dir = "data"
league_dir = "leagues"

def create_connection(league_name):
    #create connection, create db if doesn't exist
    conn = None
    try:
        if not os.path.exists(os.path.join(data_dir, league_dir, league_name)):
        
            os.makedirs(os.path.join(data_dir, league_dir, league_name))
        conn = sql.connect(os.path.join(data_dir, league_dir, league_name, f"{league_name}.db"))

        # enable write-ahead log for performance and resilience
        conn.execute('pragma journal_mode=wal')

        return conn
    except:
        print("oops, db connection no work")
        return conn

def create_season_connection(league_name, season_num):
    #create connection, create db if doesn't exist
    conn = None
    try:
        if not os.path.exists(os.path.join(data_dir, league_dir, league_name)):
        
            os.makedirs(os.path.join(data_dir, league_dir, league_name))
        conn = sql.connect(os.path.join(data_dir, league_dir, league_name, season_num, f"{league_name}.db"))

        # enable write-ahead log for performance and resilience
        conn.execute('pragma journal_mode=wal')

        return conn
    except:
        print("oops, db connection no work")
        return conn

def state(league_name):
    if not os.path.exists(os.path.dirname(os.path.join(data_dir, league_dir, league_name, f"{league_name}.state"))):
            os.makedirs(os.path.dirname(os.path.join(data_dir, league_dir, league_name, f"{league_name}.state")))
    with open(os.path.join(data_dir, league_dir, league_name, f"{league_name}.state")) as state_file:
        return json.load(state_file)

def init_league_db(league):
    conn = create_connection(league.name)

    player_stats_table_check_string = """ CREATE TABLE IF NOT EXISTS stats (
                                            counter integer PRIMARY KEY,
                                            id text,
                                            name text,
                                            team_name text,
                                            outs_pitched integer DEFAULT 0,
                                            walks_allowed integer DEFAULT 0,
                                            hits_allowed integer DEFAULT 0,
                                            strikeouts_given integer DEFAULT 0,
                                            runs_allowed integer DEFAULT 0,
                                            plate_appearances integer DEFAULT 0,
                                            walks_taken integer DEFAULT 0,
                                            sacrifices integer DEFAULT 0,
                                            hits integer DEFAULT 0,
                                            home_runs integer DEFAULT 0,
                                            total_bases integer DEFAULT 0,
                                            rbis integer DEFAULT 0,
                                            strikeouts_taken integer DEFAULT 0
                                            );"""

    teams_table_check_string = """ CREATE TABLE IF NOT EXISTS teams (
                                            counter integer PRIMARY KEY,
                                            name text NOT NULL,
                                            wins integer DEFAULT 0,
                                            losses integer DEFAULT 0,
                                            run_diff integer DEFAULT 0
                                        ); """

    if conn is not None:
        c = conn.cursor()
        c.execute(player_stats_table_check_string)
        c.execute(teams_table_check_string)

        for team in league.teams_in_league():
            c.execute("INSERT INTO teams (name) VALUES (?)", (team.name,))

            player_string = "INSERT INTO stats (name, team_name) VALUES (?,?)"
            for batter in team.lineup:
                c.execute(player_string, (batter.name, team.name))
            for pitcher in team.rotation:
                c.execute(player_string, (pitcher.name, team.name))

    conn.commit()
    conn.close()

def save_league(league):
    if league_exists(league.name):
        state_dic = {
                "season" : league.season,
                "day" : league.day,
                "constraints" : league.constraints,
                "schedule" : league.schedule,
                "game_length" : league.game_length,
                "series_length" : league.series_length,
                "games_per_hour" : league.games_per_hour,
                "owner" : league.owner,
                "champion" : league.champion,
                "historic" : league.historic               
            }
        with open(os.path.join(data_dir, league_dir, league.name, f"{league.name}.state"), "w") as state_file:
            json.dump(state_dic, state_file, indent=4)

def add_stats(league_name, player_game_stats_list):
    conn = create_connection(league_name)
    if conn is not None:
        c=conn.cursor()
        for team_name in player_game_stats_list.keys():
            for (name, player_stats_dic) in player_game_stats_list[team_name]:
                c.execute("SELECT * FROM stats WHERE name=? AND team_name=?",(name, team_name))
                this_player = c.fetchone()
                if this_player is not None:
                    for stat in player_stats_dic.keys():
                        c.execute(f"SELECT {stat} FROM stats WHERE name=? AND team_name=?",(name, team_name))
                        old_value = int(c.fetchone()[0])
                        c.execute(f"UPDATE stats SET {stat} = ? WHERE name=? AND team_name=?",(player_stats_dic[stat]+old_value, name, team_name))
                else:
                    c.execute("INSERT INTO stats(name) VALUES (?)",(name,))
                    for stat in player_stats_dic.keys():
                        c.execute(f"UPDATE stats SET {stat} = ? WHERE name=? AND team_name=?",(player_stats_dic[stat], name, team_name))
        conn.commit()
    conn.close()

def update_standings(league_name, update_dic):
    if league_exists(league_name):
        conn = create_connection(league_name)
        if conn is not None:
            c = conn.cursor()

            for team_name in update_dic.keys():
                for stat_type in update_dic[team_name].keys(): #wins, losses, run_diff
                    c.execute(f"SELECT {stat_type} FROM teams WHERE name = ?", (team_name,))
                    old_value = int(c.fetchone()[0])
                    c.execute(f"UPDATE teams SET {stat_type} = ? WHERE name = ?", (update_dic[team_name][stat_type]+old_value, team_name))
            conn.commit()
        conn.close()

def get_standings(league_name):
    if league_exists(league_name):
        conn = create_connection(league_name)
        if conn is not None:
            c = conn.cursor()

            c.execute("SELECT name, wins, losses, run_diff FROM teams",)
            standings_array = c.fetchall()
            conn.close()
            return standings_array

def season_save(league):
    if league_exists(league.name):
        seasons = 1
        with os.scandir(os.path.join(data_dir, league_dir, league.name)) as folder:
            for item in folder:
                if "." not in item.name:
                    seasons += 1
            new_dir = os.path.join(data_dir, league_dir, league.name, str(seasons))
            os.makedirs(new_dir)
        with os.scandir(os.path.join(data_dir, league_dir, league.name)) as folder:
            for item in folder:
                if "." in item.name:
                    os.rename(os.path.join(data_dir, league_dir, league.name, item.name), os.path.join(new_dir, item.name))

def get_past_standings(league_name, season_num):
    if league_exists(league_name):
         with os.scandir(os.path.join(data_dir, league_dir, league_name)) as folder:
            for item in folder:
                if item.name == str(season_num):
                    conn = create_season_connection(league_name, str(item.name))
                    if conn is not None:
                        c = conn.cursor()

                        c.execute("SELECT name, wins, losses, run_diff FROM teams",)
                        standings_array = c.fetchall()
                        conn.close()
                        return standings_array

def get_past_champion(league_name, season_num):
    if league_exists(league_name):
         with os.scandir(os.path.join(data_dir, league_dir, league_name)) as folder:
            for item in folder:
                if item.name == str(season_num):
                    with open(os.path.join(data_dir, league_dir, league_name, item.name, f"{league_name}.state")) as state_file:
                        state_dic = json.load(state_file)
                        return state_dic["champion"]

def league_exists(league_name):
    with os.scandir(os.path.join(data_dir, league_dir)) as folder:
        for subfolder in folder:
            if league_name == subfolder.name:
                with os.scandir(subfolder.path) as league_folder:
                    for item in league_folder:
                        if item.name == f"{league_name}.db":
                            return True
    return False