from __future__ import annotations
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from ui.window.views import View

class ViewsManager:
    def __init__(self, *views: View):
        self.views = views
        self.current_view: Optional[View] = None

    def show(self, view_name: str, *args, **kwargs):
        try:
            self.current_view = next(filter(lambda v: v.__class__.__name__.replace("View", "") == view_name, self.views))
            self.current_view(*args, **kwargs)
        except StopIteration as e:
            raise Exception(f"View {view_name} doesn't exist") from e

    def show_error(self, message: str):
        if self.current_view is None:
            return
        self.current_view.show_error(message)

