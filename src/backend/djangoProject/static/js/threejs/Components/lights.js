import {DirectionalLight, AmbientLight, HemisphereLight} from "three";

function createLights() {
    const ambientLight = new AmbientLight('white', 2);
    const light = new DirectionalLight('white', 6);

    // light.position.set(10, 10, 10);
    light.position.set(50, 100, 75);

    return {ambientLight, light};
}

export {createLights};