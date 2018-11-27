## Coding Question

Write an interface for a data structure that can provide the moving average of the last N elements added, add elements to the structure and get access to the elements. Provide an efficient implementation of the interface for the data structure.

### Minimum Requirements

1. Provide a separate interface (IE `interface`/`trait`) with documentation for the data structure
2. Provide an implementation for the interface
3. Provide any additional explanation about the interface and implementation in a README file.

### Running

clone this repo into CHALLENGE_PATH 

run the command below (assuming docker is installed)
```
docker run -it --entrypoint /code/entrypoint.sh --name server -v CHALLENGE_PATH:/code -p 8888:8888 --rm sepehrv/redis-server
```

access http://localhost:8888/demo for the demo

and access http://localhost:8888/trait for the documentation

### Design and assumptions

The solution has a two layer architecture with a user facing interface and backend that take care of storing values into the database.

Layers are RQ message broker connects the web interface to the workers. Queries for adding new number get Queued by RQ and consumed by the workers and get written into a Redis DB. 

This design is based on the assumption that write queries are far more than read queries and therefore the focus was to optimize that part. The read query (e.g, runnung average and access to elements) are considered more of an analytical toolkit with an occasional use. However they can be optimized given different requirements.

### Implementation

stack is in python with some JS for the frontend. Webserver is implemented using Flask. Redis is chosen as DB due to its efficiancy. 

Each element is stored with a time stamp for sorting and a unique identifier for retrival purposess.

Deployed by a docker image (pushed to my docker hub cloud). 

can be scaled to many workers accross machines easily. 

Unique identifier for each element will random access to the data 



