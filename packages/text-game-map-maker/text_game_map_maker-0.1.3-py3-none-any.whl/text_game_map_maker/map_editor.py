import os
import json
import zlib
import traceback

from PyQt5 import QtWidgets, QtCore, QtGui

from text_game_map_maker import forms, scrollarea, tgmdata
from text_game_map_maker.door_editor import DoorEditor
from text_game_map_maker import tile_button
from text_game_map_maker.qt_auto_form import QtAutoForm

from text_game_maker.tile import tile
from text_game_maker.player import player


NUM_BUTTON_ROWS = 50
NUM_BUTTON_COLUMNS = 50

DEFAULT_WINDOW_WIDTH = 500
DEFAULT_WINDOW_HEIGHT = 400

NUM_BUTTONS_PER_SCREEN_HEIGHT = 6.0

BUTTON_ZOOM_INCREMENT = 14
FONT_ZOOM_INCREMENT = 1.0

DEFAULT_BUTTON_SIZE = 180
DEFAULT_FONT_SIZE = 14.0

MIN_BUTTON_SIZE = 40
MIN_FONT_SIZE = 4

MAX_BUTTON_SIZE = 400
MAX_FONT_SIZE = 30

SCROLL_UNITS_PER_CLICK = 120

MAP_BUILDER_SAVE_FILE_SUFFIX = "tgmdata"

_tiles = {}

_move_map = {
    'north': (-1, 0),
    'south': (1, 0),
    'east': (0, 1),
    'west': (0, -1)
}


class ZoomLevel(object):
    button_size = DEFAULT_BUTTON_SIZE
    font_size = DEFAULT_FONT_SIZE

def getTilePositions(start_tile):
    positions = {}
    seen = []
    pos = (0, 0)
    tilestack = [(start_tile, None, None)]

    while tilestack:
        curr, newpos, movedir = tilestack.pop(0)
        if newpos is not None:
            pos = newpos

        if curr in seen:
            continue

        seen.append(curr)

        if movedir is not None:
            xinc, yinc = _move_map[movedir]
            oldx, oldy = pos
            newx, newy = oldx + xinc, oldy + yinc
            pos = (newx, newy)

        if curr.is_door():
            curr = curr.replacement_tile

        positions[curr.tile_id] = pos

        for direction in _move_map:
            n = getattr(curr, direction)
            if n:
                tilestack.append((n, pos, direction))

    return positions

# Set checkbox state without triggering the stateChanged signal
def _silent_checkbox_set(checkbox, value, handler):
    checkbox.stateChanged.disconnect(handler)
    checkbox.setChecked(value)
    checkbox.stateChanged.connect(handler)

class MapEditor(QtWidgets.QDialog):
    def __init__(self, primaryScreen, mainWindow):
        super(MapEditor, self).__init__()

        self.main = mainWindow
        self.primary_screen = primaryScreen
        self.loaded_file = None
        self.save_enabled = True

        screensize = self.primary_screen.size()
        self.screen_width = screensize.width()
        self.screen_height = screensize.height()

        self.resize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.gridAreaLayout = QtWidgets.QHBoxLayout()
        self.buttonAreaLayout = QtWidgets.QHBoxLayout()
        self.buildToolbar()

        # Build scrollable grid area
        self.scrollArea = scrollarea.ScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scroll_offset = 0

        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setHorizontalSpacing(2)
        self.gridLayout.setVerticalSpacing(2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridAreaLayout.addWidget(self.scrollArea)

        self.font = QtGui.QFont()
        self.font.setPointSize(ZoomLevel.font_size)
        self.font.setFamily("Arial")

        self.mainLayout.addLayout(self.buttonAreaLayout)
        self.mainLayout.addLayout(self.gridAreaLayout)
        self.selectedPosition = None
        self.startTilePosition = None

        self.rows = NUM_BUTTON_ROWS
        self.columns = NUM_BUTTON_COLUMNS

        for i in range(self.rows):
            for j in range(self.columns):
                btn = tile_button.TileButton(self)

                btn.setFont(self.font)
                btn.setAttribute(QtCore.Qt.WA_StyledBackground)
                btn.setFixedSize(ZoomLevel.button_size, ZoomLevel.button_size)
                btn.calculate_dimensions()
                btn.installEventFilter(btn)
                self.gridLayout.addWidget(btn, i, j)

        # Enable mouse tracking on scrollarea and all children
        self.scrollArea.setMouseTracking(True)

        # Set up shortcuts for arrow keys
        QtWidgets.QShortcut(QtGui.QKeySequence("right"), self, self.rightKeyPress)
        QtWidgets.QShortcut(QtGui.QKeySequence("left"), self, self.leftKeyPress)
        QtWidgets.QShortcut(QtGui.QKeySequence("up"), self, self.upKeyPress)
        QtWidgets.QShortcut(QtGui.QKeySequence("down"), self, self.downKeyPress)\

    def moveSelection(self, y_move, x_move):
        if self.selectedPosition is None:
            return

        y, x = self.selectedPosition
        newpos = (y + y_move, x + x_move)

        if ((newpos[0] < 0) or (newpos[0] >= self.columns) or
            (newpos[1] < 0) or (newpos[1] >= self.rows)):
            return

        button = self.buttonAtPosition(*newpos)
        self.setSelectedPosition(button)

    def leftKeyPress(self):
        self.moveSelection(*_move_map['west'])

    def rightKeyPress(self):
        self.moveSelection(*_move_map['east'])

    def upKeyPress(self):
        self.moveSelection(*_move_map['north'])

    def downKeyPress(self):
        self.moveSelection(*_move_map['south'])

    def buildToolbar(self):
        self.deleteButton = QtWidgets.QPushButton()
        self.clearButton = QtWidgets.QPushButton()
        self.doorButton = QtWidgets.QPushButton()
        self.wallButton = QtWidgets.QPushButton()
        self.saveButton = QtWidgets.QPushButton()
        self.loadButton = QtWidgets.QPushButton()
        self.loadFromSavedGameButton = QtWidgets.QPushButton()

        self.deleteButton.setText("Delete tile")
        self.clearButton.setText("Clear all tiles")
        self.doorButton.setText("Edit doors")
        self.wallButton.setText("Edit walls")
        self.saveButton.setText("Save to file")
        self.loadButton.setText("Load from file")
        self.loadFromSavedGameButton.setText("Load map from saved game")

        self.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.clearButton.clicked.connect(self.clearButtonClicked)
        self.doorButton.clicked.connect(self.doorButtonClicked)
        self.wallButton.clicked.connect(self.wallButtonClicked)
        self.saveButton.clicked.connect(self.saveButtonClicked)
        self.loadButton.clicked.connect(self.loadButtonClicked)
        self.loadFromSavedGameButton.clicked.connect(self.loadFromSavedGameButtonClicked)

        self.startTileCheckBox = QtWidgets.QCheckBox()
        self.startTileCheckBox.setStyleSheet("margin-left:50%; margin-right:50%;")
        self.startTileCheckBox.setChecked(False)
        self.startTileCheckBox.setEnabled(False)
        self.startTileCheckBox.stateChanged.connect(self.setStartTile)

        label = QtWidgets.QLabel("Start tile")
        label.setAlignment(QtCore.Qt.AlignCenter)
        checkBoxLayout = QtWidgets.QVBoxLayout()
        checkBoxLayout.addWidget(label)
        checkBoxLayout.addWidget(self.startTileCheckBox)
        checkBoxLayout.setAlignment(QtCore.Qt.AlignCenter)

        self.doorButton.setEnabled(False)
        self.wallButton.setEnabled(False)
        self.clearButton.setEnabled(False)
        self.deleteButton.setEnabled(False)

        tileButtonLayout = QtWidgets.QHBoxLayout()
        tileButtonLayout.addWidget(self.deleteButton)
        tileButtonLayout.addWidget(self.clearButton)
        tileButtonLayout.addWidget(self.doorButton)
        tileButtonLayout.addWidget(self.wallButton)
        tileButtonLayout.addLayout(checkBoxLayout)
        tileButtonGroup = QtWidgets.QGroupBox("Edit selected tile")
        tileButtonGroup.setAlignment(QtCore.Qt.AlignCenter)
        tileButtonGroup.setLayout(tileButtonLayout)

        fileButtonLayout = QtWidgets.QHBoxLayout()
        fileButtonLayout.addWidget(self.saveButton)
        fileButtonLayout.addWidget(self.loadButton)
        fileButtonLayout.addWidget(self.loadFromSavedGameButton)
        fileButtonGroup = QtWidgets.QGroupBox("Load/save file")
        fileButtonGroup.setAlignment(QtCore.Qt.AlignCenter)
        fileButtonGroup.setLayout(fileButtonLayout)

        compass = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap(self.main.compassPath,"1")
        pixmap = pixmap.scaled(128, 128)
        compass.setPixmap(pixmap)
        compassLayout = QtWidgets.QHBoxLayout()
        compassLayout.addWidget(compass)
        compassGroup = QtWidgets.QGroupBox()
        compassGroup.setLayout(compassLayout)
        compassGroup.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        self.buttonAreaLayout.addWidget(compassGroup)
        self.buttonAreaLayout.addWidget(tileButtonGroup)
        self.buttonAreaLayout.addWidget(fileButtonGroup)

    def warningBeforeQuit(self):
        return self.yesNoDialog("Are you sure?", "Are you sure you want to quit?"
                                " You will lose any unsaved data.")

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            if self.warningBeforeQuit():
                QtWidgets.qApp.quit()

    def setSaveEnabled(self, value):
        if value == self.save_enabled:
            return

        self.saveButton.setEnabled(value)
        self.main.saveAction.setEnabled(value)
        self.save_enabled = value

    def wheelEvent(self, event):
        self.scroll_offset += event.angleDelta().y()

        if -SCROLL_UNITS_PER_CLICK < self.scroll_offset < SCROLL_UNITS_PER_CLICK:
            return

        num_clicks = self.scroll_offset / SCROLL_UNITS_PER_CLICK
        self.scroll_offset %= SCROLL_UNITS_PER_CLICK

        if num_clicks > 0:
            self.increaseZoomLevel(False, num_clicks)
        else:
            self.decreaseZoomLevel(False, abs(num_clicks))

    def resizeGridView(self, button_size, font_size):
        for y in range(self.rows):
            for x in range(self.columns):
                btn = self.buttonAtPosition(y, x)

                self.font.setPointSize(font_size)
                btn.setFont(self.font)
                btn.setFixedSize(button_size, button_size)
                btn.calculate_dimensions()

                if (y, x) in _tiles:
                    btn.redrawDoors()

    def setDefaultZoomLevel(self):
        ZoomLevel.button_size = DEFAULT_BUTTON_SIZE
        ZoomLevel.font_size = DEFAULT_FONT_SIZE
        self.resizeGridView(ZoomLevel.button_size, ZoomLevel.font_size)

    def increaseZoomLevel(self, _, num=1):
        moved = 0
        while ((num > 0) and (ZoomLevel.button_size < MAX_BUTTON_SIZE) and
               (ZoomLevel.font_size < MAX_FONT_SIZE)):
            ZoomLevel.button_size += BUTTON_ZOOM_INCREMENT
            ZoomLevel.font_size += FONT_ZOOM_INCREMENT
            moved += 1
            num -= 1

        if moved == 0:
            return

        self.resizeGridView(ZoomLevel.button_size, ZoomLevel.font_size)

    def decreaseZoomLevel(self, _, num=1):
        moved = 0
        while((num > 0) and (ZoomLevel.button_size > MIN_BUTTON_SIZE) and
              (ZoomLevel.font_size > MIN_FONT_SIZE)):
            ZoomLevel.button_size -= BUTTON_ZOOM_INCREMENT
            ZoomLevel.font_size -= FONT_ZOOM_INCREMENT
            moved += 1
            num -= 1

        if moved == 0:
            return

        self.resizeGridView(ZoomLevel.button_size, ZoomLevel.font_size)

    def clearAllTiles(self):
        for pos in list(_tiles.keys()):
            button = self.buttonAtPosition(*pos)
            button.setText("")
            button.clearDoors()
            del _tiles[pos]
            button.setStyle(selected=False, start=False)

        self.startTilePosition = None
        self.setSelectedPosition(self.buttonAtPosition(0, 0))

    def yesNoDialog(self, header="", msg="Are you sure?"):
        reply = QtWidgets.QMessageBox.question(self, header, msg,
                                               (QtWidgets.QMessageBox.Yes |
                                               QtWidgets.QMessageBox.No |
                                               QtWidgets.QMessageBox.Cancel),
                                               QtWidgets.QMessageBox.Cancel)

        return reply == QtWidgets.QMessageBox.Yes

    def errorDialog(self, heading="Error", message="Unrecoverable error occurred"):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText(heading)
        msg.setInformativeText(message)
        msg.setWindowTitle("Critical error!")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def tile_id_in_map_data(self, tile_list, tile_id):
        for tiledata in tile_list:
            if tiledata["tile_id"] == tile_id:
                return True

        return False

    def serialize(self):
        return tgmdata.serialize(_tiles[self.startTilePosition], _tiles)

    def drawTileMap(self, start_tile, positions):
        for tile_id in positions:
            pos = tuple(positions[tile_id])
            tileobj = tile.get_tile_by_id(tile_id)
            if tileobj is None:
                continue

            _tiles[pos] = tileobj
            button = self.buttonAtPosition(*pos)
            button.setText(tileobj.tile_id)

            is_start = tileobj is start_tile
            button.setStyle(selected=False, start=is_start)
            button.redrawDoors()

    def deserialize(self, attrs):
        start_tile = tgmdata.deserialize(attrs)
        self.clearAllTiles()
        self.drawTileMap(start_tile, attrs['positions'])
        self.startTilePosition = tuple(attrs['positions'][start_tile.tile_id])

    def deserializeFromSaveFile(self, attrs):
        if (player.TILES_KEY not in attrs) or (player.START_TILE_KEY not in attrs):
            return False

        # Remove items, people and events, we're not dealing with them here
        tilelist = attrs[player.TILES_KEY]
        for tiledata in tilelist:
            del tiledata[tile.ITEMS_KEY]
            del tiledata[tile.PEOPLE_KEY]
            del tiledata[tile.ENTER_EVENT_KEY]
            del tiledata[tile.EXIT_EVENT_KEY]

        # build tilemap from list of tile data
        start_tile_name = attrs[player.START_TILE_KEY]
        start_tile = tile.builder(tilelist, start_tile_name, obj_version)

        # find lowest index tile in tilemap
        positions = getTilePositions(start_tile)
        lowest_y = positions[start_tile.tile_id][0]
        lowest_x = positions[start_tile.tile_id][1]

        for tile_id in positions:
            pos = positions[tile_id]
            if (pos[0] < lowest_y):
                lowest_y = pos[0]

            if (pos[1] < lowest_x):
                lowest_x = pos[1]

        # Correct tile positions so lowest tile is (0, 0)
        for tile_id in positions:
            old = positions[tile_id]
            positions[tile_id] = (old[0] + abs(lowest_y), old[1] + abs(lowest_x))

        self.clearAllTiles()
        self.drawTileMap(start_tile, positions)
        self.startTilePosition = positions[start_tile.tile_id]

        return True

    def buttonAtPosition(self, y, x):
        item = self.gridLayout.itemAtPosition(y, x)
        if item is None:
            return None

        return item.widget()

    def closestTileToOrigin(self, tilemap):
        seen = []
        pos = (0, 0)
        lowest_tile = start_tile
        lowest_tile_pos = (0, 0)
        tilestack = [(start_tile, None, None)]

        while tilestack:
            curr, newpos, movedir = tilestack.pop(0)
            if newpos is not None:
                pos = newpos

            if curr in seen:
                continue

            seen.append(curr)

            if movedir is not None:
                xinc, yinc = _move_map[movedir]
                oldx, oldy = pos
                newx, newy = oldx + xinc, oldy + yinc
                pos = (newx, newy)

                lowestx, lowesty = lowest_tile_pos
                if (newx <= lowestx) and (newy <= lowesty):
                    lowest_tile_pos = pos
                    lowest_tile = curr

            for direction in _move_map:
                n = getattr(curr, direction)
                if n:
                    tilestack.append((n, pos, direction))

            return lowest_tile

    def setStartTile(self, state=None):
        if self.selectedPosition == self.startTilePosition:
            return

        if self.selectedPosition not in _tiles:
            return

        if self.startTilePosition is not None:
            # Set current start tile colour back to default
            old_start = self.buttonAtPosition(*self.startTilePosition)
            old_start.setStyle(selected=False, start=False)

        if not self.startTileCheckBox.isChecked():
            self.startTileCheckBox.stateChanged.disconnect(self.setStartTile)
            self.startTileCheckBox.setChecked(True)
            self.startTileCheckBox.stateChanged.connect(self.setStartTile)

        new_start = self.buttonAtPosition(*self.selectedPosition)
        new_start.setStyle(selected=True, start=True)
        self.startTilePosition = self.selectedPosition
        self.startTileCheckBox.setEnabled(False)
        self.setSaveEnabled(True)

    def tileIDExists(self, tile_id):
        val = tile.get_tile_by_id(tile_id)
        return val is not None

    def loadFromSavedGameButtonClicked(self):
        filedialog = QtWidgets.QFileDialog
        options = filedialog.Options()
        options |= filedialog.DontUseNativeDialog
        filename, _ = filedialog.getOpenFileName(self, "Select saved game file to load",
                             "", "All Files (*);;Text Files (*.txt)",
                                                 options=options)

        if filename.strip() == '':
            return

        if not os.path.exists(filename):
            self.errorDialog("Can't find file", "There doesn't seem to be a "
                             "file called '%s'" % filename)

        try:
            with open(filename, 'rb') as fh:
                data = fh.read()
                strdata = zlib.decompress(data).decode("utf-8")
                attrs = json.loads(strdata)
        except Exception as e:
            self.errorDialog("Error loading saved game state",
                             "Unable to load saved game data from file %s: %s"
                             % (filename, str(e)))
            return

        self.deserializeFromSaveFile(attrs)

    def deleteButtonClicked(self):
        if self.selectedPosition not in _tiles:
            self.errorDialog("Unable to delete tile", "No tile in this space "
                             "to delete")
            return

        tileobj = _tiles[self.selectedPosition]
        button = self.buttonAtPosition(*self.selectedPosition)

        reply = self.yesNoDialog("Are you sure?", "Are you sure you want to "
                                "delete this tile (tile ID is '%s')" % (tileobj.tile_id))
        if not reply:
            return

        self.disconnectSurroundingTiles(tileobj, *self.selectedPosition)
        del _tiles[self.selectedPosition]
        button.setText("")

        if self.startTilePosition == self.selectedPosition:
            self.startTilePosition = None

        button.setStyle(selected=False, start=False)
        button.redrawDoors()

        # Did we delete the last tile?
        if _tiles:
            # If not, enable saving to file (if it was disabled)
            self.setSaveEnabled(True)
        else:
            # If yes, disable button for clearing all tiles
            self.clearButton.setEnabled(False)
            self.setSelectedPosition(button)

    def clearButtonClicked(self):
        reply = self.yesNoDialog("Really clear all tiles?", "Are you sure you "
                                 "want to clear all tiles? you will lose any unsaved data.")

        if not reply:
            return

        self.clearAllTiles()
        self.clearButton.setEnabled(False)

    def doorButtonClicked(self):
        tileobj = _tiles[self.selectedPosition]
        button = self.buttonAtPosition(*self.selectedPosition)

        doors_dialog = DoorEditor(self, tileobj)
        doors_dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        doors_dialog.exec_()

    def wallButtonClicked(self):
        tileobj = _tiles[self.selectedPosition]
        button = self.buttonAtPosition(*self.selectedPosition)

        settings = forms.WallSettings()

        # Populate form with existing wall configuration for selected tile
        for direction in ['north', 'south', 'east', 'west']:
            adj = getattr(tileobj, direction)
            val = True if (adj is None) or adj.is_door() else False
            setattr(settings, direction, val)

        # Display form
        dialog = QtAutoForm(settings, title="Edit walls",
                            formTitle="Select directions to be blocked by walls",
                            spec=settings.spec)

        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.setWindowIcon(QtGui.QIcon(self.main.iconPath))
        dialog.exec_()

        if not dialog.wasAccepted():
            # Dialog was cancelled or closed
            return None

        # Apply form settings to selected tile
        for direction in ['north', 'south', 'east', 'west']:
            adj = getattr(tileobj, direction)
            had_wall = True if (adj is None) or adj.is_door() else False
            has_wall = getattr(settings, direction)

            # No change, we're done with this iteration
            if had_wall == has_wall:
                continue

            if has_wall:
                # Adding a wall
                setattr(adj, tile.reverse_direction(direction), None)
                setattr(tileobj, direction, None)
            else:
                # Removing a wall
                oldy, oldx = self.selectedPosition
                deltay, deltax = _move_map[direction]
                newy, newx = oldy + deltay, oldx + deltax

                # Adjacent tile is off the grid, we're done with this iteration
                if ((newy < 0) or (newy >= self.rows) or
                    (newx < 0) or (newx >= self.columns)):
                    continue

                adj_tile = self.tileAtPosition(newy, newx)
                if adj_tile is None:
                    # No tile here, we're done with this iteration
                    continue

                setattr(adj_tile, tile.reverse_direction(direction), tileobj)
                setattr(tileobj, direction, adj_tile)

        button.update()
        self.redrawSurroundingTiles(*self.selectedPosition)

    def saveFileDialog(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        dialog.setDefaultSuffix(MAP_BUILDER_SAVE_FILE_SUFFIX)
        dialog.setNameFilter("Text Game Map Data Files (*.%s)"
                             % MAP_BUILDER_SAVE_FILE_SUFFIX)

        if dialog.exec_():
            filenames = dialog.selectedFiles()
            if len(filenames) != 1:
                return None

            return filenames[0]

        return None

    def saveButtonClicked(self):
        if self.loaded_file is None:
            self.saveAsButtonClicked()
        else:
            self.saveToFile(self.loaded_file)

    def saveAsButtonClicked(self):
        if self.startTilePosition is None:
            self.errorDialog("Unable to save map", "No start tile is set. You "
                             "must set a start tile before saving.")
            return

        filename = self.saveFileDialog()
        # Cancelled, or empty string?
        if (filename == None) or (filename.strip() == ""):
            return

        self.saveToFile(filename)

    def saveToFile(self, filename):
        try:
            string_data = json.dumps(self.serialize())
            compressed = zlib.compress(bytes(string_data, encoding="utf8"))

            with open(filename, 'wb') as fh:
                fh.write(compressed)
        except Exception:
            self.errorDialog("Error saving map data",
                             "Unable to save map data to file %s:\n\n%s"
                             % (filename, traceback.format_exc()))

        self.setSaveEnabled(False)

    def loadFromFile(self, filename):
        if not os.path.exists(filename):
            self.errorDialog("Can't find file", "There doesn't seem to be a "
                             "file called '%s'" % filename)
            return

        try:
            with open(filename, 'rb') as fh:
                strdata = fh.read()

            decompressed = zlib.decompress(strdata).decode("utf-8")
            attrs = json.loads(decompressed)
            self.deserialize(attrs)
        except Exception:
            self.errorDialog("Error loading saved map data",
                             "Unable to load saved map data from file %s:\n\n%s"
                             % (filename, traceback.format_exc()))

        self.loaded_file = filename
        if _tiles:
            self.clearButton.setEnabled(True)

        self.setSaveEnabled(False)

    def loadButtonClicked(self):
        filedialog = QtWidgets.QFileDialog
        options = filedialog.Options()
        options |= filedialog.DontUseNativeDialog
        filename, _ = filedialog.getOpenFileName(self, "Select file to open",
                             "", "All Files (*);;Text Files (*.txt)",
                                                 options=options)

        if filename.strip() == '':
            return

        self.loadFromFile(filename)

    def getButtonPosition(self, button):
        idx = self.gridLayout.indexOf(button)
        return self.gridLayout.getItemPosition(idx)[:2]

    def tileAtPosition(self, y, x):
        pos = (y, x)
        if pos not in _tiles:
            return None

        return _tiles[pos]

    def surroundingTilePositions(self, y, x):
        def _fetch_tile(y, x, yoff, xoff):
            oldy, oldx = y, x
            newy = oldy + yoff
            newx = oldx + xoff

            if newy < 0: return None
            if newx < 0: return None

            newpos = (newy, newx)
            if newpos not in _tiles:
                return None

            return newpos

        north = _fetch_tile(y, x, -1, 0)
        south = _fetch_tile(y, x, 1, 0)
        east = _fetch_tile(y, x, 0, 1)
        west = _fetch_tile(y, x, 0, -1)

        return north, south, east, west

    def setSelectedPosition(self, button):
        if self.selectedPosition is not None:
            oldstart = self.selectedPosition == self.startTilePosition
            oldbutton = self.buttonAtPosition(*self.selectedPosition)
            oldbutton.setStyle(selected=False, start=oldstart)

        self.selectedPosition = self.getButtonPosition(button)

        newstart = self.selectedPosition == self.startTilePosition
        newfilled = self.selectedPosition in _tiles
        button.setStyle(selected=True, start=newstart)

        filled = self.selectedPosition in _tiles

        if self.selectedPosition == self.startTilePosition:
            _silent_checkbox_set(self.startTileCheckBox, True, self.setStartTile)
            self.startTileCheckBox.setEnabled(False)
        elif filled:
            self.startTileCheckBox.setEnabled(True)
            _silent_checkbox_set(self.startTileCheckBox, False, self.setStartTile)
        else:
            _silent_checkbox_set(self.startTileCheckBox, False, self.setStartTile)
            self.startTileCheckBox.setEnabled(False)

        for obj in [self.doorButton, self.deleteButton, self.wallButton,
                    self.main.editDoorsAction, self.main.editWallsAction,
                    self.main.deleteTileAction]:
            if obj.isEnabled() != filled:
                obj.setEnabled(filled)

        button.setFocus(True)
        self.scrollArea.ensureWidgetVisible(button)

    def onMiddleClick(self, button):
        pass

    def onRightClick(self, button):
        self.setSelectedPosition(button)

    def runTileBuilderDialog(self, position):
        settings = forms.TileSettings()

        if position in _tiles:
            tileobj = _tiles[position]
            settings.description = tileobj.description
            settings.name = tileobj.name
            settings.tile_id = tileobj.tile_id
            settings.first_visit_message = tileobj.first_visit_message
            settings.first_visit_message_in_dark = tileobj.first_visit_message_in_dark
            settings.dark = tileobj.dark
            settings.smell_description = tileobj.smell_description
            settings.ground_smell_description = tileobj.ground_smell_description
            settings.ground_taste_description = tileobj.ground_taste_description
        else:
            tileobj = tile.Tile()
            settings.tile_id = "tile%d" % tile.Tile.tile_id

        complete = False
        while not complete:
            dialog = QtAutoForm(settings, title="Tile attributes",
                                formTitle="Set attributes of currently selected tile",
                                spec=settings.spec)

            dialog.setWindowModality(QtCore.Qt.ApplicationModal)
            dialog.setWindowIcon(QtGui.QIcon(self.main.iconPath))
            dialog.exec_()

            if not dialog.wasAccepted():
                return None

            if str(settings.tile_id).strip() == '':
                self.errorDialog("Invalid tile ID", "tile ID field cannot be empty")
            elif (tileobj.tile_id != settings.tile_id) and self.tileIDExists(settings.tile_id):
                self.errorDialog("Unable to create tile", "Tile ID '%s' already in use!"
                                 % settings.tile_id)
            else:
                complete = True

        if settings.tile_id != tileobj.tile_id:
            tileobj.set_tile_id(settings.tile_id)

        tileobj.description = settings.description
        tileobj.name = settings.name
        tileobj.first_visit_message = settings.first_visit_message
        tileobj.first_visit_message_in_dark = settings.first_visit_message_in_dark
        tileobj.dark = settings.dark
        tileobj.smell_description = settings.smell_description
        tileobj.ground_smell_description = settings.ground_smell_description
        tileobj.ground_taste_description = settings.ground_taste_description

        return tileobj

    def redrawSurroundingTiles(self, y, x):
        north, south, east, west = self.surroundingTilePositions(y, x)
        adjacent_tiles = {'north': north, 'south': south, 'east': east, 'west': west}

        for direction in adjacent_tiles:
            adjacent_tilepos = adjacent_tiles[direction]

            if not adjacent_tilepos:
                continue

            button = self.buttonAtPosition(*adjacent_tilepos)
            button.update()

    def disconnectSurroundingTiles(self, tileobj, y, x):
        north, south, east, west = self.surroundingTilePositions(y, x)
        adjacent_tiles = {'north': north, 'south': south, 'east': east, 'west': west}

        for direction in adjacent_tiles:
            adjacent_tilepos = adjacent_tiles[direction]

            if not adjacent_tilepos:
                continue

            adjacent_tileobj = self.tileAtPosition(*adjacent_tilepos)
            setattr(tileobj, direction, None)

            # re-draw the tile we just disconnected from
            button = self.buttonAtPosition(*adjacent_tilepos)
            button.update()

            reverse_direction = tile.reverse_direction(direction)
            reverse_pointer = getattr(adjacent_tileobj, reverse_direction)

            if reverse_pointer and reverse_pointer.is_door():
                reverse_pointer.replacement_tile = None
            else:
                setattr(adjacent_tileobj, tile.reverse_direction(direction), None)

    def connectSurroundingTiles(self, tileobj, y, x):
        north, south, east, west = self.surroundingTilePositions(y, x)
        adjacent_tiles = {'north': north, 'south': south, 'east': east, 'west': west}

        for direction in adjacent_tiles:
            adjacent_tilepos = adjacent_tiles[direction]

            if not adjacent_tilepos:
                continue

            adjacent_tileobj = self.tileAtPosition(*adjacent_tilepos)
            setattr(tileobj, direction, adjacent_tileobj)

            # re-draw the tile we just connected to
            button = self.buttonAtPosition(*adjacent_tilepos)
            button.update()

            reverse_direction = tile.reverse_direction(direction)
            reverse_pointer = getattr(adjacent_tileobj, reverse_direction)

            if reverse_pointer and reverse_pointer.is_door():
                reverse_pointer.replacement_tile = tileobj
            else:
                setattr(adjacent_tileobj, tile.reverse_direction(direction), tileobj)

    def editSelectedTile(self):
        if self.selectedPosition is None:
            return

        self.onLeftClick(self.buttonAtPosition(*self.selectedPosition))

    def onLeftClick(self, button):
        is_first_tile = (not _tiles)
        position = self.getButtonPosition(button)
        tileobj = self.runTileBuilderDialog(position)

        # Dialog was cancelled or otherwise failed, we're done
        if tileobj is None:
            self.setSelectedPosition(button)
            return

        if position not in _tiles:
            # Created a new tile
            _tiles[position] = tileobj
            button.setStyle(selected=True, start=False)
            self.connectSurroundingTiles(tileobj, *position)

        button.setText(str(tileobj.tile_id))
        self.setSelectedPosition(button)

        if is_first_tile:
            self.clearButton.setEnabled(True)

        self.setSaveEnabled(True)
