import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';


function loadModel(path, callback) {
    const loader = new GLTFLoader();

    loader.load(path, function (gltf) {

        callback(gltf.scene);

    }, undefined, function (error) {

        console.error(error);

    });
}

export {loadModel};