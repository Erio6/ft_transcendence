import {PerspectiveCamera} from "three";

function createCamera() {
    const camera = new PerspectiveCamera(
        30,
        1,
        0.01,
        1000,
    );

    camera.position.set(0, 0, 350);
    return camera;
}

export {createCamera};