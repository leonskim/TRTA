import QtQuick 1.1

Rectangle {
    id: container

    property string text: "Button"
    property bool is_clickable: true

    signal clicked

    width: buttonLabel.width + 20
    height: buttonLabel.height + 5
    smooth: true

    gradient: Gradient {
        GradientStop {
            position: 0.0
            color: {
                if (mouseArea.pressed)
                    return "#ff1010"
                else
                    return "#ff5151"
            }
        }
        GradientStop { 
            id: hover
            position: 1.0
            color: "#ff5151"
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        onEntered: { hover.color = "#c11515" }
        onExited: { hover.color = "#ff5151" }
        onClicked: {
            // Shouldn't send "clicked" signal when the button is
            // clicked while animation is being played.
            if (container.is_clickable)  
                container.clicked() 
        }
    }

    Text {
        id: buttonLabel
        anchors.centerIn: container
        color: "#FFFFFF"
        text: container.text
    }
}
