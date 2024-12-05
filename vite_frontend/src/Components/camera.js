import {PerspectiveCamera} from "three";

function createCamera() {
    const camera = new PerspectiveCamera(
        30,
        1,
        0.01,
        200,
    );

    camera.position.set(0, 0, 100);
    return camera;
}

export {createCamera};