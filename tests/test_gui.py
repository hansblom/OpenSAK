import pytest
from opensak.gui.mainwindow import MainWindow
from opensak.gui.cache_detail import CacheDetailPanel
from opensak.gui.map_widget import MapWidget
from opensak.gui.dialogs.settings_dialog import SettingsDialog
from opensak.gui.dialogs.import_dialog import ImportDialog
from opensak.gui.dialogs.database_dialog import NewDatabaseDialog
from opensak.gui.dialogs.filter_dialog import FilterDialog
from opensak.gui.dialogs.gps_dialog import GpsExportDialog
from opensak.gui.dialogs.found_dialog import FoundUpdaterDialog

@pytest.fixture
def app(qtbot):
    """Fixture to initialize the MainWindow and ensure the Qt event loop is active."""
    window = MainWindow()
    qtbot.add_widget(window)
    return window

# --- DIALOG TESTS ---

@pytest.mark.parametrize("dialog_class", [
    SettingsDialog,
    ImportDialog,
    NewDatabaseDialog,
    FilterDialog,
    GpsExportDialog,
    FoundUpdaterDialog,
])

def test_dialogs_instantiation(qtbot, app, dialog_class):
    """Verify that all major dialogs can be initialized without errors."""
    dialog = dialog_class(app)
    qtbot.add_widget(dialog)

    # Tiny wait to catch any asynchronous initialization crashes
    qtbot.wait(50) 
    assert dialog is not None 
    assert dialog.parent() == app 

# --- WIDGET TESTS ---

@pytest.mark.parametrize("widget_class", [
    CacheDetailPanel,
    MapWidget,
])

def test_widgets_instantiation(qtbot, app, widget_class):
    """Verify that main UI panels/widgets can be initialized."""
    widget = widget_class(app)
    qtbot.add_widget(widget)

    # Tiny wait to catch any asynchronous initialization crashes
    qtbot.wait(100)
    assert widget is not None