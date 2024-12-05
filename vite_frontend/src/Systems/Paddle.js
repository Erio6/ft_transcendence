import {createCube} from "../Components/cube.js";


class Paddle {
    constructor(location, speed, width, length, active) {
        this.location = location;
        this.active = active;
        this.speed = speed;
        this.width = width;
        this.length = length;
        if (location === "left")
            this.x = -20;
        else
            this.x = 20;
        this.y = 0;
        this.z = 0;
        this.model = createCube();
        this.model.position.set(this.x, this.y, this.z);
        this.model.scale.set(width, length, 1);
        this.pressUp = false;
        this.pressDown = false;

        if (active) {
            addEventListener("keydown", (event) => {
                if (event.code === "ArrowDown")
                    this.pressDown = true;
                else if (event.code === "ArrowUp")
                    this.pressUp = true;
                console.log(this.pressDown + " | " + this.pressUp);
            });
            addEventListener("keyup", (event) => {
                if (event.code === "ArrowDown")
                    this.pressDown = false;
                else if (event.code === "ArrowUp")
                    this.pressUp = false;
                console.log(this.pressDown + " | " + this.pressUp);
            });
        }
    }

    tick(delta) {
        if (this.pressUp)
            this.y += this.speed * delta;
        if (this.pressDown)
            this.y -= this.speed * delta;
        if (this.y > 19 - this.length)
            this.y = 19 - this.length
        else if (this.y < -19 + this.length)
            this.y = -19 + this.length
        this.model.position.set(this.x, this.y, this.z);
    }
}

export {Paddle};