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

        # Ensure the window closes before the next test
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
    """
    Verifies that major dialogs can be instantiated and displayed.
    Uses waitUntil to synchronize with the event loop safely for CI.
    """
    dialog = dialog_class(app)
    qtbot.add_widget(dialog)
    
    # Show the dialog to test basic rendering
    dialog.show()
    
    # Wait until the dialog is visible (robust for headless environments)
    qtbot.waitUntil(lambda: dialog.isVisible(), timeout=1000)
    
    assert dialog is not None
    assert dialog.parent() == app
    assert dialog.isVisible()
    
    dialog.close()

# --- WIDGET TESTS ---

@pytest.mark.parametrize("widget_class", [
    CacheDetailPanel,
    MapWidget,
])

def test_widgets_instantiation(qtbot, app, widget_class):
    """Verifies that main UI panels/widgets initialize correctly."""
    widget = widget_class(app)
    qtbot.add_widget(widget)
    
    # Widgets embedded in MainWindow (like WebEngine) might take longer to init
    # qtbot.waitUntil processes events without blocking the system
    qtbot.waitUntil(lambda: widget is not None, timeout=1000)
    
    assert widget is not None