# Plancast Python Wrapper

This is a Python wrapper for the [Plancast](http://plancast.com) API

It has been tested, but lightly. I do my best to keep things up to date and working but if you
happen to notice something please make me aware and I'll do my best to fix it quickly!

# Usage

Plancast API uses basic auth so you will need to pass in your credentials:
    
    plan = Plancast("example", "password")

Search for users with a given name:
    plan.search_users("mark")

Search for plans in Toronto
    plan.search_plans({'q': 'Toronto'})

Discover friends from a social network linked to the authenticated user's Plancast account:
    plan.discover_friends({'service': 'twitter'})

Create a new plan:
    plan.update({
        'what': 'Drinks For Everyone',
        'when': 'September 20th @ 7pm',
        'where': 'The Rhino',
    })

The plancast.py file has all the required parameters and options required for each API call. 

Inspired plenty by the Ruby version from [Wynn Netherland](http://github.com/pengwynn/plancast)
