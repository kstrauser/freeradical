# Helper scripts

## instance_rank.py

Use `instance_rank.py` to get an instance's ranking on a number of stats, as seen at the [quasi-official instance list](https://instances.social/list/old).

Example usage:

```shell
$ scripts/instance_rank.py freeradical.zone
Instances: 2044

Column          Value     Rank  Pctl
------------------------------------
Connections     2939        39  98.1
PerUser         121.067    592  71.0
Registrations   False     2044   0.0
Score           100.89      44  97.8
Statuses        66224      115  94.4
Up              True      1804  11.7
Uptime          99.785    1281  37.3
Users           547        147  92.8
Version         2.4.5      558  72.7
```

This was something I knocked out for fun. Please, _please_ let's please not make this a competition.
