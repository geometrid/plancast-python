#!/usr/bin/python

""" A simple Python wrapper around the Plancast api. """

import pickle
import base64
import urllib
import urllib2
import json

class PlancastError(Exception):
    def __init__(self, data):
        self.data = data

class UnauthorizedError(PlancastError):
    pass

class Plancast(object):
    def __init__(self, username=None, password=None, version="02", format=".json"):

        self.username = username
        self.password = password
        self.base_url = "http://api.plancast.com/%s" % version
        self.format = format
        self.data = None

    def verify_credentials(self):
        """
        Returns information about the authenticated user. 
        This method can be used to initially authenticate a user and verify their information.

        Requires authentication.
        """
        return self.get("/account/verify_credentials")

    def user(self, query):
        """
        @param: `user_id` or `username` - The user identifer to look up.
        @example:
            plancast.user({'username': 'bartekci'}) 
        """
        return self.get("/users/show", query)

    def subscriptions(self, query):
        """
        Returns the user to which a given user is subscribed.

        @param: `user_id` or `username` - The user identifier to look up.
        @option: `page` (Default: 1) - Page number, with 25 users returned per page.
        @example:
            plan.subscriptions({'username': 'bartekci'})
        """
        return self.get("/users/subscriptions", query)
        
    def subscribers(self, query):
        """
        Returns the users who are subscribed to a given user.

        @param: `user_id` or `username` - The user identifier to look up.
        @option: `page` (Default: 1) - Page number, with 25 users returned per page.
        @example:
            plan.subscribers({'username': 'bartekci'})

        """
        return self.get("/users/subscribers", query)

    def discover_friends(self, query):
        """
        Returns the users connected to the authenticated user on a given network (Facebook or Twitter)

        @param: `service` - Possible values (facebook, twitter) Which service to return friends from.
        @option: `page` (Default: 1) - Page number, with 25 users returned per page.
        @example:
            plan.discover_friends({'service': 'twitter'})
        """
        return self.get("/users/discover_friends", query)

    def search_users(self, query):
        """
        Returns up to 25 users that match the given keyword(s)

        @param: Keyword(s) containing the user to look up.
        @example:
            plan.search_users("mark")
        """
        return self.get("/users/search", {'q' : query})

    def parse_where(self, where):
        """"
        Looks up places based on a keyword string and returns matches. 
        Use this to get a place ID from a "where" string before submitting a new plan with plans/update.

        @ The location keyword to parse.
        """
        return self.get("/plans/parse_where", {'where': where})

    def search_plans(self, query={}):
        """
        Returns up to 25 plans that match the given keyword(s).

        @param: `q` - Keyword(s) to search for in plans.
        @option: (Comma-Delimited Strings) - Extensions for more data like `attendees`, `comments`, `place`. Ommited by 
                    default to minimize the response.
        @example:
            plancast.search({'q': 'beer'})
        """

        return self.get("/plans/search", query)

    def get(self, endpoint, query=None):
        if query:
            self.data = urllib.urlencode(query)

        req = urllib2.Request("%s%s%s" % (self.base_url, endpoint, self.format), self.data)

        if self.username and self.password:
            base64auth = base64.encodestring("%s:%s" % (self.username, self.password))[:-1]
            authheader = "Basic %s" % base64auth
            req.add_header("Authorization", authheader)

        try:
            handle = json.loads(urllib2.urlopen(req).read())
        except urllib2.HTTPError, e:
            raise Exception(e)

        return handle
