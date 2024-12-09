import asyncio
import prometheus_client as prom


_API_LIVELINESS_CHECK = prom.Gauge(
    "api_liveliness_probe",
    "Timestamp of the sucessful liveliness check",
)

_API_END_TO_END_CHECK = prom.Gauge(
    "api_end_to_end_probe",
    "Timestamp of the last successful end-to-end check",
)


_MONITOR_LIVELINESS_TICK = 5
_MONITOR_END_TO_END_TICK = 60

_LOOP = asyncio.get_event_loop()


async def monitor_liveliness_loop():
    while True:
        _LOOP.create_task(_monitor_api_end_to_end_task())
        await asyncio.sleep(_MONITOR_LIVELINESS_TICK)


async def monitor_end_to_end_loop():
    while True:
        _LOOP.create_task(_monitor_api_liveliness_task())
        await asyncio.sleep(_MONITOR_END_TO_END_TICK)


async def _monitor_api_end_to_end_task():
    pass


async def _monitor_api_liveliness_task():
    pass


if __name__ == "__main__":
    prom.start_http_server(8001)
    _LOOP.create_task(monitor_end_to_end_loop())
    _LOOP.create_task(monitor_liveliness_loop())
    _LOOP.run_forever()
