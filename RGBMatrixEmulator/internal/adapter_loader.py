import importlib, sys, traceback

from enum import Enum, auto

from RGBMatrixEmulator.logger import Logger

from RGBMatrixEmulator.adapters import ADAPTERS


class LoadResult(Enum):
    SUCCESS = auto()
    FAILURE = auto()
    SKIPPED = auto()

    DEFAULT = SKIPPED


class AdapterLoader():

    def __init__(self, requested_adapter):
        self.requested_adapter = requested_adapter.lower()
        self.adapter_priority = [self.requested_adapter] + [adapter_name for adapter_name in list(ADAPTERS.keys()) if adapter_name != self.requested_adapter]
        self.adapter = None

        self._loaded = False
        self._adapters = {}

    def load(self, fallback=False):
        if self._loaded:
            return self.adapter

        exceptions = []        

        for adapter_name in self.adapter_priority:
            (result, adapter, tb) = self._load(adapter_name, fallback=fallback)

            if result == LoadResult.SKIPPED:
                continue
            elif result == LoadResult.FAILURE:
                if tb is not None:
                    exceptions.append((adapter_name, tb))
            else:
                self._loaded = True
                self.adapter = adapter

                break

        if self._loaded:
            return self.adapter

        Logger.critical("All available display adapters failed to load!")

        for adapter_name, tb in exceptions:
            Logger.error(f"Adapter '{adapter_name}' failed with error:")
            Logger.error(tb)

        sys.exit(1)
                
    def _load(self, adapter_name, fallback=False):
        try:
            adapter_config = ADAPTERS[adapter_name]
            package_path = adapter_config.get("path")
            adapter_class = adapter_config.get("class")
            valid_fallback = adapter_config.get("fallback")

            if self.requested_adapter != adapter_name and not valid_fallback:
                return (LoadResult.SKIPPED, None, None)

            package = importlib.import_module(package_path)
            adapter = getattr(package, adapter_class)

            self._adapters[adapter_name] = adapter

            return (LoadResult.SUCCESS, adapter, None)
        except Exception as e:
            if fallback:
                return (LoadResult.FAILURE, None, traceback.format_exc())

            Logger.exception("Display adapter load failed with no fallback configured!")
            Logger.exception(e)

            sys.exit(1)
