# coding: utf-8
from flake8_import_order import ImportType
from flake8_import_order.styles import Error, Style

__all__ = ["Ruler501ImportOrderStyle"]

NAME_TYPE_CONSTANT = 'ALL_CAPS_STYLE'
NAME_TYPE_CLASS = 'CamelCaseStyle'
NAME_TYPE_FUNCTION = "underscore_style"
RELATIVE_SET = {ImportType.APPLICATION, ImportType.APPLICATION_RELATIVE}


class Ruler501ImportOrderStyle(Style):
    """
    All groups of imports require a line break between them, except packages within your application.
    
    All groups must be alphabetical horizontally and vertically.
    `from` import units are on separate lines sorted by constants first, followed by classes,
    followed by functions (i.e. CAPITAL_CASE, CamelCase, underscore_case).


    Group ordering:
    1. __future__
    2. builtins
    3. third-party, grouped by package
    4. application-import-names by package
    5. relative imports
    """
    @staticmethod
    def import_key(import_):
        package = None if import_.package is None else import_.package.lower()
        if import_.type in (ImportType.FUTURE, ImportType.STDLIB):
            return (
                import_.type,
                import_.is_from,
                package,
                import_.level,
                import_.modules,
                import_.names,
            )
        elif import_.type in {ImportType.THIRD_PARTY}:
            return (
                import_.type,
                package,
                import_.is_from,
                import_.level,
                import_.modules,
                import_.names,
            )
        else:
            return (
                import_.type,
                package,
                import_.is_from,
                import_.level,
                import_.modules,
                import_.names,
            )

    @staticmethod
    def same_section(previous, current):
        app_or_third = current.type in {ImportType.THIRD_PARTY, ImportType.APPLICATION}
        same_type = current.type == previous.type
        both_relative = {previous.type, current.type} <= RELATIVE_SET
        same_package = previous.package == current.package
        return (not app_or_third and same_type or both_relative) or (
            app_or_third and same_package
        )

    @staticmethod
    def sorted_names(names):
        # Names within an import line must be alphabetical.
        return sorted(names, key=lambda name: name.lower())

    @staticmethod
    def to_category(name):
        """
        Classifies a name as being either CAPITAL_CASE, CamelCase, or
        underscore_case.
        """
        if name.isupper():
            return NAME_TYPE_CLASS if len(name) == 1 else NAME_TYPE_CONSTANT
        elif name.islower():
            return NAME_TYPE_FUNCTION
        else:
            return NAME_TYPE_CLASS if name[0].isupper() else NAME_TYPE_FUNCTION
        
    def _check(self, previous_import, previous, current_import):
        yield from super(Ruler501ImportOrderStyle, self)._check(previous_import, previous, current_import)
        seen = set()
        for name in current_import.names:
            value = self.to_category(name)
            if value not in seen:
                seen.add(value)
                if len(seen) > 1:
                    yield Error(current_import.lineno,
                                'I204',
                                'Grouping combines {} import types in the same statement'.format(seen))
                    break 