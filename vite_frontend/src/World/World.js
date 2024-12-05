import {createCamera} from "../Components/camera.js";
import {createCube} from "../Components/cube.js";
import {createScene} from "../Components/scene.js";
import {createLights} from "../Components/lights.js";
import {createRenderer} from "../Systems/renderer.js";
import {Resizer} from "../Systems/Resizer.js";
import {Loop} from "../Systems/Loop.js";
import {Paddle} from "../Systems/Paddle.js"
import {createControls} from "../Systems/controls.js";

let camera, renderer, scene, loop;

class World {
    constructor(container) {
        camera = createCamera();
        scene = createScene();
        renderer = createRenderer();

        const controls = createControls(camera, renderer.domElement);

        const top = createCube();
        const bot = createCube();
        // const paddleLeft = createCube();
        const paddleLeft = new Paddle("left", 20, 1, 4, true);
        const paddleRight = createCube();
        const {ambientLight, light} = createLights();

        loop = new Loop(camera, scene, renderer);
        container.append(renderer.domElement);

        top.position.set(0, 20, 0);
        top.scale.set(20, 1, 1);
        bot.position.set(0, -20, 0);
        bot.scale.set(20, 1, 1);


        // paddleLeft.position.set(-20, 0, 0);
        paddleRight.position.set(20, 0, 0);
        // paddleLeft.scale.set(1, 5, 1);
        paddleRight.scale.set(1, 5, 1);

        loop.updatables.push(controls);
        loop.updatables.push(paddleLeft);
        // loop.updatables.push(cube);

        scene.add(top, bot, paddleLeft.model, paddleRight, light, ambientLight);

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