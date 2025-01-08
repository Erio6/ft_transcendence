import {createCube} from "../Components/cube.js";


class Paddle {
    constructor(location, name, speed, width, length, active, x, field_height, field_width, websocket) {
        this.location = location;
        this.name = name;
        this.active = active;
        this.speed = speed;
        console.log(this.speed, speed);
        this.width = width / 2;
        this.length = length / 2;
        this.field_height = field_height;
        this.field_width = field_width;
        this.websocket = websocket;
        this.score = 0;
        if (location === "left")
            this.x = -50 + x + this.width;
        else
            this.x = 50 - x - this.width;
        this.y = 0;
        this.z = 0;
        this.model = createCube();
        this.model.position.set(this.x, this.y, this.z);
        this.model.scale.set(this.width, this.length, 1);
        this.pressUp = false;
        this.pressDown = false;

        if (active) {
            addEventListener("keydown", (event) => {
                if (event.code === "ArrowDown") {
                    this.pressDown = true;
                    this.websocket.send(JSON.stringify({
                        "type": 'move',
                        "data": 1,
                        "value": true,
                        "loc": this.location
                    }))
                }
                else if (event.code === "ArrowUp") {
                    this.pressUp = true;
                    this.websocket.send(JSON.stringify({
                        "type": 'move',
                        "data": -1,
                        "value": true,
                        "loc": this.location
                    }))
                }
                console.log(this.pressDown + " | " + this.pressUp);
            });
            addEventListener("keyup", (event) => {
                if (event.code === "ArrowDown") {
                    this.pressDown = false;
                    console.log("send");
                    this.websocket.send(JSON.stringify({
                        "type": 'move',
                        "data": 1,
                        "value": false,
                        "loc": this.location
                    }))
                }
                else if (event.code === "ArrowUp") {
                    this.pressUp = false;
                    this.websocket.send(JSON.stringify({
                        "type": 'move',
                        "data": -1,
                        "value": false,
                        "loc": this.location
                    }))
                }
                console.log(this.pressDown + " | " + this.pressUp);
            });
        }
    }
    
    tick(delta) {
        if (this.pressUp)
            this.y += this.speed * delta;
        if (this.pressDown)
            this.y -= this.speed * delta;
        if (this.y > this.field_height - this.length)
            this.y = this.field_height - this.length;
        else if (this.y < -this.field_height + this.length)
            this.y = -this.field_height + this.length;
        if (this.active) {
            // console.log(this.speed, delta);
            // console.log(this.x, this.y, this.z);
        }
        this.model.position.set(this.x, this.y, this.z);
    }
}

export {Paddle};