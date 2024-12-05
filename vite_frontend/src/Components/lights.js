import {DirectionalLight, AmbientLight, HemisphereLight} from "three";

function createLights() {
    const light = new DirectionalLight('white', 6);
    const ambientLight = new AmbientLight('white', 2);

    light.position.set(10, 10, 10);

    return {ambientLight, light};
}

export {createLights};