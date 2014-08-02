import QtQuick 1.1

Rectangle {
    id: container
    width: 300
    height: 280
    color: "#600c01"

    signal gaugeAniFinished

    function setStartButtonText(text) {
        btn_start.text = text
    }

    function moveMeter(x) {
        gauge.x += x
    }

    function setPhase(now) {
        if (now == "w") { 
            phase.source = "../images/phase_work.png"
            gauge_ani(135, 1000)
        }
        else if (now == "b") { 
            phase.source = "../images/phase_break.png"
            gauge_ani(-100, 500)
        }
        else if (now == "l") { 
            phase.source = "../images/phase_long_break.png"
            gauge_ani(17, 700)
        }
        else { 
            phase.source = "../images/phase_ready.png"
            gauge_ani(-157, 1000)
        }

        phaseOpacityAni.running = true
    }

    function gauge_ani(position, duration) {
        gaugeAni.to = position
        gaugeAni.duration = duration
        gaugeAni.running = true
    }

    function button_opacity_ani(from, to, duration) {
        buttonOpacityAni.from = from
        buttonOpacityAni.to = to
        buttonOpacityAni.duration = duration
        buttonOpacityAni.running = true
    }

    PropertyAnimation {
        id: buttonOpacityAni
        targets: [btn_start, btn_reset]
        property: "opacity"
        from: 0.0
        to: 1.0
        duration: 500
        easing.type: Easing.OutQuad
    }

    PropertyAnimation {
        id: gaugeAni
        target: gauge
        property: "x"
        to: 0
        duration: 0
        easing.type: Easing.InOutCubic

        onRunningChanged: {
            if (gaugeAni.running) {
                
                // When the gauge animation is being played, block the mouse click events.
                btn_start.is_clickable = false
                btn_reset.is_clickable = false

                // Buttons' opacity is 0 when the application is just opened.
                if (btn_start.opacity != 0)
                    // Button Animation No.2 (When the gauge is moving)
                    button_opacity_ani(1.0, 0.6, 300) 

            } else {

                // When the gauge animation stopped, unblock the mouse click events.
                btn_start.is_clickable = true
                btn_reset.is_clickable = true

                if (btn_start.opacity == 0) { 
                    // Button Animation No.1 (When the Application is started)
                    button_opacity_ani(0.0, 1.0, 500) 
                } else {
                    // Button Animation No.3 (When the guage stops)
                    button_opacity_ani(0.6, 1.0, 300) 
                    // Emit signal to run timer
                    container.gaugeAniFinished()
                }

            }
        }
    }

    PropertyAnimation {
        id: phaseOpacityAni
        target: phase
        property: "opacity"
        from: 0.0
        to: 1.0
        duration: 2000
        easing.type: Easing.OutQuad
    }

    Image {
        id: gauge
        x: 218
        y: 132
        width: 317
        height: 72
        source: "../images/gauge.png"
        smooth: true

        Component.onCompleted: { 
            gauge_ani(-157, 2000)
        }
    }

    Image {
        id: phase
        x: 102
        y: 208
        width: 93
        height: 24
        source: "../images/phase_ready.png"
        smooth: true
    }

    Image {
        id: tomato
        x: 0
        y: 0
        width: 300
        height: 280
        source: "../images/tomato.png"
        smooth: true
    }

    Progress {
        id: progress
        objectName: "progress"
        x: 110
        y: 201
    }
    
    Button {
        id: btn_start
        objectName: "btn_start"
        x: 0
        y: 0
        width: 149
        height: 40
        text: "Start"
        opacity: 0.0
    }

    Button {
        id: btn_reset
        objectName: "btn_reset"
        x: 151
        y: 0
        width: 149
        height: 40
        text: "Reset"
        opacity: 0.0
    }
}
