Swamp Dragon
============

# UNDER DEVELOPMENT

Swamp Dragon is a pub/sub solution running on top of Tornado, and is compatible with Django models.
It allows data to be published to channels via routers and does all the heavy lifting.


# Important
**Note**: As Django models are blocking, long queries will prevent other requests to come through.

**Note**: Currently it's heavily tied to Django

**Note**: All serializers needs to reside in serializers.py

**Note**: Angular doesn't include a checkbox ng-model unless a value is set.
This means adding a checkbox with ng-model="mymodel.flag" will not be included when submitting data,
unless the checkbox is ticked or mymodel is initiated ```scope.mymodel = { flag=false };```

**Note**: Calling update on a queryset won't work on self publishing models.
i.e ```MyModel.objects.all().update(foo=bar)``` won't trigger a publishing action


#TODO
*  Auto discover routes returns URLs and needs to be renamed
*  Write documentation
*  Add instructions for swampDragon.call = function(verb, route, channel, args, callbackName)
*  Add instructions on self publishing models
*  term_match_check: make sure compared values are of the same type
*  Filter case sensitivity
