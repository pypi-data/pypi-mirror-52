__version__ = [1, 0, 3]
"""list: of `[major, minor, bugfix]` version numbers for the package.
"""

from datacustodian.datacustodian_app import run, app, start, stop, set_loop
def get_event_loop():
    from datacustodian.datacustodian_app import loop
    return loop

def get_version():
    """Returns the version of the package formatted as a string.
    """
    return '.'.join(map(str, __version__))

def application_ready():
    """Checks to see if the application has finished initializing *and* the
    agents have all finished initializing by checking the :class:`threading.Event`
    flags.
    """
    from datacustodian.datacustodian_app import started
    from datacustodian.dlt import agent_events
    agents_ready = False
    for agent_name, event in agent_events.items():
        agents_ready = agents_ready and event.is_set()
        if not agents_ready:
            break

    return agents_ready and started.is_set()
