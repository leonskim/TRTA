import QtQuick 1.1

Rectangle {
    id: container
    width: speaker.width
    height: speaker.height
    color: "transparent"
    smooth: true

    property bool isEnabled: true
    signal clicked (bool isEnabled)

    Image {
        id: speaker
        width: 23
        height: 23
        source: "../images/sound_on.png"
        opacity: 0.7
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        onEntered: { speaker.opacity = 1.0 }
        onExited: { speaker.opacity = 0.7 }
        onClicked: { 
            isEnabled = !(isEnabled)

            if (isEnabled)
                speaker.source = "../images/sound_on.png"
            else
                speaker.source = "../images/sound_off.png"

            container.clicked(container.isEnabled) 
        }
    }
}