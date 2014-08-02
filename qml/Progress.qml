import QtQuick 1.1

Rectangle {
	id: container

	width: 76
	height: 6
	color: "#00000000"

	property variant items: [p1, p2, p3, p4, p5, p6, p7, p8]
	
	function setProgress(progress) {
		for (var i = 0; i < items.length; i++) {
			if (i+1 <= progress)
				items[i].opacity = 0.8
			else
				items[i].opacity = 0.3		
		}
	}

	Rectangle {
        id: p1
        x: 0
        y: 0
        width: 6
        height: 6
        radius: 3
        color: "#ffffff"
        opacity: 0.3
	    Behavior on opacity { SmoothedAnimation { velocity: 0.5; } }
    }

    Rectangle {
        id: p2
        x: p1.x + 10
        y: p1.y
        width: p1.width
        height: p1.height
        radius: p1.radius
        color: p1.color
        opacity: 0.3
	    Behavior on opacity { SmoothedAnimation { velocity: 0.5; } }
    }

    Rectangle {
        id: p3
        x: p2.x + 10
        y: p1.y
        width: p1.width
        height: p1.height
        radius: p1.radius
        color: p1.color
        opacity: 0.3
	    Behavior on opacity { SmoothedAnimation { velocity: 0.5; } }
    }

    Rectangle {
        id: p4
        x: p3.x + 10
        y: p1.y
        width: p1.width
        height: p1.height
        radius: p1.radius
        color: p1.color
        opacity: 0.3
	    Behavior on opacity { SmoothedAnimation { velocity: 0.5; } }
    }

    Rectangle {
        id: p5
        x: p4.x + 10
        y: p1.y
        width: p1.width
        height: p1.height
        radius: p1.radius
        color: p1.color
        opacity: 0.3
	    Behavior on opacity { SmoothedAnimation { velocity: 0.5; } }
    }

    Rectangle {
        id: p6
        x: p5.x + 10
        y: p1.y
        width: p1.width
        height: p1.height
        radius: p1.radius
        color: p1.color
        opacity: 0.3
	    Behavior on opacity { SmoothedAnimation { velocity: 0.5; } }
    }

    Rectangle {
        id: p7
        x: p6.x + 10
        y: p1.y
        width: p1.width
        height: p1.height
        radius: p1.radius
        color: p1.color
        opacity: 0.3
	    Behavior on opacity { SmoothedAnimation { velocity: 0.5; } }
    }

    Rectangle {
        id: p8
        x: p7.x + 10
        y: p1.y
        width: p1.width
        height: p1.height
        radius: p1.radius
        color: p1.color
        opacity: 0.3
	    Behavior on opacity { SmoothedAnimation { velocity: 0.5; } }
    }

}