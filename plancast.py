#!/usr/bin/python

""" A simple Python wrapper around the Plancast api. """

import base64
import urllib
import urllib2

try:
    import simplejson as json
except ImportError:
    import json


class PlancastError(Exception):
    def __init__(self, data):
        errors = {
            401: UnauthorizedError,
            403: RateLimitExceeded,
            404: NotFound,
            500: ServerError,
        }
        raise errors.get(data.code, UnknownError)(data)

class UnauthorizedError(Exception): pass
class RateLimitExceeded(Exception): pass
class NotFound(Exception): pass
class ServerError(Exception): pass
class UnknownError(Exception): pass


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

    def update_subscription(self, query):
        """
        Subscribes the authenticated user to a target user and returns information about the target user. 
        If the target user has enabled account protection, a subscription request will be sent.

        @param: `user_id` or `username` - The user identifier to lookup.
        @example:
            plan.update_subscription({'username': 'bartekci'})
        """
        return self.get("/subscriptions/update", query)

    def destroy_subscription(self, query):
        """
        Stops the authenticated user from subscribing to a target user and returns information about the target user

        @param: `user_id` or `username` - The user identifier to lookup.
        @example:
            plan.destroy_subscription({'username': 'bartekci'})
        """
        return self.get("/subscriptions/destroy", query)

    def plans(self, query):
        """
        Returns a given user's plans.

        @param: `user_id` or `username` - The user identifier to lookup.
        @option: `view_type` (default: schedule) - The type of plans to return
                    See http://groups.google.com/group/plancast-api/web/listing-view-types
        @option: `page` (default: 1) - Page number
        @option: `count` (default 25, max 100) - Number of plans per page.
        @option: `extensions` (possible values: attendees, comments, place) - Comma-delimited list of
                        extended data types you want; ommitted by default to minimize response size.
        @example:
            plan.plans({'username': 'bartekci'})
        """
        return self.get("/plans/user", query)

    def home(self, query=None):
        """
        Returns plans on the authenticated user's homepage (their own plans, plus their subscribers.)

        @option: `view_type` (default: schedule) - The type of plans to return
                    See http://groups.google.com/group/plancast-api/web/listing-view-types
        @option: `page` (default: 1) - Page number
        @option: `count` (default 25, max 100) - Number of plans per page.
        @option: `extensions` (possible values: attendees, comments, place) - Comma-delimited list of
                        extended data types you want; ommitted by default to minimize response size.
        @example:
            plan.home({'view_type': 'past'})
        """
        return self.get("/plans/home", query)
    
    def show(self, query):
        """
        Returns the details for a given plan.

        One of the following parameters are required:
        @param: `attendance_id` - The ID of an attendance, in base 36
        - Or -
        @param: `plan_id` - The ID of a plan, in base 36.
        See: http://groups.google.com/group/plancast-api/web/plans-vs-attendances

        @option: `extensions` (possible values: attendees, comments, place) - Comma-delimited list of
                        extended data types you want; ommitted by default to minimize response size.
        @example:
            plan.show({'plan_id': 'enf'})
        """
        return self.get("/plans/show", query)
    
    def update(self, query):
        """
        Creates a new plan or updates the details of an existing plan. 
        Returns up-to-date information about the plan in either case.

        @param: `what` - Brief descriptor of the plan.
        @param: `when` - String descriptor of plan's date/time; Plancast takes this and parses it into timestamps for you.
                    Highly recommended to use the `parse_when` method to verify that the string is parseable first.
        @param: `where` - String descriptor of the plan's location.
        @option: `place_id` - Optional but highly recommended. ID of a canonical place record retrieved using `parse_where` method.
        @option: `external_url` - URL for more information about this place.
        @option: `description` - Longer, more free-form descriptor of the plan.
        @option: `syndicate_facebook` - (Default: user's default) Whether to syndicate the plan to Facebook, if auth is available.
        @option: `syndicate_twitter` - (Default: user's default) Whether to syndicate the plan to Twitter, if auth is available.
        @option: `plan_id` or `attendance_id` - Base 36 ID of an existing plan or attendance; provide this if you'd
                    like to update a plan instead of creating a new one.
        @example:
            plan.update({
                'what': 'Drinks For Everyone',
                'when': 'September 20th @ 7pm',
                'where': 'The Rhino',
            })
        """
        return self.get("/plans/update", query)

    def attend(self, query=None):
        """
        Adds an attendance for a particular plan for the authenticated user and returns information about it.

        @param: `plan_id` or `attendance_id` - Base 36 ID of plan or existing attendance for a plan.
        @option: `syndicate_facebook` - (Default: user's default) Whether to syndicate the plan to Facebook, if auth is available.
        @option: `syndicate_twitter` - (Default: user's default) Whether to syndicate the plan to Twitter, if auth is available.
        @example:
            plan.attend({'plan_id': 'enf'})

        """
        return self.get("/plans/attend", query)

    def destroy(self, query):
        """
        Deletes an attendance for the authenticated user and returns its previous information.

        Note: this destroys an attendance not an actual plan, which may be shared with others. If the attendance is 
        destroyed, any other attendances and the plan with which they are associated will remain. If this is the 
        only attendance for the plan, the plan will still exist in the database but it will be orphaned and 
        virtually deleted as far as users are concerned. 
        See: http://groups.google.com/group/plancast-api/web/plans-vs-attendances for more information

        @param: `plan_id` or `attendance_id` - Base 36 ID of plan or existing attendance for a plan.
        @example:
            plan.destroy({'plan_id': 'enf'})
        """
        return self.get("/plans/destroy", query)

    def search_plans(self, query={}):
        """
        Returns up to 25 plans that match the given keyword(s).

        @param: `q` - Keyword(s) to search for in plans.
        @option: (Comma-Delimited Strings) - Extensions for more data like `attendees`, `comments`, `place`. Ommitted by 
                    default to minimize the response.
        @example:
            plan.search_plans({'q': 'beer'})
        """

        return self.get("/plans/search", query)

    def parse_when(self, when):
        """
        Attempts to parse a string for datetime information and returns the result if successful. 
        Use this to verify a "when" string before submitting a new plan with the `update` method.
        
        @param: The time string to parse.
        @example:
            plan.parse_when("September 7th @ 7pm")
        """
        return self.get("/plans/parse_when", {'when': when})

    def parse_where(self, where):
        """"
        Looks up places based on a keyword string and returns matches. 
        Use this to get a place ID from a "where" string before submitting a new plan with plans/update.

        @param: The location keyword to parse.
        """
        return self.get("/plans/parse_where", {'where': where})

    def update_comment(self, query):
        """
        Creates a new comment on a plan and returns information about it.

        @param: `content` - Content of the comment.
        @param: `plan_id` or `attendance_id` - Base 36 ID of plan or existing attendance for a plan.
        @example:
            plan.update_comment({
                'content': 'Hello, this is a cool.',
                'plan_id': '289a',
            })
        """
        return self.get("/comments/update", query)

    def destroy_comment(self, comment_id):
        """
        Deletes a comment for the authenticated user and returns its previous information.

        @param: The comment id.
        @example:
            plan.destroy_comment("7511")
        """
        return self.get("/comments/destroy", {'comment_id': comment_id})

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
            raise PlancastError(e)

        return handle
