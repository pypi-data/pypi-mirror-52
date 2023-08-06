import QtQuick 2.0
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import QtQuick.Window 2.10
import QtQuick.Dialogs 1.0

Item {
    id: mainWindowItem
    width: 300
    height: 175
    enabled: app.enabled

    ColumnLayout {
        id: columnLayout
        anchors.rightMargin: 5
        anchors.leftMargin: 5
        anchors.bottomMargin: 5
        anchors.topMargin: 5
        anchors.fill: parent

        RowLayout {
            id: devicesLayout
            height: 26
            anchors.leftMargin: 0

            Label {
                id: devicesLabel
                text: "Device"
                leftPadding: 9
            }

            ComboBox {
                id: devicesComboBox
                Layout.fillWidth: true
                enabled: app.devicesEnabled
                model: devicesShowAllCheckbox.checked
                       ? app.deviceAllItems.length > 0 ? app.deviceAllItems : [app.devicesMessage]
                : app.deviceItems.length > 0 ? app.deviceItems : [app.devicesMessage]
                Binding { target: app; property: "devicesIndex"; value: devicesComboBox.currentIndex }
            }

            CheckBox {
                id: devicesShowAllCheckbox
                text: qsTr("Show All")
                checked: app.devicesShowAll
                Binding { target: app; property: "devicesShowAll"; value: devicesShowAllCheckbox.checked }
            }
        }

        GroupBox {
            id: firmwareGroupBox
            height: 130
            transformOrigin: Item.Center
            topPadding: 24
            anchors.leftMargin: 0
            Layout.fillHeight: false
            Layout.fillWidth: true
            title: qsTr("Firmware")
            enabled: devicesComboBox.currentText != app.devicesMessage

            Column {
                id: column
                anchors.fill: parent
                spacing: 4

                RowLayout {
                    id: firmwareControllerModelLayout
                    y: 78
                    height: 31
                    anchors.left: parent.left
                    anchors.right: parent.right

                    Label {
                        id: firmwareControllerLabel
                        text: qsTr("Controller")
                    }

                    ComboBox {
                        id: firmwareControllerComboBox
                        Layout.fillWidth: true
                        model: app.firmwareControllers
                        enabled: firmwareControllerModelOverrideCheckbox.checked
                        currentIndex: app.firmwareControllersIndex
                        Binding { target: app; property: "firmwareController"; value: firmwareControllerComboBox.currentText }
                    }

                    Label {
                        id: firmwareModelLabel
                        text: qsTr("Model")
                    }

                    ComboBox {
                        id: firmwareModelComboBox
                        Layout.fillWidth: true
                        model: app.firmwareModels
                        enabled: firmwareControllerModelOverrideCheckbox.checked
                        currentIndex: app.firmwareModelsIndex
                        Binding { target: app; property: "firmwareModel"; value: firmwareModelComboBox.currentText }
                    }

                    CheckBox {
                        id: firmwareControllerModelOverrideCheckbox
                        text: qsTr("Override")
                        checked: app.firmwareOverride
                        Binding { target: app; property: "firmwareOverride"; value: firmwareControllerModelOverrideCheckbox.checked }
                    }
                }

                RowLayout {
                    id: firmwareVersionLayout
                    y: 31
                    height: 26
                    anchors.right: parent.right
                    anchors.left: parent.left

                    Label {
                        id: firmwareVersionLabel
                        text: qsTr("Version")
                        Layout.minimumWidth: firmwareControllerLabel.width
                    }

                    ComboBox {
                        id: firmwareVersionComboBox
                        Layout.fillWidth: true
                        model: app.firmwareVersions
                        enabled: !firmwareVersionLatestCheckbox.checked
                        Binding { target: app; property: "firmwareVersion"; value: firmwareVersionComboBox.currentText }
                    }

                    CheckBox {
                        id: firmwareVersionLatestCheckbox
                        text: qsTr("Latest")
                        Layout.minimumWidth: firmwareControllerModelOverrideCheckbox.width
                        checked: app.firmwareLatest
                        Binding { target: app; property: "firmwareLatest"; value: firmwareVersionLatestCheckbox.checked }
                        onClicked: {
                            if(firmwareVersionLatestCheckbox.checked) {
                                firmwareVersionComboBox.currentIndex = 0;
                            }
                        }
                    }
                }

                Text {
                    id: firmwareMessageText
                    text: app.firmwareMessage
                    font.bold: true
                    font.underline: false
                    font.italic: false
                    horizontalAlignment: Text.AlignLeft
                    anchors.left: parent.left
                    anchors.leftMargin: 0
                    anchors.right: parent.right
                    font.pixelSize: 9
                }

                RowLayout {
                    id: buttonLayout
                    anchors.right: parent.right

                    Button {
                        id: chooseFileButton
                        text: qsTr("Choose File...")
                        onClicked: firmwareOpenDialog.open()
                    }

                    Button {
                        id: firmwareUpdateButton
                        text: qsTr("Update")
                        topPadding: 4
                        onClicked: app.onUpdateClicked()
                    }

                }


            }

        }

        Item {
            id: item1
            width: 200
            height: 200
            Layout.fillHeight: true
            Layout.fillWidth: true
        }

    }

    FileDialog {
        id: firmwareOpenDialog
        title: "Please choose a firmware file"
        nameFilters: ["Firmware files (*.binary *.eeprom)"]
        onAccepted: app.onFirmwareOpenDialogAccepted(firmwareOpenDialog.fileUrls)
    }
}

/*##^## Designer {
    D{i:18;anchors_x:192;anchors_y:"-28"}D{i:7;anchors_width:265}
}
 ##^##*/
