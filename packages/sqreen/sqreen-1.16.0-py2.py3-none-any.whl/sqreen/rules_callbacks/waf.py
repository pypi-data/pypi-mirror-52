# -*- coding: utf-8 -*-
# Copyright (c) 2016, 2017, 2018, 2019 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#

import hashlib
import logging
from threading import Lock
from weakref import WeakKeyDictionary

from ..binding_accessor import BindingAccessor
from ..exceptions import InvalidArgument
from ..rules import RuleCallback
from ..utils import is_unicode

try:
    from sq_native import waf
except ImportError:
    waf = None  # pragma: no cover


LOGGER = logging.getLogger(__name__)


class WAFInstance:
    """
    Per runner WAF instance.
    """

    DEFAULT_BUDGET = 5000

    def __init__(self, waf_rules_id, waf_rules):
        ret = waf.initialize(waf_rules_id, waf_rules)
        if ret is not True:
            msg = "failed to initialize the WAF rules"
            raise InvalidArgument(msg)
        self._waf_rules_id = waf_rules_id

    def run(self, params, budget=None):
        """ Run the WAF on the parameters.
        """
        return waf.run(self._waf_rules_id, params, budget or self.DEFAULT_BUDGET)

    def __del__(self):
        if self._waf_rules_id is not None:
            waf.clear(self._waf_rules_id)

    class DummyRunner:
        pass

    _pool = WeakKeyDictionary()
    _lock = Lock()
    _dummy_runner = DummyRunner()

    @classmethod
    def get_for_runner(cls, waf_rules_name, waf_rules, runner=None):
        """ Get the WAF instance associated with the runner.
        """
        if runner is None:
            runner = cls._dummy_runner

        if is_unicode(waf_rules):
            waf_rules = waf_rules.encode("utf-8")
        if not isinstance(waf_rules, bytes):
            raise InvalidArgument("Invalid WAF rules")

        waf_rules_hash = hashlib.sha256(waf_rules).hexdigest()
        waf_rules_id = "{}_{}".format(waf_rules_hash, waf_rules_name)

        with cls._lock:
            instances = cls._pool.get(runner)
            if instances is None:
                instances = cls._pool[runner] = {}
            instance = instances.get(waf_rules_id)
            if instance is None or instance._waf_rules_id != waf_rules_id:
                LOGGER.debug("Instanciate new WAF context for %s", waf_rules_id)
                instance = instances[waf_rules_id] = cls(
                    waf_rules_id, waf_rules)
            return instance


class WAFCB(RuleCallback):
    """ WAF Callback
    """

    def __init__(self, *args, **kwargs):
        super(WAFCB, self).__init__(*args, **kwargs)
        if not self.module_is_available():
            msg = "WAF is disabled because the native module is not installed"
            raise InvalidArgument(msg)

        values = self.data.get("values", {})
        waf_rules = values.get("waf_rules")

        self._inst = WAFInstance.get_for_runner(self.rule_name, waf_rules, self.runner)

        bas = {}
        for expr in values.get("binding_accessors", []):
            bas[expr] = BindingAccessor(expr)
        self.binding_accessors = bas
        self._budget = values.get("budget", None)

    def pre(self, original, *args, **kwargs):
        request = self.storage.get_current_request()
        if request is None:
            return

        binding_eval_args = {
            "binding": locals(),
            "global_binding": globals(),
            "framework": request,
            "instance": original,
            "arguments": self.storage.get_current_args(args),
            "kwarguments": kwargs,
            "cbdata": self.data,
            "return_value": None,
        }

        params = {}
        for expr, ba in self.binding_accessors.items():
            params[expr] = ba.resolve(**binding_eval_args)

        LOGGER.debug("WAF run with parameters: %r", params)
        ret = self._inst.run(params, budget=self._budget)
        LOGGER.debug("WAF returned: %r", ret)
        if ret.action in (waf.PW_BLOCK, waf.PW_MONITOR):
            self.record_attack({
                "waf_data": ret.data,
                # This is a hack based on the rule name.
                "ba_type": "php-daemon" if "daemon" in self.rule_name else "python"
            })
            if ret.action == waf.PW_BLOCK and self.block is True:
                return {"status": "raise", "rule_name": self.rule_name}
        elif ret.action < 0:
            raise RuntimeError("WAF returned unexpected action: %r", ret)

    @staticmethod
    def module_is_available():
        """ Return True if the native module is present, False otherwise.
        """
        return waf is not None
