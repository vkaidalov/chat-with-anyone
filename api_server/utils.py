import trafaret as tr


TRAFARET = tr.Dict({
    tr.Key('postgres'):
        tr.Dict({
            'database': tr.String(),
            'user': tr.String(),
            'password': tr.String(),
            'host': tr.String(),
            'port': tr.Int(),
            'pool_min_size': tr.Int(),
            'pool_max_size': tr.Int(),
        }),
    tr.Key('host'): tr.IP,
    tr.Key('port'): tr.Int(),
})
