import QtQuick 1.1

Item {
    id: shadow

    function setText(text) {
        message.text = text
        notifyAni.running = true
    }

    function setWidth(width) {
        shadow.width = width
    }

    function setSize(width, height) {
        shadow.width = width
        shadow.height = height
        shadow.y = -shadow.height // Notification comes down from out of the screen.
    }

    SequentialAnimation {
        id: notifyAni

        PropertyAnimation {
            target: shadow
            property: "y"
            to: 0
            duration: 500
            easing.type: Easing.OutQuad
        }

        PropertyAnimation {
            target: message
            property: "opacity"
            from: 0
            to: 1
            duration: 500
            easing.type: Easing.OutQuad
        }

        PauseAnimation { duration: 1000 }

        PropertyAnimation {
            target: message
            property: "opacity"
            from: 1
            to: 0
            duration: 300
            easing.type: Easing.InQuad
        }

        PropertyAnimation {
            target: shadow
            property: "y"
            to: -150
            duration: 300
            easing.type: Easing.InQuad
        }
    }

    Rectangle {
        color: "#000000"
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0; color: "#000000" }
            GradientStop { position: 1; color: "transparent" }
        }
    }

    Text {
        id: message
        text: ""
        font.bold: true
        font.pixelSize: shadow.height / 3
        opacity: 0
        anchors.centerIn: shadow
        color: "#ffffff"
        smooth: true
    }

    // When mouse is clicked, cancel the animation and go back to the initial state.
    MouseArea {
        anchors.fill: parent
        onClicked: {
            notifyAni.running = false
            shadow.y = -shadow.height
            message.opacity = 0
        }
    }
}