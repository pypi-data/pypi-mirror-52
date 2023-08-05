# SPTAG

## Quick Start

### Creating random index

First, using 'hawking cli' create an embedding table:

```
hawking batch-index
```

Then, create SPTAG index using indexbuilder:

```
./indexbuilder -o /host/index/rand-index-docs-100-dim-10 -i /host/index/random-docs-100-dim-10.em  -a BKT -d 10 -v Float
```

### Serving the index

To serve an index, run:

Update the service.ini and update the `IndexFolder`:

```
[Service]
ListenAddr=0.0.0.0
ListenPort=5000
ThreadNumber=8
SocketThreadNumber=8

[QueryConfig]
DefaultMaxResultNumber=10
DefaultSeparator=|

[Index]
List=BKT

[Index_BKT]
IndexFolder=/host/index/rand-index-docs-100-dim-10
```

Then run the SPTAG server:

```
./server -c service.ini -m socket
```

### Sending query to SPTAG server

Using `hawking cli`, run:

```
hawking remote-query "elon musk" "artificial intelligence" -s 127.0.0.1 -p 5000
```

Note that, if you run the server on AWS/GCP, update the server **ip address** and **port** accordingly.
