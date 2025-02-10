from __future__ import annotations

from typing import Any

from flask import redirect
from flask import render_template


class View:
    @staticmethod
    def render_template(template_name_or_list: str, **context: Any) -> Any:
        return render_template(template_name_or_list, **context)

    @staticmethod
    def redirect(location: str, code: int = 302, response: Any = None) -> Any:
        return redirect(location, code, response)
