import {createCube} from "../Components/cube.js";


class Paddle {
    constructor(location, speed, width, length, active, x, field_height, field_width) {
        this.location = location;
        this.active = active;
        this.speed = speed;
        this.width = width / 2;
        this.length = length / 2;
        this.field_height = field_height;
        this.field_width = field_width;
        if (location === "left")
            this.x = -50 + x;
        else
            this.x = 50 - x;
        this.y = 0;
        this.z = 0;
        this.model = createCube();
        this.model.position.set(this.x, this.y, this.z);
        this.model.scale.set(this.width, this.length, 1);
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
        if (this.y > this.field_height - 1 - this.length)
            this.y = this.field_height - 1 - this.length;
        else if (this.y < -this.field_height + 1 + this.length)
            this.y = -this.field_height + 1 + this.length;
        this.model.position.set(this.x, this.y, this.z);
    }
}

export {Paddle};