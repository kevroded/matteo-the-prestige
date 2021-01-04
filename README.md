# A simsim fork for the FredChat

This fork changes small things about the bot to better fit in in the FredChat discord. The official readme can be seen below and a summary of changes is viewable directly below this 
- Removes almost all references to Matteo as that is not the name of the bot user
- Adds in new weather effects
- Adds the help command as the bot's status
- Shows a players vibes when requesting their stats
- Updated the credit command to credit Sakimori and SIBR instead of the pfp artist as the original profile pic is not being used
- Game history can be viewed in the same style embed as showallteams

# matteo-the-prestige
# simsim discord bot

blaseball, blaseball, is back! in an unofficial capacity.

custom players, custom teams, custom leagues (that last one is coming soon™) all in discord! 

we've also got things like custom team creation, easy setup for your teams to play against each other, and player idolization, all powered by this bot and onomancer.

accepting pull requests, check the issues for to-dos.


## commands: (everything here is case sensitive, and can be prefixed with either m; or m!)

### team commands:
- m;saveteam
  - saves a team to the database allowing it to be used for games. send this command at the top of a list, with entries separated by new lines (shift+enter in discord, or copy+paste from notepad).
	- the first line of the list is your team's name (cannot contain emoji).
	- the second line is your team's icon and slogan, this should begin with an emoji followed by a space, followed by a short slogan.
	- the next lines are your batters' names in the order you want them to appear in your lineup, lineups can contain any number of batters between 1 and 12.
	- the final line is your pitcher's name.
  - if you did it correctly, you'll get a team embed with a prompt to confirm. hit the 👍 and it'll be saved.
- m;showteam [name]
  - shows information about any saved team.
- m;showallteams
  - shows a paginated list of all teams available for games which can be scrolled through.	  
- m;searchteams [searchterm]
  - shows a paginated list of all teams whose names contain the given search term.
- m;deleteteam [teamname]
  - allows you to delete the team with the provided name if you are the owner of it, gives a confirmation first to prevent accidental deletions. if it isn't letting you delete your team, you probably created it before teams having owners was a thing, contact xvi and xie can assign you as the owner.
- m;import
  - imports an onomancer collection as a new team. you can use the new onomancer simsim setting to ensure compatibility.
  
### player commands:	 
- m;showplayer [name]
  - displays any name's stars, there's a limit of 70 characters. that should be *plenty*. note: if you want to lookup a lot of different players you can do it on onomancer instead of spamming this command a bunch and clogging up discord: https://onomancer.sibr.dev/reflect
- m;idolize [name]
  - records any name as your idol, mostly for fun.
- m;showidol 
  - displays your idol's name and stars.
  
### game commands:
- m;startgame
  - starts a game with premade teams made using saveteam, use this command at the top of a list followed by each of these in a new line:
	- the away team's name.
	- the home team's name.
	- and finally, optionally, the number of innings, which must be greater than 2 and less than 31. if not included it will default to 9.	  

### other commands:
- m;help [command]
  - shows the instructions from here for given command. if no command is provided, it will instead provide a list of all of the commands that instructions can be provided for.    
- m;credit
  - shows artist credit for matteo's avatar.  
- m;roman [number]
  - converts any natural number less than 4,000,000 into roman numerals, this one is just for fun.

## patreon!

these folks are helping me a *ton* via patreon, and i cannot possibly thank them enough:
- Ale Humano
- Chris Denmark
- Astrid Bek
