import pytest
from unittest.mock import patch, MagicMock

# GUI Component Imports
from opensak.gui.mainwindow import MainWindow
from opensak.gui.cache_detail import CacheDetailPanel
from opensak.gui.map_widget import MapWidget
from opensak.gui.dialogs import (
    settings_dialog,
    import_dialog,
    database_dialog,
    filter_dialog,
    gps_dialog,
    found_dialog
)

@pytest.fixture
def app(qtbot):
    """
    Fixture to initialize dependencies and the MainWindow.
    """

    # Mock ZipFile to prevent MainWindow from trying to open non-existent files
    with patch("zipfile.ZipFile", MagicMock()):
        window = MainWindow()
        qtbot.add_widget(window)
        yield window
        window.close()

# --- DIALOG TESTS ---

@pytest.mark.parametrize("dialog_name, dialog_class", [
    ("SettingsDialog", settings_dialog.SettingsDialog),
    ("ImportDialog", import_dialog.ImportDialog),
    ("NewDatabaseDialog", database_dialog.NewDatabaseDialog),
    ("FilterDialog", filter_dialog.FilterDialog),
    ("GpsExportDialog", gps_dialog.GpsExportDialog),
    ("FoundUpdaterDialog", found_dialog.FoundUpdaterDialog),
])

def test_dialogs_instantiation(qtbot, app, dialog_name, dialog_class):
    """Verifies that major dialogs can be instantiated and displayed."""
    dialog = dialog_class(app)
    qtbot.add_widget(dialog)
    
    dialog.show()
    qtbot.waitUntil(lambda: dialog.isVisible(), timeout=1000)
    
    assert dialog is not None
    assert dialog.isVisible()
    
    dialog.close()

# --- WIDGET TESTS ---

@pytest.mark.parametrize("widget_class", [
    CacheDetailPanel,
    MapWidget,
])

def test_widgets_instantiation(qtbot, app, widget_class, request):
    """Verifies that main UI panels/widgets initialize correctly."""
    widget = widget_class(app)
    # We add it to qtbot for safety, but we will "capture" it for manual cleanup
    qtbot.add_widget(widget)
    
    qtbot.waitUntil(lambda: widget is not None, timeout=2000)
    assert widget is not None

    # --- SAFE CLEANUP TO PREVENT SEGFAULT & RUNTIMERROR ---
    # 1. Remove the widget from pytest-qt's internal tracking list 
    # so it doesn't try to close it again during teardown.
    if hasattr(request.node, "qt_widgets"):
        request.node.qt_widgets = [
            (w_ref, skip_func) for w_ref, skip_func in request.node.qt_widgets 
            if w_ref() is not widget
        ]

    # 2. Now manually trigger the WebEngine-safe deletion
    widget.setParent(None)
    widget.deleteLater()
    
    # 3. Quickly flush the event loop
    qtbot.wait(50)