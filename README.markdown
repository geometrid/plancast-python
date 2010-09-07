# Plancast Python Wrapper

This is a premature Python wrapper for the [Plancast](http://plancast.com) API

It is not fully complete, but I wanted a quick wrapper to play with some of the Plancast
API and not have to worry about re-writing the usual auth and request code.

# Usage

Plancast API uses basic auth so you will need to pass in your credentials:
    
    plan = Plancast("example", "password")

Search for users with a given name:
    plan.search_users("mark")

Search for plans in Toronto
    plan.search_plans({'q': 'Toronto'})

Discover friends from a social network linked to the authenticated user's Plancast account:
    plan.discover_friends({'service': 'twitter'})

The plancast.py file has all the required parameters and options required for each implemeneted API call. More will
come as I go through the Plancast API, but the current implementations should be working.

Inspired by the Ruby version from [Wynn Netherland](http://github.com/pengwynn/plancast)
