"""
Rewrite the URLs in anything that looks like a string, dict or list.
"""
from typing import Iterable, Optional, Union

from .models import URLRewrite


def _rewrite_url(value: str, rewrites: Iterable) -> Optional[str]:
    for start, replacement in rewrites:
        if not value.startswith(start):
            continue

        return value.replace(start, replacement, 1)

    return None


class Rewriter:
    def __init__(self):
        self.rewrites = URLRewrite.objects.values_list("from_value", "to_value")

    @property
    def reverse_rewrites(self):
        return [(to_value, from_value) for from_value, to_value in self.rewrites]

    def forwards(self, data: Union[list, dict]):
        """
        Rewrite URLs from from_value to to_value.
        """
        self._rewrite(data, self.rewrites)

    def backwards(self, data: Union[list, dict]):
        """
        Rewrite URLs from to_value to from_value.
        """
        self._rewrite(data, self.reverse_rewrites)

    def _rewrite(self, data: Union[list, dict], rewrites: Iterable) -> None:
        if isinstance(data, list):
            new_items = []
            for item in data:
                if isinstance(item, str):
                    new_value = _rewrite_url(item, rewrites)
                    if new_value:
                        new_items.append(new_value)
                    else:
                        new_items.append(item)
                else:
                    self._rewrite(item, rewrites=rewrites)
                    new_items.append(item)

            # replace list elements
            assert len(new_items) == len(data)
            for i in range(len(data)):
                data[i] = new_items[i]
            return

        assert isinstance(data, dict)

        for key, value in data.items():
            if isinstance(value, (dict, list)):
                self._rewrite(value, rewrites=rewrites)
                continue

            elif not isinstance(value, str):
                continue

            assert isinstance(value, str)

            rewritten = _rewrite_url(value, rewrites)
            if rewritten is not None:
                data[key] = rewritten
