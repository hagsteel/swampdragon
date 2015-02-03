# Choosing a base router

Depending on your intent behind the router there are a few guidelines to selecting a router:


## BaseRouter

If you don't intend to use a Django model with your router, then extend the ```BaseRouter```.

For more information on how to use the BaseRouter see [the BaseRouter](/documentation/routers-base-router).


## ModelRouter

If you are using a self-publishing model, choose this router, as the ```ModelPublisherRouter``` would issue two updates unless you override the ```updated``` function.

This is also a good alternative if you are not relying on the publishing feature of the router.

For more information see [ModelRouter](/documentation/routers-base-model-router).


## ModelPublisherRouter

If you don't intend to use self-publishing models and want to benefit from having more granular control over the model data being published, then use the ```ModelPublisherRouter```.

For more information see [ModelPublisherRouter](/documentation/routers-base-model-publisher-router).
