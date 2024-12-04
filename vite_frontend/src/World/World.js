import {createCamera} from "../Components/camera.js";
import {createCube} from "../Components/cube.js";
import {createScene} from "../Components/scene.js";
import {createLights} from "../Components/lights.js";
import {createRenderer} from "../Systems/renderer.js";
import {Resizer} from "../Systems/Resizer.js";
import {Loop} from "../Systems/Loop.js";

let camera, renderer, scene, loop;

class World {
    constructor(container) {
        camera = createCamera();
        scene = createScene();
        renderer = createRenderer();
        loop = new Loop(camera, scene, renderer);
        container.append(renderer.domElement);

        const cube = createCube();
        const light = createLights();

        loop.updatables.push(cube);

        scene.add(cube, light);

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