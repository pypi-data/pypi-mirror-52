"""
Default configuration for timon
"""
default_cfg = dict(
    type="timon config",
    version="0.1",
    probes=dict(
        ),
    schedules=dict(
        ),
    probe_cls=dict(
        isup=dict(
            cls="timon.probes.IsUpProbe",
            ),
        diskfree=dict(
            cls="timon.probes.DiskFreeProbe",
            ),
        ),

)
