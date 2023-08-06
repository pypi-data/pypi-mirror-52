class Rule:
    """Squirrel Firewall Rule"""

    def __init__(self, *args, **kwargs):
        """On init, test condition  """
        try:
            self.condition(*args, **kwargs)
        except Exception as e:
            self.on_condition_fails(exception_raised=e)

    def on_condition_fails(self, exception_raised, *args, **kwargs): ...

    def condition(self, *args, **kwargs): ...


DEFAULT_FIREWALL_RULES = [

]


class Firewall:
    """Squirrel Firewall"""
    rules_classes: [Rule] = []
    rules_are_loaded = False

    def load_rules_classes(self):
        self.rules_classes = DEFAULT_FIREWALL_RULES
        self.rules_are_loaded = True

    def firewall(self, **input_data):
        if self.rules_are_loaded:
            self.load_rules_classes()
        for rule_class in self.rules_classes:
            rule_class(**input_data)
