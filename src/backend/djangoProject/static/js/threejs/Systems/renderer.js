import {WebGLRenderer, PCFSoftShadowMap} from "three";

function createRenderer() {
    const renderer = new WebGLRenderer({antialias: true});
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = PCFSoftShadowMap;

    renderer.physicallyCorrectLights = true;

    return renderer;
}

export {createRenderer};