import {TextGeometry} from 'three/addons/geometries/TextGeometry.js';
import {FontLoader} from "three/addons/loaders/FontLoader.js";
import {MeshStandardMaterial} from "three";
import {Mesh} from "three";

let font;

function loadFont(scene, x, y, z, score, group) {
    const loader = new FontLoader();
    loader.load(
        '/static/js/threejs/Components/fonts/helvetiker_regular.typeface.json',
        function (fontParam) {
            font = fontParam;
            const model = generateObject(x, y, z, score, group);
            scene.add(model);
        });
}

function generateObject(x, y, z, score, group) {
    console.log(font);
    const geometry = new TextGeometry(score, {
        font: font,
        size: 10,
        depth: 4,
        curveSegments: 12,
        bevelEnabled: false,
        bevelThickness: 0.1,
        bevelSize: 0,
        bevelOffset: 0,
        bevelSegments: 5
    });
    geometry.computeBoundingBox();
    const material = new MeshStandardMaterial({color: "blue"});
    const materials = [material, material];
    const model = new Mesh(geometry, materials);
    const offsetX = geometry.boundingBox.max.x / 2;
    const offsetY = geometry.boundingBox.max.y / 2;
    model.position.set(-offsetX + x, -offsetY + y, z);
    group.add(model);
    return model;
}

function createFont(scene, x = 0, y = 0, z = -5, score = "00", group) {
    loadFont(scene, x, y, z, score, group); // Wait for the font to load

}

export {createFont};