import yaml
import asyncio
import logging

with open("./config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)


logcfg = cfg["logging"]
logging.basicConfig(
    format=logcfg["format"],
    datefmt=logcfg["datefmt"],
    level=logging.__getattribute__(logcfg["level"].upper()),
)


if __name__ == "__main__":
    from cycler import Cycler

    cycler = Cycler(cfg)
    asyncio.run(cycler.cycle_forever())
