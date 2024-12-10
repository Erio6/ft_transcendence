import {createCamera} from "../Components/camera.js";
import {createCube} from "../Components/cube.js";
import {createScene} from "../Components/scene.js";
import {createLights} from "../Components/lights.js";
import {createRenderer} from "../Systems/renderer.js";
import {Resizer} from "../Systems/Resizer.js";
import {Loop} from "../Systems/Loop.js";
import {Paddle} from "../Systems/Paddle.js"
import {createControls} from "../Systems/controls.js";
import {Ball} from "../Systems/Ball.js";

let camera, renderer, scene, loop;

class World {
    constructor(container) {
        let lastPart = window.location.toString().split("/");
        lastPart = lastPart.pop() || lastPart.pop();
        lastPart = 256;
        const webSocket = new WebSocket("ws://localhost:8000/ws/game/" + lastPart + "/");

        webSocket.onopen = (event) => {
            console.log("WebSocket connection established.");
        };

        webSocket.onclose = (event) => {
            console.warn("WebSocket connection closed:", event);
            // Optionally attempt reconnection
        };

        webSocket.onerror = (error) => {
            console.error("WebSocket error:", error);
        };

        webSocket.onmessage = (event) => {
            const json = JSON.parse(event.data);
            console.log(json);
            if (json['type'] === 'init_ball') {
                this.ball = new Ball(json['x'], json['y'], json['v_x'], json['v_y'], json['speed'], json['radius'], 50, 50);
                loop.updatables.push(this.ball);
                scene.add(this.ball.model);
            }
            else if (json['type'] === 'ball')
                this.ball.collide(json['x'], json['y'], json['v_x'], json['v_y'], json['speed']);
            else if (json['type'] === 'score') {
                this.ball.collide(json['x'], json['y'], json['v_x'], json['v_y'], json['speed']);
            }
        }


        camera = createCamera();
        scene = createScene();
        renderer = createRenderer();

        const controls = createControls(camera, renderer.domElement);

        const top = createCube();
        const bot = createCube();
        // const paddleLeft = createCube();
        const paddleLeft = new Paddle("left", 20, 3.5, 25, true, 2, 50, 50);
        const paddleRight = new Paddle("right", 20, 3.5, 25, false, 2, 50, 50);
        // const ball = new Ball(50, 50, 0, 1, 10, 1, 19);
        const {ambientLight, light} = createLights();

        loop = new Loop(camera, scene, renderer);
        container.append(renderer.domElement);

        top.position.set(0, 50, 0);
        top.scale.set(50, 1, 1);
        bot.position.set(0, -50, 0);
        bot.scale.set(50, 1, 1);


        // paddleLeft.position.set(-20, 0, 0);
        //paddleRight.position.set(50, 0, 0);
        // paddleLeft.scale.set(1, 5, 1);
        //paddleRight.scale.set(1, 5, 1);

        loop.updatables.push(controls);
        loop.updatables.push(paddleLeft);
        // loop.updatables.push(ball);
        // loop.updatables.push(cube);

        scene.add(top, bot, paddleLeft.model, paddleRight.model, light, ambientLight);

        this.canvas = renderer.domElement;

        const resizer = new Resizer(container, camera, renderer);
    }

    render() {
        renderer.render(scene, camera);
    }

    start() {
        loop.start();
    }

    stop() {
        loop.stop();
    }
}

export {World};