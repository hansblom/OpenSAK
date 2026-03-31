"""
src/opensak/gui/dialogs/waypoint_dialog.py — Tilføj/Rediger cache dialog.
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QTextEdit, QComboBox,
    QDoubleSpinBox, QSpinBox, QCheckBox,
    QPushButton, QDialogButtonBox, QTabWidget,
    QWidget, QGroupBox, QMessageBox
)

from opensak.db.models import Cache
from opensak.lang import tr


# ── Konstanter ────────────────────────────────────────────────────────────────

CACHE_TYPES = [
    "Traditional Cache",
    "Multi-cache",
    "Unknown Cache",
    "Letterbox Hybrid",
    "Wherigo Cache",
    "Event Cache",
    "Mega-Event Cache",
    "Earthcache",
    "Virtual Cache",
    "Webcam Cache",
]

CONTAINER_SIZES = [
    "Nano",
    "Micro",
    "Small",
    "Regular",
    "Large",
    "Other",
    "Not chosen",
]


class WaypointDialog(QDialog):
    """
    Dialog til at tilføje eller redigere en cache manuelt.
    """

    def __init__(self, parent=None, cache: Optional[Cache] = None):
        super().__init__(parent)
        self._cache = cache
        self._is_edit = cache is not None
        self.setWindowTitle(tr("wp_dialog_title_edit") if self._is_edit else tr("wp_dialog_title_add"))
        self.setMinimumSize(520, 580)
        self._setup_ui()
        if self._is_edit:
            self._populate(cache)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        tabs = QTabWidget()

        # ── Fane 1: Grundlæggende ─────────────────────────────────────────────
        basic = QWidget()
        basic_layout = QFormLayout(basic)
        basic_layout.setSpacing(8)

        self._gc_code = QLineEdit()
        self._gc_code.setPlaceholderText(tr("wp_ph_gc_code"))
        if self._is_edit:
            self._gc_code.setReadOnly(True)
            self._gc_code.setStyleSheet("color: gray;")
        basic_layout.addRow(tr("wp_label_gc_code"), self._gc_code)

        self._name = QLineEdit()
        self._name.setPlaceholderText(tr("wp_ph_name"))
        basic_layout.addRow(tr("wp_label_name"), self._name)

        self._cache_type = QComboBox()
        self._cache_type.addItems(CACHE_TYPES)
        basic_layout.addRow(tr("wp_label_type"), self._cache_type)

        self._container = QComboBox()
        self._container.addItems(CONTAINER_SIZES)
        basic_layout.addRow(tr("wp_label_container"), self._container)

        # Koordinater
        coord_group = QGroupBox(tr("wp_label_coords"))
        coord_layout = QFormLayout(coord_group)

        self._lat = QDoubleSpinBox()
        self._lat.setRange(-90.0, 90.0)
        self._lat.setDecimals(6)
        self._lat.setSingleStep(0.0001)
        coord_layout.addRow(tr("wp_label_lat"), self._lat)

        self._lon = QDoubleSpinBox()
        self._lon.setRange(-180.0, 180.0)
        self._lon.setDecimals(6)
        self._lon.setSingleStep(0.0001)
        coord_layout.addRow(tr("wp_label_lon"), self._lon)

        basic_layout.addRow(coord_group)

        # D/T
        dt_layout = QHBoxLayout()
        self._difficulty = QDoubleSpinBox()
        self._difficulty.setRange(1.0, 5.0)
        self._difficulty.setSingleStep(0.5)
        self._difficulty.setDecimals(1)
        self._difficulty.setValue(1.5)
        dt_layout.addWidget(QLabel(tr("wp_label_difficulty")))
        dt_layout.addWidget(self._difficulty)
        dt_layout.addSpacing(16)

        self._terrain = QDoubleSpinBox()
        self._terrain.setRange(1.0, 5.0)
        self._terrain.setSingleStep(0.5)
        self._terrain.setDecimals(1)
        self._terrain.setValue(1.5)
        dt_layout.addWidget(QLabel(tr("wp_label_terrain")))
        dt_layout.addWidget(self._terrain)
        dt_layout.addStretch()
        basic_layout.addRow(tr("wp_label_dt"), dt_layout)

        tabs.addTab(basic, tr("wp_tab_basic"))

        # ── Fane 2: Detaljer ──────────────────────────────────────────────────
        details = QWidget()
        details_layout = QFormLayout(details)
        details_layout.setSpacing(8)

        self._placed_by = QLineEdit()
        self._placed_by.setPlaceholderText(tr("wp_ph_placed_by"))
        details_layout.addRow(tr("wp_label_placed_by"), self._placed_by)

        self._country = QLineEdit()
        self._country.setPlaceholderText(tr("wp_ph_country"))
        details_layout.addRow(tr("wp_label_country"), self._country)

        self._state = QLineEdit()
        self._state.setPlaceholderText(tr("wp_ph_state"))
        details_layout.addRow(tr("wp_label_state"), self._state)

        self._short_desc = QTextEdit()
        self._short_desc.setMaximumHeight(80)
        self._short_desc.setPlaceholderText(tr("wp_ph_short_desc"))
        details_layout.addRow(tr("wp_label_short_desc"), self._short_desc)

        self._long_desc = QTextEdit()
        self._long_desc.setMaximumHeight(120)
        self._long_desc.setPlaceholderText(tr("wp_ph_long_desc"))
        details_layout.addRow(tr("wp_label_long_desc"), self._long_desc)

        self._hints = QLineEdit()
        self._hints.setPlaceholderText(tr("wp_ph_hint"))
        details_layout.addRow(tr("wp_label_hint"), self._hints)

        tabs.addTab(details, tr("wp_tab_details"))

        # ── Fane 3: Status ────────────────────────────────────────────────────
        status = QWidget()
        status_layout = QFormLayout(status)
        status_layout.setSpacing(8)

        self._available = QCheckBox(tr("wp_cb_available"))
        self._available.setChecked(True)
        status_layout.addRow(tr("wp_label_status"), self._available)

        self._archived = QCheckBox(tr("wp_cb_archived"))
        status_layout.addRow("", self._archived)

        self._premium = QCheckBox(tr("wp_cb_premium"))
        status_layout.addRow("", self._premium)

        self._found = QCheckBox(tr("wp_cb_found"))
        status_layout.addRow(tr("wp_label_personal"), self._found)

        self._dnf = QCheckBox(tr("wp_cb_dnf"))
        status_layout.addRow("", self._dnf)

        self._favorite = QCheckBox(tr("wp_cb_favorite"))
        status_layout.addRow("", self._favorite)

        tabs.addTab(status, tr("wp_tab_status"))

        layout.addWidget(tabs)

        # ── Knapper ───────────────────────────────────────────────────────────
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.button(QDialogButtonBox.StandardButton.Save).setText(tr("save"))
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText(tr("cancel"))
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _populate(self, cache: Cache) -> None:
        """Udfyld felterne med data fra en eksisterende cache."""
        self._gc_code.setText(cache.gc_code or "")
        self._name.setText(cache.name or "")

        idx = self._cache_type.findText(cache.cache_type or "")
        if idx >= 0:
            self._cache_type.setCurrentIndex(idx)

        idx = self._container.findText(cache.container or "")
        if idx >= 0:
            self._container.setCurrentIndex(idx)

        if cache.latitude:
            self._lat.setValue(cache.latitude)
        if cache.longitude:
            self._lon.setValue(cache.longitude)
        if cache.difficulty:
            self._difficulty.setValue(cache.difficulty)
        if cache.terrain:
            self._terrain.setValue(cache.terrain)

        self._placed_by.setText(cache.placed_by or "")
        self._country.setText(cache.country or "")
        self._state.setText(cache.state or "")
        self._short_desc.setPlainText(cache.short_description or "")
        self._long_desc.setPlainText(cache.long_description or "")
        self._hints.setText(cache.encoded_hints or "")

        self._available.setChecked(cache.available if cache.available is not None else True)
        self._archived.setChecked(cache.archived if cache.archived is not None else False)
        self._premium.setChecked(cache.premium_only if cache.premium_only is not None else False)
        self._found.setChecked(cache.found if cache.found is not None else False)
        self._dnf.setChecked(cache.dnf if cache.dnf is not None else False)
        self._favorite.setChecked(cache.favorite_point if cache.favorite_point is not None else False)

    def _validate_and_accept(self) -> None:
        """Validér og gem."""
        gc_code = self._gc_code.text().strip().upper()
        name = self._name.text().strip()

        if not gc_code:
            QMessageBox.warning(self, tr("warning"), tr("wp_val_gc_required"))
            return
        if not gc_code.startswith("GC"):
            QMessageBox.warning(self, tr("warning"), tr("wp_val_gc_invalid"))
            return
        if not name:
            QMessageBox.warning(self, tr("warning"), tr("wp_val_name_required"))
            return

        self.accept()

    def get_data(self) -> dict:
        """Returner formulardata som dict klar til at oprette/opdatere en Cache."""
        return {
            "gc_code":           self._gc_code.text().strip().upper(),
            "name":              self._name.text().strip(),
            "cache_type":        self._cache_type.currentText(),
            "container":         self._container.currentText(),
            "latitude":          self._lat.value(),
            "longitude":         self._lon.value(),
            "difficulty":        self._difficulty.value(),
            "terrain":           self._terrain.value(),
            "placed_by":         self._placed_by.text().strip() or None,
            "country":           self._country.text().strip() or None,
            "state":             self._state.text().strip() or None,
            "short_description": self._short_desc.toPlainText().strip() or None,
            "long_description":  self._long_desc.toPlainText().strip() or None,
            "encoded_hints":     self._hints.text().strip() or None,
            "available":         self._available.isChecked(),
            "archived":          self._archived.isChecked(),
            "premium_only":      self._premium.isChecked(),
            "found":             self._found.isChecked(),
            "dnf":               self._dnf.isChecked(),
            "favorite_point":    self._favorite.isChecked(),
        }
