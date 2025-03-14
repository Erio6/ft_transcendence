import {createCubeMat} from "../Components/cube.js";
import {MeshStandardMaterial} from "three";

class Ball {
    constructor(x, y, v_x, v_y, speed, radius, field_height, field_width) {
        this.x = x;
        this.y = 100 - y;
        this.v_x = v_x;
        this.v_y = v_y;
        this.speed = speed;
        this.radius = (radius / 100) * Math.max(field_width, field_height);
        this.field_height = field_height;
        this.field_width = field_width;
        const material = new MeshStandardMaterial({color: 0xaaaaaa, metalness: 1, roughness: 0.2});
        this.model = createCubeMat(material);
        this.model.scale.set(this.radius, this.radius, this.radius);
        this.model.position.set(this.x - 50, this.y - 50, 0);
    }

    collide(x, y, v_x, v_y, speed) {
        this.x = x;
        this.y = 100 - y;
        this.v_x = v_x;
        this.v_y = v_y;
        this.speed = parseInt(speed);
        console.log("collide " + v_x);
    }

    normalize(value, ratio) {
        value -= 50;
        // console.log(value);
        value /= 50;
        value *= ratio;
        return value;
    }

    wall_collide() {
        if (this.y >= 100 - this.radius) {
            this.y = 100 - this.radius;
            this.v_y *= -1;
        } else if (this.y <= this.radius) {
            this.y = this.radius;
            this.v_y *= -1;
        }
    }

    tick(delta) {
        this.x += this.v_x * delta * this.speed;
        this.y += -this.v_y * delta * this.speed;
        this.wall_collide();
        // console.log(this.normalize(this.x, this.field_width));
        this.model.position.set(this.x - 50, this.y - 50, 0);
    }
}

export {Ball};