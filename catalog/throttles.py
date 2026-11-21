from rest_framework.throttling import UserRateThrottle

# we made those to split the user request limit to certain number in minutes and in day 
class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'

class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'