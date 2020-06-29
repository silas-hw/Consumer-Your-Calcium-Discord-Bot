# Consumer-Your-Calcium-Discord-Bot
official discord bot for the Consume Your Calcium discord,     
providing useful tools for members and admins

## what does it do?
### Set reminders
Reminders mention users or roles after a certain amount of time  
  
To use the command in discord type:  
`//reminder @user/role time "message to be displayed"`  
    
after the given time has passed the bot would send:  
`@user/role message to be displayed (reminder set by @user)`  
  
the time can either be in minutes (e.g 5) or as a 24 hour timestamp (e.g 14:23)  
  
### inform you if a user is afk  
If a user is afk or has set themself as afk the bot will inform you if you mention them  

### Set custom prefixes  
With the custom prefix command changing the bots command prefix is much easier and allows for custom prefixes per server    
  
simply type:
`//prefix customPrefix`  
  
## Send bot update announcements  
**This command can only be accessed by the bot owner**  
  
The bot has the ability to send announcements for updates to the bot  
Announcements always mention everyone  
  
`//announce "announcement text"`  

## Built with  
  
* [discord.py](https://discordpy.readthedocs.io/en/latest/) for the main discord bot framework  
* [asyncio](https://docs.python.org/3/library/asyncio.html) for asynchronous functions  
* [python](https://www.python.org/) as the main programming language    
* [pytz](https://pypi.org/project/pytz/) for timezones  

## Hosted by  
* [heroku](www.heroku.com)

## Authors
* [CleanlyWolf/Silas Hayes-Williams](https://twitter.com/silas_hw) *(twitter)*  
  
## Special thanks  
* [ZOD14C](https://steamcommunity.com/profiles/76561198985320935) *(steam)* for creating the Consume Your Calcium server  
* [Theblockbuster1](https://github.com/Theblockbuster1) *(github)* for helping with understanding of code
