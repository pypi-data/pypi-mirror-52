# cloudmicro platform library

As most services require the requests to them to be authenticated and checked
for permissions - the speed of traversing these requests via HTTPS is 
prohibitive. Therefore, we give each service direct access to the platform
database to query via predefined methods.

This library also includes license, provider and user JSON serialisation. 

Our mission is to have all single resource requests to return in under
100ms, and this will never happen if we have to authenticate between
microservices. 

